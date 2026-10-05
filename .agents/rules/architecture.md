---
trigger: always_on
description: Full-Stack Architecture, Database Schema, REST/WebSocket APIs, and Directory Blueprint
---

# ARCHITECTURE.md — System Architecture & Full-Stack Design

This document details the full-stack software architecture, database schema, REST/WebSocket API contracts, security mechanisms, and Agent-Based Modeling (ABM) engine for the **3D CAD WiFi Simulator**.

---

## 1. High-Level Full-Stack Architecture

```mermaid
graph TD
    subgraph Client_Browser ["Client Browser (Frontend)"]
        UI["Clean CAD UI (Toolbar, Topbar, Inspector, New Sim Modal)"]
        Canvas3D["3D CAD Viewport (Three.js / WebGL - 60 FPS)"]
        State["Client State & Auth Store (JWT, Active Simulation)"]
    end

    subgraph API_Gateway ["FastAPI Application"]
        StaticServer["Static Files Server (Serves HTML, CSS, JS)"]
        AuthMiddleware["JWT Authentication & Security Middleware"]
        RouterAuth["/api/auth (Register, Login, Me)"]
        RouterSim["/api/simulations (CRUD Operations)"]
        WSHandler["WebSocket /ws/simulation/{id} (Live RF Streaming)"]
    end

    subgraph Backend_Engine ["Python ABM & Physics Engine"]
        AgentManager["Agent Manager (Routers, Walls, Clients, Probes)"]
        NumPyPhysics["NumPy Vectorized RF Engine (FSPL + Multi-Wall)"]
        Optimizer["Smart Placement Advisor (Grid Search)"]
    end

    subgraph Database_Layer ["Persistence Layer"]
        DB[(SQLite / PostgreSQL via SQLAlchemy)]
        UserTable["users Table"]
        SimTable["simulations Table"]
    end

    Client_Browser <-->|HTTP / REST (JSON)| RouterAuth
    Client_Browser <-->|HTTP / REST (JSON)| RouterSim
    Client_Browser <-->|Bi-directional WebSocket| WSHandler
    Client_Browser --- StaticServer
    
    RouterAuth --> DB
    RouterSim --> DB
    RouterSim --> AgentManager
    WSHandler --> AgentManager
    AgentManager --> NumPyPhysics
    AgentManager --> Optimizer
    DB --- UserTable
    DB --- SimTable
```

---

## 2. Database Schema (SQLAlchemy / SQLModel)

### 2.1 Table: `users`
| Column | Type | Constraints | Description |
| :--- | :--- | :--- | :--- |
| `id` | UUID / String | Primary Key, Index | Unique user identifier |
| `email` | String(255) | Unique, Index, Not Null | User login email |
| `hashed_password` | String(255) | Not Null | Bcrypt hashed password |
| `created_at` | DateTime | Default: UTC Now | Account creation timestamp |

### 2.2 Table: `simulations`
| Column | Type | Constraints | Description |
| :--- | :--- | :--- | :--- |
| `id` | UUID / String | Primary Key, Index | Unique simulation project ID |
| `user_id` | UUID / String | Foreign Key (`users.id`), Index | Owner reference |
| `title` | String(100) | Not Null | Project name (e.g. "Living Room 1st Floor") |
| `room_width` | Float | Not Null, Default: 10.0 | Width $M$ in meters |
| `room_length` | Float | Not Null, Default: 8.0 | Length $N$ in meters |
| `room_height` | Float | Not Null, Default: 2.8 | Ceiling height in meters |
| `grid_step` | Float | Default: 0.25 | Snapping resolution in meters |
| `agents_data` | JSON / Text | Not Null | Serialized agent models (walls, routers, devices) |
| `created_at` | DateTime | Default: UTC Now | Timestamp created |
| `updated_at` | DateTime | Auto-update on save | Timestamp last modified |

---

## 3. Security Architecture
1. **Password Hashing:** Passwords are never stored in plaintext; hashed using `passlib[bcrypt]` with dynamic salts.
2. **Stateless JWT Authentication:**
   - Token payload: `{ "sub": user_id, "exp": expiration_timestamp }`.
   - Signed using `HMAC-SHA256` with a server-side secret key (`SECRET_KEY`).
   - Protected endpoints utilize FastAPI's `Depends(get_current_user)` dependency.
