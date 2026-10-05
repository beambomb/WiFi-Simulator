# Material attenuation loss database (dB per penetration based on standard thickness)
MATERIAL_DATABASE = {
    "concrete": {
        "name": "Reinforced Concrete",
        "standard_thickness_m": 0.15,
        "loss_2_4ghz": 14.0,
        "loss_5_0ghz": 22.0,
        "loss_6_0ghz": 25.0,
        "color": "#718096",
    },
    "brick": {
        "name": "Red Brick",
        "standard_thickness_m": 0.12,
        "loss_2_4ghz": 8.0,
        "loss_5_0ghz": 14.0,
        "loss_6_0ghz": 16.5,
        "color": "#C25E40",
    },
    "drywall": {
        "name": "Drywall / Gypsum",
        "standard_thickness_m": 0.10,
        "loss_2_4ghz": 3.0,
        "loss_5_0ghz": 5.0,
        "loss_6_0ghz": 6.2,
        "color": "#CBD5E1",
    },
    "wood": {
        "name": "Solid Wood",
        "standard_thickness_m": 0.08,
        "loss_2_4ghz": 4.0,
        "loss_5_0ghz": 7.0,
        "loss_6_0ghz": 8.5,
        "color": "#A2714B",
    },
    "door": {
        "name": "Wooden Door",
        "standard_thickness_m": 0.04,
        "loss_2_4ghz": 2.5,
        "loss_5_0ghz": 4.0,
        "loss_6_0ghz": 5.0,
        "color": "#855836",
    },
    "glass": {
        "name": "Clear Glass Window",
        "standard_thickness_m": 0.01,
        "loss_2_4ghz": 2.0,
        "loss_5_0ghz": 3.5,
        "loss_6_0ghz": 4.2,
        "color": "#60A5FA",
    },
    "metal": {
        "name": "Metal Sheet / Shield",
        "standard_thickness_m": 0.005,
        "loss_2_4ghz": 28.0,
        "loss_5_0ghz": 35.0,
        "loss_6_0ghz": 40.0,
        "color": "#475569",
    },
}

def get_wall_attenuation(material_key: str, freq_ghz: float, thickness_m: float | None = None) -> float:
    mat = MATERIAL_DATABASE.get(material_key.lower(), MATERIAL_DATABASE["drywall"])
    if freq_ghz >= 5.8:
        base_loss = mat["loss_6_0ghz"]
    elif freq_ghz >= 4.5:
        base_loss = mat["loss_5_0ghz"]
    else:
        base_loss = mat["loss_2_4ghz"]

    if thickness_m and thickness_m > 0 and mat["standard_thickness_m"] > 0:
        ratio = max(0.2, min(5.0, thickness_m / mat["standard_thickness_m"]))
        return base_loss * ratio
    return base_loss
