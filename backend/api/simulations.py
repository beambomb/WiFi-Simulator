from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from backend.auth import get_current_user
from backend.database import get_db
from backend.models import User, Simulation
from backend.schemas import (
    SimulationCreate,
    SimulationUpdate,
    SimulationResponse,
    SimulationListItem,
)

router = APIRouter(prefix="/api/simulations", tags=["Simulations"])

@router.post("", response_model=SimulationResponse, status_code=status.HTTP_201_CREATED)
def create_simulation(
    sim_in: SimulationCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    sim = Simulation(
        user_id=current_user.id,
        title=sim_in.title,
        room_width=sim_in.room_width,
        room_length=sim_in.room_length,
        room_height=sim_in.room_height,
        grid_step=sim_in.grid_step,
        agents_data=sim_in.agents_data or '{"routers":[],"walls":[],"devices":[]}',
    )
    db.add(sim)
    db.commit()
    db.refresh(sim)
    return sim

@router.get("", response_model=list[SimulationListItem])
def list_simulations(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return (
        db.query(Simulation)
        .filter(Simulation.user_id == current_user.id)
        .order_by(Simulation.updated_at.desc())
        .all()
    )

@router.get("/{sim_id}", response_model=SimulationResponse)
def get_simulation(
    sim_id: str,
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
    return sim

@router.put("/{sim_id}", response_model=SimulationResponse)
def update_simulation(
    sim_id: str,
    sim_in: SimulationUpdate,
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

    update_data = sim_in.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(sim, field, value)

    db.commit()
    db.refresh(sim)
    return sim

@router.delete("/{sim_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_simulation(
    sim_id: str,
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

    db.delete(sim)
    db.commit()
    return None