3. **Data Ownership Isolation:**
   - Every database query for simulations enforces `WHERE simulations.user_id == current_user.id`.
   - Access attempts to records owned by other users return `404 Not Found` or `403 Forbidden`.
4. **Input Validation:**
   - Strict Pydantic models validate all incoming requests, preventing SQL injection and malformed spatial payloads.
5. **CORS (Cross-Origin Resource Sharing):**
   - Configured via `fastapi.middleware.cors.CORSMiddleware` with explicit allowed origins.

---

## 4. REST & WebSocket API Specification

### 4.1 Authentication Endpoints
- `POST /api/auth/register` — Create account (`email`, `password`) $\rightarrow$ `{ "id", "email" }`.
- `POST /api/auth/login` — Authenticate (`username`/`email`, `password`) $\rightarrow$ `{ "access_token", "token_type": "bearer" }`.
- `GET /api/auth/me` — Retrieve current authenticated profile.

### 4.2 Simulation CRUD Endpoints
- `GET /api/simulations` — List all simulations belonging to current user (`id`, `title`, `room_width`, `room_length`, `updated_at`).
- `POST /api/simulations` — Create new simulation with room dimensions $M \times N$.
- `GET /api/simulations/{id}` — Fetch complete simulation record including full `agents_data`.
- `PUT /api/simulations/{id}` — Update / save simulation layout, room sizing, and agent configurations.
- `DELETE /api/simulations/{id}` — Delete simulation project.

### 4.3 Simulation & Physics Endpoints
- `POST /api/simulations/{id}/calculate` — Compute full RF path loss matrix over $M \times N$ probe points (returns discrete iso-band data + client RSSI telemetry).
- `WS /ws/simulation/{id}` — High-frequency WebSocket connection for streaming live agent positions and receiving instant scalar field matrices during interactive dragging.

---

## 5. "New Simulation" Lifecycle & Workflow

```
[ User clicks "+ New Simulation" ]
               │
               ▼
[ Unsaved Changes Check ]
  ├── Dirty State? -> Prompt: "Save current layout?"
  └── Clean State  -> Continue
               │
               ▼
[ Modal: Setup New Space ]
  - Title: "Main Office"
  - Dimensions: M = 12.0m, N = 8.0m, H = 2.8m
  - Grid Snap: 0.25m
               │
               ▼ [ Click "Create Space" ]
1. Frontend dispatches POST /api/simulations
2. Backend creates record in SQLite/PostgreSQL
3. Frontend resets 3D scene:
   - Removes existing wall meshes and router agents
   - Reconfigures metric grid geometry to 12.0m x 8.0m
   - Updates camera focus and status indicators
4. User immediately starts drafting walls and placing routers
```

---

## 6. Full-Stack Directory Structure

```
wifi_simulator/
├── .agents/                     # Rules & Workflows for Antigravity IDE
│   ├── rules/
│   │   ├── code-style.md
│   │   ├── design.md
│   │   ├── prd.md
│   │   ├── architecture.md
│   │   ├── specs.md
│   │   └── tasks.md
│   └── workflows/
│       └── commit-push.md
├── agents/                      # Comprehensive Project Documentation
│   ├── AGENTS.md
│   ├── DESIGN.md
│   ├── PRD.md
│   ├── ARCHITECTURE.md
│   ├── SPECS.md
│   └── TASKS.md
├── backend/                     # Python FastAPI Application
│   ├── main.py                  # Server entry & static file mounting
│   ├── requirements.txt         # Dependencies
│   ├── config.py                # Environment configs & JWT secrets
│   ├── database.py              # DB connection & sessionmaker
│   ├── models.py                # User and Simulation models
│   ├── schemas.py               # Pydantic schemas
│   ├── auth.py                  # Auth guards & hashing
│   └── api/
│       ├── auth.py              # Authentication routes
│       └── simulations.py       # Simulation CRUD routes
└── frontend/                    # Web Client (Vanilla JS / Three.js)
    ├── package.json             # Build tool / bundler configs
    └── package-lock.json
```
