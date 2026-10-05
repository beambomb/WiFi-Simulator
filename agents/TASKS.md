# TASKS.md — Implementation Roadmap & Sprint Tracking

This document outlines the phased development plan and task checklist for building the **3D CAD WiFi Simulator** with a **FastAPI** backend and **Three.js** frontend. Every milestone enforces the rules set forth in `AGENTS.md` (maximum 3 changes per commit, minimal comments, clean flat CAD styling, zero gradients).

---

## Milestone 0: Documentation & Architectural Blueprints
*Goal: Establish requirements, design system, physical specifications, full-stack architecture, and agent operational guidelines.*

- [x] Create `AGENTS.md` (Operational instructions, commit cadence, coding standards).
- [x] Create `DESIGN.md` (Zero-gradient flat palette, CAD UI/UX hierarchy, stepped iso-band rules).
- [x] Create `PRD.md` (Problem statement, user stories, MVP scope, Auth, CRUD, New Simulation).
- [x] Create `ARCHITECTURE.md` (Full-stack architecture, DB schema, REST/WebSocket API, folder layout).
- [x] Create `SPECS.md` (WiFi physics, FSPL formulas, multi-wall attenuation matrix, ray intersection).
- [x] Create `TASKS.md` (Roadmap, milestones, and task tracking).

---

## Milestone 1: Backend Scaffolding & Database Setup
*Goal: Establish the Python FastAPI backend, database connection, and data models.*

- [x] Initialize Python environment and `backend/requirements.txt` (FastAPI, Uvicorn, SQLAlchemy, Pydantic, NumPy, Bcrypt, PyJWT).
- [x] Configure SQLite database engine, session factory, and base model in `backend/database.py`.
- [x] Create `User` database model and Pydantic schemas in `backend/models.py` & `backend/schemas.py`.
- [x] Create `Simulation` database model and Pydantic schemas in `backend/models.py` & `backend/schemas.py`.
- [x] Verify database table generation and test basic FastAPI health endpoint (`GET /health`).

---

## Milestone 2: Authentication, Security & CRUD APIs
*Goal: Implement secure user registration, JWT login, and full project CRUD operations.*

- [x] Implement password hashing (Bcrypt) and JWT token generation/validation in `backend/auth.py`.
- [x] Implement user registration (`POST /api/auth/register`) and login (`POST /api/auth/login`) in `backend/api/auth.py`.
- [x] Build `get_current_user` dependency to protect private endpoints.
- [x] Implement Simulation CRUD endpoints in `backend/api/simulations.py`:
  - [x] `POST /api/simulations` (Create new simulation project with $M \times N$ sizing).
  - [x] `GET /api/simulations` (List all projects belonging to authenticated user).
  - [x] `GET /api/simulations/{id}` (Retrieve specific project with full layout).
  - [x] `PUT /api/simulations/{id}` (Update/Save changes to layout and agent positions).
  - [x] `DELETE /api/simulations/{id}` (Delete project with owner verification).

---

## Milestone 3: Frontend 3D CAD Viewport & Project Management UI
*Goal: Build the flat CAD interface, 3D metric grid, "New Simulation" dialog, and Auth modals.*

- [ ] Setup frontend structure with zero-gradient flat CAD styling defined in `DESIGN.md`.
- [ ] Implement 3D CAD Viewport using Three.js (Perspective 3D Orbit & Orthographic 2D Top-Down).
- [ ] Implement dynamic metric grid rendering that auto-resizes to room dimensions $M \times N$.
- [ ] Build **"New Simulation" Modal Dialog**:
  - [ ] Form for Title, Width $M$ (m), Length $N$ (m), and Ceiling Height (m).
  - [ ] Unsaved changes prompt.
  - [ ] Dynamic canvas and grid reset matching the new room size.
- [ ] Build Login / Register UI modals and connect with backend JWT authentication.
- [ ] Build Project Drawer / Switcher (load saved floor plans from backend).

---

## Milestone 4: Agent Placement & CAD Drafting Tools
*Goal: Enable interactive creation of physical agents (Walls, Doors, Windows, Routers, Devices).*

- [ ] Implement CAD Toolbar and Tool State Manager (Select, Wall, Door, Window, Router, Client Device).
- [ ] Implement Two-Click Wall Drafting Tool:
  - [ ] Click-and-drag wall creation with real-time length (m) and angle display.
  - [ ] Material selector (Concrete, Brick, Drywall, Wood, Metal) with flat color coding.
  - [ ] Wall opening placement (Wooden Door, Glass Window).
- [ ] Implement Router Agent placement:
  - [ ] 3D router mesh/model with frequency toggle (2.4 GHz vs. 5.0 GHz) and TX power slider.
- [ ] Implement Client Device placement:
  - [ ] Device models (Laptop, Smartphone, Smart TV) with live telemetry badge.
- [ ] Implement grid snapping ($0.25\text{ m}$ / $0.50\text{ m}$) and selection bounding boxes.

---

## Milestone 5: Python RF Simulation Engine & WebSocket Pipeline
*Goal: Compute realistic electromagnetic propagation and stream live signal data to the client.*

