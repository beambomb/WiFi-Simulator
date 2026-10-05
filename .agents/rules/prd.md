---
trigger: always_on
description: Product Requirements, Problem Statement, Scope, and CRUD Workflows
---

# Product Requirements (PRD) Core

## 1. Problem Statement & Vision
- Problem: ISPs falsely claim *"putting your WiFi router anywhere in the house makes no difference"*, causing customer regret and dead zones.
- Solution: A 3D CAD WiFi Simulator using Agent-Based Modeling (ABM) and a Python FastAPI calculation engine.

## 2. Key Functional Capabilities
1. **Dynamic Room Sizing ($M \times N$ meters):** Configurable floor dimensions and ceiling height with real-time 3D grid reconfiguration.
2. **Interactive Agent-Based Modeling:**
   - Emitter Agents (WiFi Router / AP with 2.4/5/6 GHz, TX power).
   - Attenuator Agents (Concrete, Brick, Drywall, Wood, Door, Window with RF attenuation loss).
   - Receiver Agents (Laptops, Phones with live telemetry badges).
3. **Authentication & Multi-Project CRUD:**
   - Secure user accounts (JWT + Bcrypt).
   - Create new simulations, list floor plans, load projects, auto-save changes, and delete projects.
   - Strict data ownership isolation.
