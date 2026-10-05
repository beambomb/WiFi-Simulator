import json
from fastapi import APIRouter, Depends, HTTPException, WebSocket, WebSocketDisconnect, status
from pydantic import BaseModel
from sqlalchemy.orm import Session

from backend.auth import get_current_user
from backend.database import get_db
from backend.models import User, Simulation
from backend.physics.engine import evaluate_client_telemetry, compute_probe_heatmap

router = APIRouter(tags=["Simulation Engine"])

class CalculationRequest(BaseModel):
    router: dict
    walls: list[dict] = []
    clients: list[dict] = []
    environment: dict = {
        "noise_floor_dbm": -95.0,
        "path_loss_exponent": 2.2,
    }
    probe_step_m: float = 0.5

@router.post("/api/simulations/{sim_id}/calculate")
def calculate_simulation(
    sim_id: str,
    req: CalculationRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    sim = (
        db.query(Simulation)
        .filter(Simulation.id == sim_id, Simulation.user_id == current_user.id)
        .first()
    )
    if not sim:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Simulation not found")

    heatmap = compute_probe_heatmap(
        width_m=sim.room_width,
        length_m=sim.room_length,
        router=req.router,
        walls=req.walls,
        env=req.environment,
        step_m=req.probe_step_m,
    )

    client_telemetry = [
        evaluate_client_telemetry(c, req.router, req.walls, req.environment)
        for c in req.clients
    ]

    return {
        "simulation_id": sim_id,
        "heatmap": heatmap,
        "clients": client_telemetry,
    }

@router.websocket("/ws/simulation/{sim_id}")
async def websocket_simulation(websocket: WebSocket, sim_id: str):
    await websocket.accept()
    try:
        while True:
            raw_data = await websocket.receive_text()
            payload = json.loads(raw_data)

            width = float(payload.get("room_width", 10.0))
            length = float(payload.get("room_length", 8.0))
            router_data = payload.get("router", {})
            walls_data = payload.get("walls", [])
            clients_data = payload.get("clients", [])
            env_data = payload.get("environment", {"noise_floor_dbm": -95.0, "path_loss_exponent": 2.2})
            step = float(payload.get("probe_step_m", 0.5))

            heatmap = compute_probe_heatmap(width, length, router_data, walls_data, env_data, step)
            clients_eval = [
                evaluate_client_telemetry(c, router_data, walls_data, env_data)
                for c in clients_data
            ]

            await websocket.send_json({
                "type": "SIMULATION_UPDATE",
                "sim_id": sim_id,
                "heatmap": heatmap,
                "clients": clients_eval,
            })
    except WebSocketDisconnect:
        pass
