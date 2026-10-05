# PRD.md — Product Requirements Document

## 1. Executive Summary & Problem Statement
- **The Core Problem:** Internet Service Providers (ISPs) often mislead customers by claiming *"putting your WiFi router anywhere in the house makes no difference."* In reality, structural obstacles, wall materials, physical distance, and poor placement cause severe dead zones, high latency, and buyer's remorse.
- **The Solution:** A lightweight, browser-based **3D CAD WiFi Simulator** utilizing **Agent-Based Modeling (ABM)**. Users define their custom floor space ($M \times N$ meters), map their home layout with material-accurate walls, place virtual router and client agents, and visually inspect signal coverage, attenuation, and dead zones in real-time.

---

## 2. Product Vision & Goals
1. **Empower Homeowners & Renters:** Provide clear visual proof of why dead zones occur and identify the optimal router location before running cables or purchasing costly mesh hardware.
2. **CAD-Grade Usability, Zero Friction:** Deliver a CAD-like architectural tool (clean, flat, precise) that runs in any modern browser without heavy installations.
3. **Scientifically Grounded ABM Simulation:** Model every physical element (emitters, obstacles, client receivers) as autonomous agents with physically validated RF attenuation and path-loss behaviors.

---

## 3. User Personas
- **The Frustrated Customer (Primary):** Wants to diagnose dead spots in their home office or bedroom after an ISP installation, testing "what-if" router placements.
- **The Smart Home Planner:** Designing a new apartment/house layout and deciding where ethernet drop points and APs should be installed.
- **The Network Student / Technician:** Needs a quick, visual communication tool to show clients how concrete vs. drywall affects 5 GHz vs. 2.4 GHz signal reach.

---

## 4. Key Functional Requirements

### 4.1 Space & Canvas Configuration
- **Custom Dimensions:** Users can specify floor width ($M$) and length ($N$) in meters (e.g., $10\text{ m} \times 8\text{ m}$), with configurable ceiling height (default $2.8\text{ m}$).
- **Precision Grid:** Metric grid with selectable snapping increments ($0.25\text{ m}$, $0.5\text{ m}$, $1.0\text{ m}$).
- **Dual View Modes:**
  - **Top-Down 2D Architectural Plan:** For rapid wall sketching and object alignment.
  - **3D Isometric CAD View:** For spatial awareness and visual validation.

### 4.2 Agent-Based Modeling (ABM) Entities
Every simulation element is treated as an autonomous agent with distinct properties:

1. **Emitter Agent (WiFi Router / Access Point):**
   - Transmit power (default: $20\text{ dBm} / 100\text{ mW}$).
   - Frequency band toggle: $2.4\text{ GHz}$ (better penetration) vs. $5.0\text{ GHz}$ (faster throughput, higher attenuation).
   - Antenna radiation pattern (omnidirectional standard).
2. **Obstacle / Attenuator Agents (Structural Elements):**
   - **Walls:** Concrete, Brick, Drywall, Wood, Metal.
   - **Openings:** Wooden Doors, Glass Windows.
   - Properties: Length, thickness ($0.1\text{m} - 0.3\text{m}$), and RF attenuation coefficient (dB drop per penetration).
3. **Receiver Agents (Client Devices):**
   - Laptops, Smartphones, Smart TVs, IoT sensors.
   - Live telemetry: Displays real-time RSSI (in $-\text{dBm}$), connection link speed estimation (in $\text{Mbps}$), and signal quality tier (Excellent to Dead Zone).

### 4.3 Simulation & Analysis Engine
- **Multi-Wall Path Loss Computation:** Combines Free-Space Path Loss (FSPL) with obstacle penetration loss along direct ray vectors.
- **Discrete Iso-Band Heatmap:** Live 2D/3D planar heatmap displaying stepped RF coverage zones (no blurry gradients).
- **Dead-Zone Calculator:** Summarizes total covered area percentage vs. unserviceable dead-zone percentage.
- **Optimal Placement Advisor (Roadmap):** Suggests improved router coordinates based on registered client positions.

---

## 5. Non-Functional Requirements
- **Performance:** Maintain 60 FPS viewport navigation and sub-100ms simulation recalculation when moving agents.
- **Design Constraint:** Strictly flat design without gradients; maximum UX clarity and technical precision.
- **Portability:** 100% client-side execution; runs locally in browser without server dependencies.

---

## 6. Scope Boundaries
- **In-Scope (MVP):** Single-floor $M \times N$ layout, multi-wall attenuation, 2.4/5 GHz selection, router and client agents, flat iso-contour heatmap, real-time RSSI indicators.
- **Deferred to Later Phases:** Multi-story stairs RF bleed, complex dynamic multi-path reflection (ray tracing bounces), outdoor foliage simulation, multi-AP mesh roaming handoff.