- [x] Implement 2D line segment intersection in `backend/physics/raycast.py`.
- [x] Implement NumPy vectorized Multi-Wall Cost231 / Motley-Keenan path loss in `backend/physics/engine.py`.
- [x] Establish WebSocket endpoint (`/ws/simulation/{id}`) for low-latency live calculation streaming.
- [x] Calculate live RSSI ($-\text{dBm}$) and link speed estimates ($\text{Mbps}$) for placed client devices.
- [x] Implement multi-parameter telemetry (MIMO streams, channel width, custom thickness, traffic satisfaction).

---

## Milestone 6: Stepped Iso-Band Heatmap & Analytics
*Goal: Visualize signal coverage using discrete, flat contour bands across the $M \times N$ floor.*

- [ ] Generate probe sampling grid in Python and stream scalar field matrix to frontend.
- [ ] Render planar heatmap mesh with discrete stepped color bands (Zero gradients: Emerald, Blue, Amber, Red, Dark Gray).
- [ ] Build Coverage Analytics dashboard:
  - [ ] Percentage of floor area with Excellent/Good coverage.
  - [ ] Percentage of floor area classified as Dead Zone ($< -85\text{ dBm}$).
- [ ] Add Heatmap height slider (floor level to desk height $0.8\text{ m}$) and visibility toggle.

---

## Milestone 7: Smart Optimization & Router Placement Advisor
*Goal: Solve customer frustration by recommending the mathematically optimal router position.*

- [ ] Implement grid search evaluation algorithm in Python to test candidate router coordinates.
- [ ] Score candidate locations based on maximizing client device RSSI and minimizing dead zone area.
- [ ] Add "Suggest Optimal Router Position" button with visual indicator of ideal placement in 3D CAD space.
- [ ] Add Floor Plan Export feature (JSON download / PDF summary).

---

## Appendix: Frontend Integration Contract (Essential API Endpoints)

Untuk Frontend Agent / Developer, gunakan kontrak endpoint API berikut:

### 1. Base URL & Headers
- **Base URL:** `http://localhost:8000` (atau relative `/` saat production).
- **Authenticated Headers:** `Authorization: Bearer <access_token>`

### 2. Authentication Endpoints

#### A. Register New User
- **Method & Path:** `POST /api/auth/register`
- **Request Body:**
  ```json
  {
    "email": "user@example.com",
    "password": "secretpassword"
  }
  ```
- **Response (`201 Created`):**
  ```json
  {
    "id": "uuid-string",
    "email": "user@example.com",
    "created_at": "2026-10-05T13:45:00Z"
  }
  ```

#### B. Login & Get JWT Token
- **Method & Path:** `POST /api/auth/login`
- **Request Content-Type:** `application/x-www-form-urlencoded`
- **Form Data:**
  - `username`: `user@example.com`
  - `password`: `secretpassword`
- **Response (`200 OK`):**
  ```json
  {
    "access_token": "eyJhbGciOi...",
    "token_type": "bearer",
    "user": {
      "id": "uuid-string",
      "email": "user@example.com",
      "created_at": "2026-10-05T13:45:00Z"
    }
  }
  ```

#### C. Get Current Profile
- **Method & Path:** `GET /api/auth/me`
- **Headers:** `Authorization: Bearer <token>`
- **Response (`200 OK`):** User object.

---

### 3. Simulation Project CRUD Endpoints (Protected)

#### A. Create New Simulation ("New Simulation" Dialog)
- **Method & Path:** `POST /api/simulations`
- **Headers:** `Authorization: Bearer <token>`
- **Request Body:**
  ```json
  {
    "title": "Living Room Floor 1",
    "room_width": 12.0,
    "room_length": 8.0,
    "room_height": 2.8,
    "grid_step": 0.25,
    "agents_data": "{\"routers\":[],\"walls\":[],\"devices\":[]}"
  }
  ```
- **Response (`201 Created`):** Complete simulation object with `id`.

#### B. List All User's Saved Simulations
- **Method & Path:** `GET /api/simulations`
- **Headers:** `Authorization: Bearer <token>`
- **Response (`200 OK`):**
  ```json
  [
    {
      "id": "sim-uuid-1",
      "title": "Living Room Floor 1",
      "room_width": 12.0,
      "room_length": 8.0,
      "room_height": 2.8,
      "updated_at": "2026-10-05T13:45:00Z"
    }
  ]
  ```

#### C. Load Specific Simulation
- **Method & Path:** `GET /api/simulations/{id}`
- **Headers:** `Authorization: Bearer <token>`
- **Response (`200 OK`):** Complete simulation object including full `agents_data`.

#### D. Save / Update Simulation
- **Method & Path:** `PUT /api/simulations/{id}`
- **Headers:** `Authorization: Bearer <token>`
- **Request Body (Partial fields allowed):**
  ```json
  {
    "title": "Updated Room Name",
    "room_width": 14.0,
    "agents_data": "{\"routers\":[...],\"walls\":[...],\"devices\":[...]}"
  }
  ```
- **Response (`200 OK`):** Updated simulation record.

#### E. Delete Simulation
- **Method & Path:** `DELETE /api/simulations/{id}`
- **Headers:** `Authorization: Bearer <token>`
- **Response (`204 No Content`):** Empty.

---

### 4. Health Check
- **Method & Path:** `GET /health`
- **Response (`200 OK`):** `{"status": "ok", "project": "3D CAD WiFi Simulator"}`
