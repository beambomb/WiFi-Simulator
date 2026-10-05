---
trigger: always_on
description: Full-Stack Architecture, Database Schema, and REST/WebSocket API Contracts
---

# Full-Stack Architecture & API Reference

## 1. System Structure
- **Backend:** Python 3.12 + FastAPI + SQLAlchemy (SQLite `wifi_simulator.db`) + NumPy ABM engine.
- **Frontend:** Vanilla JS / Three.js (WebGL 60 FPS) + Vite.
- **Communication:** REST JSON for CRUD & Auth; WebSocket `/ws/simulation/{id}` for live interactive dragging telemetry.

## 2. Database Schema
- `users`: `id` (UUID), `email` (unique), `hashed_password` (bcrypt), `created_at`.
- `simulations`: `id` (UUID), `user_id` (FK), `title`, `room_width` ($M$), `room_length` ($N$), `room_height`, `grid_step`, `agents_data` (JSON string), `created_at`, `updated_at`.

## 3. Essential Endpoints
- `POST /api/auth/register` (email, password)
- `POST /api/auth/login` (username, password -> bearer token)
- `GET /api/auth/me` (profile)
- `POST /api/simulations` (create new simulation with $M \times N$ size)
- `GET /api/simulations` (list user's simulations)
- `GET /api/simulations/{id}` (fetch simulation by ID)
- `PUT /api/simulations/{id}` (update room size or agents_data)
- `DELETE /api/simulations/{id}` (delete simulation)
