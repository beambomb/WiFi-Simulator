# 3D CAD WiFi Simulator

## Architectural Overview and Technical Documentation

### 1. Abstract and Problem Statement
In domestic and commercial wireless networking, Internet Service Providers (ISPs) and vendors frequently state that physical router placement has negligible impact on coverage and throughput. In practice, electromagnetic propagation at microwave frequencies (2.4 GHz, 5.0 GHz, and 6.0 GHz) undergoes severe attenuation, reflection, and absorption due to building architecture, structural wall materials, and indoor furniture. The resulting shadow fading and multipath degradation produce substantial dead zones, packet drops, and substandard Quality of Service (QoS).

The 3D CAD WiFi Simulator is an engineering-grade, full-stack simulation platform utilizing Agent-Based Modeling (ABM) and a high-performance Python (FastAPI) numerical engine. The application provides an interactive Computer-Aided Design (CAD) interface allowing users to define arbitrary floor spaces of dimension $M \times N$ meters, construct architectural walls and openings, place physical furniture, configure wireless emitters, and evaluate real-time Received Signal Strength Indicator (RSSI) fields and client device telemetry.

---

## 2. Core Architectural Pillars

### 2.1 Agent-Based Modeling (ABM) Paradigm
Unlike purely static heatmaps that treat space as a continuous scalar field without interacting entities, this system models the wireless environment as an ensemble of discrete autonomous agents:
- **Emitter Agents (Routers / Access Points):** Autonomous radio transmitters with configurable transmission power ($P_{\text{tx}}$), multi-band support (2.4 GHz, 5.0 GHz, 6.0 GHz), channel bandwidth (20 MHz to 160 MHz), and Multiple-Input Multiple-Output (MIMO) spatial streams ($1\times1, 2\times2, 4\times4$). Emitter agents govern channel selection, band steering, and dynamic rate adaptation.
- **Attenuator and Obstacle Agents (Walls and Openings):** Structural obstacles with defined geometric lengths, thicknesses ($0.05\text{ m}$ to $0.50\text{ m}$), and frequency-dependent dielectric penetration losses.
- **Interior Obstacle Agents (`FurnitureAgent`):** Three-dimensional volumetric entities (metal appliances, large mirrors, water containers, wardrobes, and upholstery) characterized by both absorption loss and specular reflection coefficients.
- **Receiver Agents (Client Devices):** Mobile and stationary endpoints operating under distinct behavioral personas (Gamer PC, 4K Streamer, Low-Power IoT Sensor, and Mobile Smartphone) evaluating signal-to-noise ratio (SNR), latency jitter, and packet delivery satisfaction.

### 2.2 Strict CAD Design Standards (Zero-Gradient Policy)
In adherence to technical CAD and Finite Element Analysis (FEA) standards (such as ANSYS, AutoCAD, and MATLAB field solvers), all user interface surfaces, structural models, and field visualizations strictly avoid linear and radial gradients. Signal coverage is rendered through stepped discrete iso-contours with high-contrast, flat solid color bands, ensuring unambiguous geometric thresholds for engineering evaluation.

---

## 3. Electromagnetic Wave Propagation Physics

### 3.1 Free-Space Path Loss (FSPL) and Log-Distance Model
For unobstructed line-of-sight (LOS) propagation over three-dimensional Euclidean distance $d$ (meters) at center frequency $f$ (MHz):

$$\text{FSPL}(d, f) = 20 \log_{10}(d) + 20 \log_{10}(f) - 27.55$$

For enclosed indoor environments subject to path loss exponent $n$:

$$\text{PL}_{\text{distance}}(d, f) = \left[ 20 \log_{10}(f) - 27.55 \right] + 10 \cdot n \cdot \log_{10}(d)$$

Default reference values:
- Free space exponent: $n = 2.0$
- Typical indoor residential/office: $n = 2.2$ to $3.0$
- Thermal noise floor: $N_0 = -95.0\text{ dBm}$

### 3.2 Motley-Keenan Multi-Wall Attenuation Formulation
When a direct ray vector between an emitter and receiver intersects $k$ obstacle types, cumulative penetration attenuation is summed along the path:

$$\text{PL}_{\text{total}}(d, f) = \text{PL}_{\text{distance}}(d, f) + \sum_{i=1}^{k} \left( W_i \cdot \alpha_i(f, \tau_i) \right)$$

Where:
- $W_i$ denotes the number of traversed obstacles of type $i$.
- $\alpha_i(f, \tau_i)$ denotes the empirical attenuation coefficient in decibels (dB), scaled by physical thickness $\tau_i$.

