# PRD.md — Product Requirements Document

## 1. Executive Summary & Problem Statement
- **The Core Problem:** Internet Service Providers (ISPs) often mislead customers with claims like *"putting your WiFi router anywhere in the house makes no difference."* In reality, physical distance, wall materials, architectural geometry, and poor placement cause severe dead zones, high latency, and buyer's remorse.
- **The Solution:** A full-stack web application featuring an interactive **3D CAD WiFi Simulator** powered by **Agent-Based Modeling (ABM)** and a high-performance **Python (FastAPI)** calculation backend. Users can manage multiple floor plans, create new custom $M \times N$ spaces, place physical agents (routers, walls, doors, devices), and inspect live RF signal coverage and dead zones in real-time.

---

## 2. Product Vision & Goals
1. **Empower Homeowners & Renters:** Provide definitive visual proof of signal attenuation and identify the optimal router location before running cables or purchasing costly mesh hardware.
2. **CAD-Grade Usability, Zero Friction:** Deliver a CAD-like architectural tool (clean, flat, zero gradients, metric precision) accessible directly in modern web browsers.
3. **Multi-Project Cloud Persistence:** Enable authenticated users to create, save, load, and manage multiple simulation projects across different spaces (e.g., "Living Room 1st Floor", "2-Bedroom Apartment").
4. **Scientifically Grounded ABM Simulation:** Model every physical element as an autonomous agent evaluated against empirical RF propagation standards.

---

## 3. User Personas
- **The Frustrated Customer (Primary):** Wants to diagnose dead spots in their home office or bedroom after an ISP installation, testing "what-if" router placements.
- **The Smart Home Planner:** Designing a new apartment/house layout and deciding where ethernet drop points and APs should be installed.
- **The Network Student / Technician:** Needs a fast visual communication tool to show clients how concrete vs. drywall affects 5 GHz vs. 2.4 GHz signal reach.

---

## 4. Key Functional Requirements

### 4.1 User Authentication & Security
- **User Registration & Login:** Email and password registration with encrypted credentials.
- **Session Management:** Stateless JSON Web Tokens (JWT) for secure API requests.
- **Data Ownership Isolation:** Users can only view, edit, or delete their own simulation projects; cross-tenant access is strictly blocked.
- **Input Sanitization & Schema Validation:** Strict Pydantic typing to prevent corrupted spatial payloads and unauthorized data injection.

### 4.2 Project & Simulation Management (CRUD)
- **New Simulation Workflow:**
  - Dedicated "+ New Simulation" action in the top navigation bar.
  - Sizing dialog prompting for Simulation Title, Width $M$ (meters), Length $N$ (meters), and Ceiling Height (meters).
  - Unsaved changes prompt (prevents accidental data loss).
  - Instant canvas reset and dynamic 3D metric grid reconfiguration matching the new dimensions.
- **Save / Auto-Save:** Persists full room geometry, agent positions, materials, and RF settings into the database.
- **Simulation Library (List & Load):** Drawer or modal allowing users to browse their saved floor plans and load any project into the 3D viewport seamlessly.
- **Delete Project:** Secure deletion of obsolete simulation records.

### 4.3 Space & 3D CAD Canvas
- **Custom Dimensions:** Configurable floor width ($M$) and length ($N$) in meters (default $10\text{ m} \times 8\text{ m}$).
- **Precision Grid:** Metric grid with selectable snapping increments ($0.25\text{ m}$, $0.5\text{ m}$, $1.0\text{ m}$).
- **Dual View Modes:**
  - **Top-Down 2D Architectural Plan:** For rapid drafting of walls and object alignment.
  - **3D Isometric CAD View:** For spatial awareness and visual validation.

### 4.4 Agent-Based Modeling (ABM) Entities
1. **Emitter Agent (WiFi Router / Access Point):**
   - Transmit power (default: $20\text{ dBm} / 100\text{ mW}$).
   - Frequency band toggle: $2.4\text{ GHz}$ vs. $5.0\text{ GHz}$ vs. $6.0\text{ GHz}$.
   - Channel bandwidth ($20, 40, 80, 160\text{ MHz}$) & MIMO streams ($1\times1, 2\times2, 4\times4$).
   - Autonomous behavior rules: Band steering, dynamic modulation rate fallback, and channel load congestion.
2. **Obstacle Agents (Structural & Interior Attenuators):**
   - **Structural Walls:** Concrete, Brick, Drywall, Wood, Metal, Openings (Doors, Windows).
   - **Furniture / Interior Objects (`FurnitureAgent`):** 3D volumetric obstacles (Refrigerator, Mirror, Fish Aquarium, Wardrobe, Sofa).
   - Dual physical interaction rules: **Transmission Loss** (absorption) and **Specular Reflection** (multipath bounce).
3. **Receiver Agents (Client Devices with Distinct Personas):**
   - **Gamer PC Persona:** Demands low latency (<20ms) and high SNR (>25 dB); logs retransmissions and frustration score.
   - **4K Streamer Persona (Smart TV):** Demands sustained throughput (>25 Mbps); simulates adaptive buffer depletion and downscaling (4K -> 1080p -> buffering).
   - **IoT Sensor Persona:** Low-power sleep/wake cycle; verifies link reliability on brief wakeups.
   - **Mobile Smartphone Persona:** Navigates spatial waypoints through rooms, evaluating roaming handover thresholds ($<-75\text{ dBm}$).

### 4.5 Simulation & Analysis Engine (Python FastAPI)
- **Multi-Wall Path Loss Computation:** Combines Free-Space Path Loss (FSPL) with obstacle penetration loss along direct ray vectors using NumPy vectorization.
- **Discrete Iso-Band Heatmap:** Live 2D/3D planar heatmap displaying stepped RF coverage zones (strictly flat colors, zero gradients).
- **Dead-Zone Calculator:** Summarizes total covered area percentage vs. unserviceable dead-zone percentage.
- **Optimal Placement Advisor:** Evaluates candidate router coordinates to maximize coverage across placed client devices.

---

## 5. Non-Functional Requirements
- **Performance:** Maintain 60 FPS viewport navigation and sub-50ms simulation recalculation.
- **Design Aesthetic:** Strictly flat design without gradients; maximum UX clarity, high contrast, and technical CAD precision.
- **Deployment Ease:** Container-ready single-service architecture (FastAPI serving static frontend assets and REST/WebSocket APIs).

---

## 6. Scope Boundaries
- **In-Scope (MVP):** Single-floor $M \times N$ layout, multi-wall attenuation, 2.4/5 GHz selection, router and client agents, flat iso-contour heatmap, user auth, and simulation CRUD.
- **Deferred to Later Phases:** Multi-story stairs RF bleed, complex dynamic multi-path reflection (ray bounces), outdoor foliage simulation, multi-AP mesh roaming handoff.
