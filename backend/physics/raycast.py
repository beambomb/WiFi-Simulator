from backend.physics.materials import get_wall_attenuation

def segment_intersects(p1: tuple[float, float], p2: tuple[float, float], 
                       p3: tuple[float, float], p4: tuple[float, float]) -> bool:
    # Cross product 2D segment-segment intersection
    x1, y1 = p1
    x2, y2 = p2
    x3, y3 = p3
    x4, y4 = p4

    d = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
    if abs(d) < 1e-9:
        return False

    t = ((x1 - x3) * (y3 - y4) - (y1 - y3) * (x3 - x4)) / d
    u = -((x1 - x2) * (y1 - y3) - (y1 - y2) * (x1 - x3)) / d

    return 0.0 <= t <= 1.0 and 0.0 <= u <= 1.0

def calculate_traversed_attenuation(
    source: tuple[float, float], 
    target: tuple[float, float], 
    walls: list[dict], 
    freq_ghz: float
) -> float:
    total_loss = 0.0
    for wall in walls:
        w_start = (float(wall.get("x1", 0)), float(wall.get("y1", 0)))
        w_end = (float(wall.get("x2", 0)), float(wall.get("y2", 0)))
        
        if segment_intersects(source, target, w_start, w_end):
            mat_key = wall.get("material", "drywall")
            thickness = float(wall.get("thickness", 0.15))
            total_loss += get_wall_attenuation(mat_key, freq_ghz, thickness)

    return total_loss
