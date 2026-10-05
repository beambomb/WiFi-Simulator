import math
import numpy as np
from backend.physics.raycast import calculate_traversed_attenuation

def calculate_fspl(distance_m: float, freq_mhz: float, n_exp: float = 2.0) -> float:
    d = max(0.5, distance_m)
    # Generalized Log-Distance Path Loss: L0 + 10*n*log10(d/d0)
    # L0 at 1m: 20log10(1) + 20log10(f) - 27.55 = 20log10(f) - 27.55
    l0 = 20.0 * math.log10(freq_mhz) - 27.55
    return l0 + 10.0 * n_exp * math.log10(d)

def estimate_throughput(
    rssi_dbm: float, 
    noise_floor_dbm: float, 
    bandwidth_mhz: int = 80, 
    mimo_streams: int = 2
) -> float:
    snr = rssi_dbm - noise_floor_dbm
    if snr <= 5.0:
        return 0.0

    # Shannon-Hartley capacity approximation with 60% efficiency factor
    snr_linear = 10.0 ** (snr / 10.0)
    bandwidth_hz = bandwidth_mhz * 1e6
    capacity_bps = bandwidth_hz * math.log2(1.0 + snr_linear) * 0.6 * mimo_streams
    return round(capacity_bps / 1e6, 1)

def evaluate_client_telemetry(client: dict, router: dict, walls: list[dict], env: dict) -> dict:
    rx = float(client.get("x", 0))
    ry = float(client.get("y", 0))
    rz = float(client.get("height_m", 0.8))

    tx = float(router.get("x", 0))
    ty = float(router.get("y", 0))
    tz = float(router.get("height_m", 1.2))

    dist_2d = math.hypot(rx - tx, ry - ty)
    dist_3d = math.sqrt(dist_2d ** 2 + (rz - tz) ** 2)

    freq_ghz = float(router.get("frequency_ghz", 5.0))
    freq_mhz = freq_ghz * 1000.0
    tx_power = float(router.get("tx_power_dbm", 20.0))
    tx_gain = float(router.get("antenna_gain_dbi", 3.0))
    rx_gain = float(client.get("antenna_gain_dbi", 0.0))
    rx_sensitivity = float(client.get("rx_sensitivity_dbm", -85.0))
    n_exp = float(env.get("path_loss_exponent", 2.2))
    noise_floor = float(env.get("noise_floor_dbm", -95.0))

    wall_loss = calculate_traversed_attenuation((tx, ty), (rx, ry), walls, freq_ghz)
    path_loss = calculate_fspl(dist_3d, freq_mhz, n_exp) + wall_loss

    rssi = round(tx_power + tx_gain + rx_gain - path_loss, 1)
    snr = round(rssi - noise_floor, 1)

    bw = int(router.get("channel_width_mhz", 80))
    mimo = int(router.get("mimo_streams", 2))
    throughput = estimate_throughput(rssi, noise_floor, bw, mimo)

    if rssi >= -50:
        quality = "excellent"
    elif rssi >= -65:
        quality = "good"
    elif rssi >= -75:
        quality = "fair"
    elif rssi >= rx_sensitivity:
        quality = "poor"
    else:
        quality = "dead_zone"

    traffic_demand = client.get("traffic_type", "streaming").lower()
    traffic_ok = (
        (traffic_demand == "gaming" and snr >= 25 and throughput >= 50) or
        (traffic_demand == "streaming" and throughput >= 25) or
        (traffic_demand == "iot" and rssi >= rx_sensitivity) or
        (throughput >= 10)
    )

    return {
        "client_id": client.get("id"),
        "rssi_dbm": rssi,
        "snr_db": snr,
        "throughput_mbps": throughput,
        "quality_tier": quality,
        "is_connected": rssi >= rx_sensitivity,
        "traffic_satisfied": traffic_ok,
        "wall_loss_db": round(wall_loss, 1),
        "distance_m": round(dist_3d, 2),
    }

def compute_probe_heatmap(
    width_m: float, 
    length_m: float, 
    router: dict, 
    walls: list[dict], 
    env: dict, 
    step_m: float = 0.5
) -> dict:
    cols = max(2, int(math.ceil(width_m / step_m)) + 1)
    rows = max(2, int(math.ceil(length_m / step_m)) + 1)

    tx = float(router.get("x", width_m / 2.0))
    ty = float(router.get("y", length_m / 2.0))
    tz = float(router.get("height_m", 1.2))
    freq_ghz = float(router.get("frequency_ghz", 5.0))
    freq_mhz = freq_ghz * 1000.0
    tx_power = float(router.get("tx_power_dbm", 20.0))
    tx_gain = float(router.get("antenna_gain_dbi", 3.0))
    n_exp = float(env.get("path_loss_exponent", 2.2))

    x_vals = np.linspace(0, width_m, cols)
    y_vals = np.linspace(0, length_m, rows)

    matrix = []
    excellent_pts = 0
    good_pts = 0
    fair_pts = 0
    poor_pts = 0
    dead_pts = 0

    for r in range(rows):
        row_vals = []
        py = float(y_vals[r])
        for c in range(cols):
            px = float(x_vals[c])
            dist_2d = math.hypot(px - tx, py - ty)
            dist_3d = math.sqrt(dist_2d ** 2 + tz ** 2)

            wall_loss = calculate_traversed_attenuation((tx, ty), (px, py), walls, freq_ghz)
            pl = calculate_fspl(dist_3d, freq_mhz, n_exp) + wall_loss
            val = round(tx_power + tx_gain - pl, 1)

            row_vals.append(val)
            if val >= -50:
                excellent_pts += 1
            elif val >= -65:
                good_pts += 1
            elif val >= -75:
                fair_pts += 1
            elif val >= -85:
                poor_pts += 1
            else:
                dead_pts += 1

        matrix.append(row_vals)

    total_pts = rows * cols
    return {
        "cols": cols,
        "rows": rows,
        "step_m": step_m,
        "rssi_matrix": matrix,
        "coverage_stats": {
            "excellent_pct": round(excellent_pts / total_pts * 100, 1),
            "good_pct": round(good_pts / total_pts * 100, 1),
            "fair_pct": round(fair_pts / total_pts * 100, 1),
            "poor_pct": round(poor_pts / total_pts * 100, 1),
            "dead_zone_pct": round(dead_pts / total_pts * 100, 1),
        }
    }