### 3.3 Material Attenuation and Reflection Database
Physical constants derived from NIST, ITU-R P.1238, and empirical RF characterization benchmarks:

| Material / Obstacle | Standard Thickness | Attenuation (2.4 GHz) | Attenuation (5.0 GHz) | Attenuation (6.0 GHz) | Reflection Coefficient ($R$) | CAD Color Hex |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| Reinforced Concrete | 0.15 m | 14.0 dB | 22.0 dB | 25.0 dB | 0.20 | `#718096` |
| Red Brick Wall | 0.12 m | 8.0 dB | 14.0 dB | 16.5 dB | 0.15 | `#C25E40` |
| Drywall / Gypsum | 0.10 m | 3.0 dB | 5.0 dB | 6.2 dB | 0.10 | `#CBD5E1` |
| Solid Wood / Timber | 0.08 m | 4.0 dB | 7.0 dB | 8.5 dB | 0.12 | `#A2714B` |
| Interior Wooden Door | 0.04 m | 2.5 dB | 4.0 dB | 5.0 dB | 0.10 | `#855836` |
| Clear Window Glass | 0.01 m | 2.0 dB | 3.5 dB | 4.2 dB | 0.15 | `#60A5FA` |
| Metal Sheet / Shield | 0.005 m | 28.0 dB | 35.0 dB | 40.0 dB | 0.95 | `#475569` |
| Refrigerator / Appliance | 0.80 m x 0.80 m | 30.0 dB | 38.0 dB | 42.0 dB | 0.90 | `#64748B` |
| Full-Length Wall Mirror | 0.05 m x 1.20 m | 15.0 dB | 20.0 dB | 23.0 dB | 0.85 | `#93C5FD` |
| Fish Aquarium / Water Tank | 0.40 m x 1.00 m | 16.0 dB | 24.0 dB | 28.0 dB | 0.25 | `#0284C7` |
| Wardrobe / Clothes Closet | 0.60 m x 1.50 m | 8.0 dB | 12.0 dB | 14.0 dB | 0.15 | `#B45309` |
| Upholstered Sofa / Bed | 1.00 m x 2.00 m | 2.5 dB | 4.0 dB | 4.8 dB | 0.05 | `#6B7280` |

### 3.4 Specular Multipath Reflection (Image Source Method)
Planar surfaces with high reflection coefficients (metal appliances, silver-backed glass mirrors) generate secondary reflection paths. For emitter coordinate $E$ and reflective plane $P$, the virtual image source is $E'$. The path length of the reflected ray reaching receiver $R$ is:

$$d_{\text{refl}} = \|R - E'\|$$

The received reflected power component is calculated as:

$$P_{\text{refl}} = P_{\text{tx}} + G_{\text{tx}} - \text{FSPL}(d_{\text{refl}}, f) + 10 \log_{10}(R) - \sum \text{Loss}_{\text{wall}}$$

Total effective received signal strength ($\text{RSSI}_{\text{total}}$) synthesizes direct and reflected components:

$$\text{RSSI}_{\text{total}} = 10 \log_{10} \left( 10^{\frac{\text{RSSI}_{\text{direct}}}{10}} + 10^{\frac{P_{\text{refl}}}{10}} \right)$$

### 3.5 Link Capacity and Throughput Estimation
Practical link speeds are estimated via modified Shannon-Hartley capacity bounds scaled by spectral efficiency $\eta = 0.60$ and MIMO streams $N_{\text{ss}}$:

$$C = B \cdot \log_{2}\left(1 + 10^{\frac{\text{SNR}}{10}}\right) \cdot \eta \cdot N_{\text{ss}}$$

Where:
- $B$: Channel Bandwidth in Hertz ($20, 40, 80, 160\text{ MHz}$).
- $\text{SNR} = \text{RSSI} - N_0$ (dB).
- Throughput drops to 0 Mbps when $\text{SNR} \le 5.0\text{ dB}$ or $\text{RSSI} < \text{Sensitivity Threshold}$.

---

## 4. Signal Quality Tiers (Stepped Iso-Bands)

Field distributions are rendered into five discrete, non-interpolated stepped iso-bands:

