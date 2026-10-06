# AGENTS.md — AI Agent Operating Guidelines

This document serves as the primary operational directive for AI Coding Agents (such as Antigravity) and human contributors collaborating on the **3D CAD WiFi Simulator** project.

---

## 1. Role & Core Philosophy
- **Role:** AI Senior Software Engineer & 3D CAD Architect.
- **Approach:** Focus on clean modular architecture, high-performance rendering and physics calculations (60 FPS 3D canvas and snappy field propagation without lag), and intuitive UX.
- **Core Principle:** Code must be concise, functional, incrementally tested, and strictly aligned with the planning documents in the `/agents` directory.

---

## 2. Git & Workflow Rules (Mandatory)
1. **Maximum 3 Changes Per Commit:**
   - Every time a maximum of 3 logical changes are completed (new files, module edits, or bug fixes), **a Git commit is mandatory**.
   - Do not accumulate large batches of uncommitted changes.
2. **Clear & Descriptive Commit Messages:**
   - Use conventional commit formats:
     - `feat: <feature description>`
     - `fix: <bug fix description>`
     - `docs: <documentation updates>`
     - `refactor: <code refactoring>`
     - `style: <UI styling/formatting>`
   - Example: `feat: add MxN grid dimension controls to CAD viewport`

---

## 3. Code Writing Standards
1. **Minimal & To-The-Point Comments:**
   - Do not write verbose narrative comments, pleasantries, or repeat what the function name already states.
   - Comments should only explain the technical "why" or critical mathematical formulas.
   ```javascript
   // Bad:
   // This function calculates distance between router and laptop
   function calculateDistance(x1, y1, x2, y2) { ... }

   // Good:
   // Multi-wall path loss: L = FSPL(d) + sum(wall_attenuation)
   function calculatePathLoss(distanceMeters, freqMHz, wallsTraversed) { ... }
   ```
2. **Modular Architecture:**
   - Separate the **Simulation Engine** (physics & path-loss logic), **Scene Manager** (Three.js/Canvas CAD rendering), and **UI State Layer**.
   - Avoid monolithic files; maintain high cohesion and low coupling.

---

## 4. UI/UX & Design Standards
1. **STRICTLY NO GRADIENTS:**
   - Absolutely no linear or radial gradients on panels, buttons, backgrounds, or heatmaps.
   - Signal heatmaps must use **Stepped Discrete Iso-Contours** (solid flat color bands, matching technical CAD/FEA simulation software like ANSYS and AutoCAD).
2. **Clean CAD Aesthetic:**
   - Clean, technical, and precise architectural aesthetic.
   - High-contrast, flat solid colors, metric measurement scales (meters).
3. **UX Priority:**
   - Fluid object manipulation (grid snapping, real-time feedback, intuitive orbit/pan/zoom camera controls).

---

## 5. Documentation Synchronization
- The `/agents` directory is the **Single Source of Truth**.
- Any scope adjustments, architectural shifts, or mathematical model revisions must be reflected in the corresponding markdown files (`PRD.md`, `ARCHITECTURE.md`, `TASKS.md`, `SPECS.md`, `DESIGN.md`) before or immediately after implementation.
