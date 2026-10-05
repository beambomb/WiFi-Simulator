# TASKS.md — Implementation Roadmap & Sprint Tracking

This document outlines the phased development plan and task checklist for building the **3D CAD WiFi Simulator**. Every milestone enforces the rules set forth in `AGENTS.md` (maximum 3 changes per commit, minimal comments, clean flat CAD styling, zero gradients).

---

## Milestone 0: Documentation & Blueprints
*Goal: Establish requirements, design system, physical specifications, and agent operational guidelines.*

- [x] Create `AGENTS.md` (Operational instructions, commit cadence, coding standards).
- [x] Create `DESIGN.md` (Zero-gradient flat palette, CAD UI/UX hierarchy, stepped iso-band rules).
- [x] Create `PRD.md` (Problem statement, user stories, MVP scope, functional requirements).
- [x] Create `ARCHITECTURE.md` (ABM hierarchy, data pipeline, proposed project folder structure).
- [x] Create `SPECS.md` (WiFi physics, FSPL formulas, multi-wall attenuation matrix, ray intersection).
- [x] Create `TASKS.md` (Roadmap, milestones, and task tracking).

---

## Milestone 1: Project Scaffolding & 3D CAD Viewport
*Goal: Initialize a lightweight development environment and render an interactive metric CAD grid.*

- [ ] Initialize project scaffolding (Vite + Three.js or lightweight WebGL).
- [ ] Implement flat dark CAD workspace styling (Zero gradients, CSS tokens from `DESIGN.md`).
- [ ] Build `CADViewport` with dual-camera support (Perspective 3D Orbit & Orthographic 2D Top-Down).
- [ ] Implement dynamic $M \times N$ metric grid renderer with 1.0m major lines and 0.25m minor subdivision lines.
- [ ] Add Room Dimension Controller modal/inputs (allow user to resize floor space $M \times N$).

---

## Milestone 2: Agent Modeling & Placement System
*Goal: Allow users to place and manipulate all simulation agents (Router, Walls, Doors, Devices) with grid snapping.*

- [ ] Implement base `Agent` entity and reactive `SceneGraphState`.
- [ ] Implement `AttenuatorAgent` (Walls):
  - [ ] Two-click wall drawing tool with length and angle readout.
  - [ ] Material selector (Concrete, Brick, Drywall, Wood, Metal) with flat color coding.
  - [ ] Openings placement (Wooden Door, Glass Window).
- [ ] Implement `EmitterAgent` (WiFi Router / AP):
  - [ ] 3D router mesh/model with omnidirectional antenna.
  - [ ] Frequency toggle (2.4 GHz vs. 5.0 GHz) and TX power adjustment (dBm).
- [ ] Implement `ReceiverAgent` (Client Devices):
  - [ ] Device icons/models (Laptop, Smartphone, Smart TV).
  - [ ] Live telemetry badge attached to device.
- [ ] Implement grid snapping ($0.25\text{ m}$ / $0.50\text{ m}$) and selection bounding boxes.

---

## Milestone 3: RF Propagation & Real-Time Calculation Engine
*Goal: Connect physical formulas to agents so moving walls or routers dynamically recalculates signal metrics.*

- [ ] Implement 2D line segment intersection algorithm (`Intersection2D.js`).
- [ ] Implement Free-Space Path Loss ($FSPL$) formula with frequency parameters (`PathLossModel.js`).
- [ ] Implement multi-wall cumulative attenuation computation (`RfEngine.js`).
- [ ] Calculate live RSSI ($-\text{dBm}$) and link speed estimates ($\text{Mbps}$) for all placed `ReceiverAgent`s.
- [ ] Display live telemetry in the right-hand Property Inspector panel.

---

## Milestone 4: Stepped Iso-Band Heatmap & Analytics
*Goal: Render flat, discrete stepped color contours of the RF field across the entire $M \times N$ floor.*

- [ ] Generate a sampling probe grid covering the $M \times N$ floor surface.
- [ ] Implement discrete stepped color band shader/texture (Zero gradients: Emerald, Blue, Amber, Red, Dark Gray).
- [ ] Build Coverage Analytics widget:
  - [ ] Percentage of floor area with Excellent/Good coverage.
  - [ ] Percentage of floor area classified as Dead Zone ($< -85\text{ dBm}$).
- [ ] Add Heatmap visibility toggle and plane height slider (floor level to table height $0.8\text{ m}$).

---

## Milestone 5: Smart Optimization & Placement Advisor
*Goal: Solve the core customer frustration by recommending the optimal router placement.*

- [ ] Implement automated grid search to evaluate candidate router locations.
- [ ] Calculate score based on maximizing client device RSSI while minimizing dead zones.
- [ ] Add "Suggest Optimal Router Position" button with visual indicator of ideal placement.
- [ ] Provide export/save floor plan feature (JSON configuration).