| Signal Range (RSSI) | Link Classification | Solid CAD Color | Physical Network Performance |
| :--- | :--- | :--- | :--- |
| $\ge -50.0\text{ dBm}$ | Excellent | `#10B981` (Emerald) | Maximum modulation rate, zero packet drops, ultra-low jitter. |
| $-51.0\text{ to } -65.0\text{ dBm}$ | Good | `#3B82F6` (Blue) | High throughput, seamless 4K video conferencing, reliable QoS. |
| $-66.0\text{ to } -75.0\text{ dBm}$ | Fair | `#F59E0B` (Amber) | Standard browsing, rate fallback active, increased latency under load. |
| $-76.0\text{ to } -85.0\text{ dBm}$ | Poor | `#EF4444` (Red) | High retransmission rates, frequent buffering, roaming boundary. |
| $< -85.0\text{ dBm}$ | Dead Zone | `#1F2937` (Dark Gray) | Link termination, handshake failure, unserviceable region. |

---

## 5. System Architecture

```
+---------------------------------------------------------------------------------+
|                               CLIENT LAYER                                      |
|                                                                                 |
|  [ Three.js Viewport (WebGL) ]        [ Clean CAD UI (HTML/CSS) ]               |
|  - 3D Perspective & 2D Orthographic   - Toolbar, Dimension Modal, Inspector     |
|  - Metric Dynamic Grid (1m x 0.25m)   - Live Telemetry Badges, Coverage Stats   |
|  - Stepped Iso-Band Heatmap Mesh      - Zero Gradients / Flat Solid Palettes    |
+---------------------------------------------------------------------------------+
                                        │
                         HTTP REST JSON │ WebSocket Streaming
                                        ▼
+---------------------------------------------------------------------------------+
|                             BACKEND API GATEWAY                                 |
|                                                                                 |
|  [ FastAPI Application (Python 3.12) ]                                          |
|  - Authentication Router: /api/auth (Register, Login, Token, Me)                |
|  - Simulation CRUD Router: /api/simulations (Create, List, Read, Update, Delete)|
|  - Simulation Engine: /api/simulations/{id}/calculate                           |
|  - WebSocket Pipeline: /ws/simulation/{id} (Sub-50ms live dragging stream)     |
|  - Security Middleware: Stateless JWT (HMAC-SHA256), Bcrypt, Tenant Isolation   |
+---------------------------------------------------------------------------------+
          │                                              │
          ▼                                              ▼
+-----------------------------+        +------------------------------------------+
|      DATABASE LAYER         |        |         PHYSICS & ABM ENGINE             |
|                             |        |                                          |
|  [ SQLAlchemy 2.0 ORM ]     |        |  - NumPy Vectorized RF Propagation       |
|  - users table              |        |  - Cross-Product 2D Raycast Intersector  |
|  - simulations table        |        |  - Specular Reflection Image Source      |
|  (SQLite / PostgreSQL)      |        |  - Shannon-Hartley Throughput Estimator  |
+-----------------------------+        +------------------------------------------+
```

---

## 6. Directory Layout

```text
wifi_simulator/
├── .agents/                     # Antigravity IDE Customization System
│   ├── rules/                   # Active Workspace System Rules (always_on)
│   │   ├── code-style.md        # Commit rules, concise comment standards
│   │   ├── design.md            # Zero-gradient CAD design tokens
│   │   ├── prd.md               # Product requirements and personas
│   │   ├── architecture.md      # Full-stack design and API contracts
│   │   ├── specs.md             # Electromagnetic formulas and material tables
│   │   └── tasks.md             # Sprint tracking and API integration contract
│   └── workflows/
│       └── commit-push.md       # Slash command workflow (/commit-push)
├── agents/                      # Comprehensive Architecture Documentation
│   ├── AGENTS.md
│   ├── DESIGN.md
│   ├── PRD.md
│   ├── ARCHITECTURE.md
│   ├── SPECS.md
│   └── TASKS.md
├── backend/                     # Python FastAPI Application
│   ├── main.py                  # Entrypoint, CORS, router mounts, static server
│   ├── config.py                # Environment configurations and JWT secrets
│   ├── database.py              # SQLAlchemy engine and session dependency
│   ├── models.py                # User and Simulation database models
│   ├── schemas.py               # Pydantic schemas for auth and spatial CRUD
│   ├── auth.py                  # Bcrypt hashing and JWT bearer guard
│   ├── requirements.txt         # Pinned backend dependencies
│   ├── api/
│   │   ├── auth.py              # User authentication endpoints
│   │   ├── simulations.py       # Simulation CRUD endpoints
│   │   └── simulation_engine.py # REST calculation and WebSocket stream
│   └── physics/
│       ├── materials.py         # Attenuation database and frequency scaling
│       ├── raycast.py           # Vector line-segment intersection algorithms
│       └── engine.py            # NumPy RF field propagation and telemetry
├── frontend/                    # Web Client
│   ├── package.json             # Three.js and Vite configuration
│   ├── package-lock.json
│   └── index.html
├── .gitignore                   # Ignores venv, node_modules, cache, db
└── README.md                    # Project technical documentation
```

