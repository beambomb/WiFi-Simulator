---
trigger: always_on
description: AI Agent Operating Guidelines, Git Commit Cadence, and Coding Standards
---

# AI Agent Operating Guidelines

This rule governs the behavior of AI Coding Agents working in this repository.

## 1. Git & Workflow Rules (Mandatory)
1. **Maximum 3 Changes Per Commit:**
   - Every time a maximum of 3 logical changes are completed (new files, edits, or fixes), **a Git commit is mandatory**.
   - Do not accumulate large batches of uncommitted changes.
2. **Clear & Descriptive Commit Messages:**
   - Use conventional commit formats (`feat:`, `fix:`, `docs:`, `refactor:`, `style:`, `build:`).
   - Example: `feat(backend): implement simulation CRUD endpoints`

## 2. Code Writing Standards
1. **Minimal & To-The-Point Comments:**
   - Do not write verbose narrative comments, pleasantries, or repeat function names.
   - Comments must only explain the technical "why" or critical mathematical formulas.
2. **Modular Architecture:**
   - Maintain strict separation of concerns between Backend Engine, 3D CAD Viewport, and State Management.

## 3. UI/UX & Design Standards
1. **STRICTLY NO GRADIENTS:**
   - Absolutely no linear or radial gradients on panels, buttons, backgrounds, or heatmaps.
   - Signal heatmaps must use **Stepped Discrete Iso-Contours** (solid flat color bands, matching technical CAD/FEA simulation software like ANSYS and AutoCAD).
2. **Clean CAD Aesthetic:**
   - High-contrast, flat solid colors, metric measurement scales (meters).
3. **UX Priority:**
   - Fluid object manipulation (grid snapping, real-time feedback, intuitive camera controls).