---

## 7. API Specification Summary

### 7.1 Authentication Endpoints
- `POST /api/auth/register`: Create user account (`email`, `password`). Returns `201 Created` with User object.
- `POST /api/auth/login`: Form-encoded authentication (`username`, `password`). Returns `200 OK` with `{ access_token, token_type: "bearer", user }`.
- `GET /api/auth/me`: Validates JWT bearer token and returns authenticated user profile.

### 7.2 Simulation Project Management (CRUD)
- `POST /api/simulations`: Creates a new simulation project with initial room dimensions $M \times N$ meters, ceiling height, and serialized `agents_data`.
- `GET /api/simulations`: Lists all simulation projects owned by the authenticated user.
- `GET /api/simulations/{id}`: Retrieves complete layout and serialized agent state for project `{id}`.
- `PUT /api/simulations/{id}`: Persists modifications to layout geometry, room dimensions, and agent models.
- `DELETE /api/simulations/{id}`: Removes simulation record with ownership verification. Returns `204 No Content`.

### 7.3 Real-Time Physics and WebSocket Pipeline
- `POST /api/simulations/{id}/calculate`: Synchronous computation of probe grid matrix ($M \times N$) and client device telemetry.
- `WS /ws/simulation/{id}`: Bi-directional WebSocket stream for low-latency calculations during live object dragging.

---

## 8. Installation and Execution Guide

### 8.1 Prerequisites
- Python 3.12 or higher
- Node.js 18.0 or higher with npm
- Git

### 8.2 Backend Setup
1. Open terminal in the project root directory.
2. Initialize and activate Python virtual environment:
   ```powershell
   python -m venv venv
   .\venv\Scripts\Activate.ps1
   ```
3. Install dependencies:
   ```powershell
   pip install -r backend/requirements.txt
   ```
4. Start the FastAPI backend server:
   ```powershell
   uvicorn backend.main:app --host 127.0.0.1 --port 8000 --reload
   ```
5. Verify health endpoint and API documentation:
   - Health Check: `http://127.0.0.1:8000/health`
   - Interactive Swagger Documentation: `http://127.0.0.1:8000/docs`

### 8.3 Frontend Setup
1. Navigate to the frontend directory:
   ```powershell
   cd frontend
   npm install
   ```
2. Start the development server:
   ```powershell
   npm run dev
   ```
3. Open `http://localhost:5173` in a modern WebGL-compliant browser.

### 8.4 Simulation Engine Verification
To execute a verification test of the multi-wall path loss engine and client device telemetry without starting the web server, run:
```powershell
.\venv\Scripts\python -c "
from backend.physics.engine import evaluate_client_telemetry, compute_probe_heatmap

router = {'x': 2.0, 'y': 2.0, 'frequency_ghz': 5.0, 'tx_power_dbm': 20.0, 'channel_width_mhz': 80, 'mimo_streams': 2}
walls = [{'x1': 5.0, 'y1': 0.0, 'x2': 5.0, 'y2': 8.0, 'material': 'concrete', 'thickness': 0.15}]
client_los = {'id': 'c1', 'name': 'Laptop LOS', 'x': 3.0, 'y': 2.0, 'traffic_type': 'gaming'}
client_nlos = {'id': 'c2', 'name': 'Laptop Behind Concrete', 'x': 7.0, 'y': 2.0, 'traffic_type': 'streaming'}
env = {'noise_floor_dbm': -95.0, 'path_loss_exponent': 2.2}

print('LOS Telemetry:', evaluate_client_telemetry(client_los, router, walls, env))
print('NLOS Telemetry:', evaluate_client_telemetry(client_nlos, router, walls, env))
print('Coverage Matrix:', compute_probe_heatmap(10.0, 8.0, router, walls, env, step_m=1.0)['coverage_stats'])
"
```

---

## 9. Operating Guidelines and Version Control Cadence
- **Repository Governance:** All development activities are governed by the guidelines defined in `.agents/rules/code-style.md`.
- **Commit Boundary:** A maximum of three logical changes (file additions, edits, or fixes) are permitted per Git commit.
- **Workflow Automation:** Full repository synchronization and batched commits can be triggered via the `/commit-push` workflow.
