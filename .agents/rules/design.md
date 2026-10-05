---
trigger: always_on
description: UI/UX & 3D CAD Design System, Flat Palette, and Zero Gradients Rules
---

# DESIGN.md — UI/UX & 3D CAD Design System

This document outlines the visual design system, color palette, typography, and interaction patterns for the **3D CAD WiFi Simulator**.

---

## 1. Design Philosophy
- **Precision CAD Aesthetic:** Inspired by modern architectural CAD software (AutoCAD, Revit, Blender Archimesh) engineered into a lightweight, high-performance web application.
- **Flat & Clean (Strictly Zero Gradients):** All visual components utilize flat, solid colors. No gradients, no noisy blurs, no distracting glowing effects.
- **Data-Driven Visual Clarity:** Signal metrics, wall attenuation values, and spatial coordinates must be immediately readable at a glance.

---

## 2. Color Palette (Flat Solid Palette)

### A. Workspace & UI Surfaces
| Element | Hex Code | Purpose |
| :--- | :--- | :--- |
| **Canvas Background** | `#1A1D24` | 3D CAD Viewport dark background |
| **Grid Lines (Major)** | `#2E3646` | Primary 1.0m grid lines |
| **Grid Lines (Minor)** | `#222834` | Secondary 0.25m subdivision grid lines |
| **Panel Surface** | `#20252F` | Toolbars, sidebars, and floating inspectors |
| **Panel Border** | `#343D4F` | 1px solid structural component borders |
| **Text Primary** | `#F1F5F9` | Titles, measurements, key numeric values |
| **Text Secondary** | `#94A3B8` | Labels, metric units (`m`, `dBm`, `GHz`), hints |
| **Accent / Selection** | `#3B82F6` | Active tools, selected object bounding boxes |

### B. Obstacle Material Agents (Solid Flat Material Colors)
Each obstacle agent has a distinctive solid flat color across both 2D floor plans and 3D extruded views:

| Material Agent | Solid Color | Physical / Attenuation Characteristics |
| :--- | :--- | :--- |
| **Reinforced Concrete** | `#718096` | Solid dark gray; very high RF attenuation (~12 to 18 dB) |
| **Red Brick** | `#C25E40` | Solid terracotta brick; high RF attenuation (~6 to 10 dB) |
| **Drywall / Gypsum** | `#CBD5E1` | Solid light gray; moderate attenuation (~2 to 4 dB) |
| **Solid Wood** | `#A2714B` | Solid timber brown; moderate attenuation (~3 to 5 dB) |
| **Wooden Door** | `#855836` | Solid dark walnut with hinge indicator (~3 dB) |
| **Clear Glass Window**| `#60A5FA` | Solid light blue (60% opacity, zero gradient) (~2 dB) |
| **Metal Sheet** | `#475569` | Solid slate; near-total reflection / blockage (~25+ dB) |

### C. Interior Furniture Agents (Solid Flat Object Colors)
| Furniture Agent | Solid Color | Visual CAD Appearance & Material Representation |
| :--- | :--- | :--- |
| **Refrigerator / Metal Appliance** | `#64748B` | Solid metallic cool slate; high specular reflection (R ~ 0.90) |
| **Full-Length Mirror** | `#93C5FD` | Solid ice cyan; RF reflective mirror (R ~ 0.85) |
| **Fish Aquarium / Water Jug** | `#0284C7` | Solid deep ocean blue; extreme dielectric absorption |
| **Wardrobe / Clothes Closet** | `#B45309` | Solid dark amber wood; heavy RF absorption |
| **Sofa / Upholstered Bed** | `#6B7280` | Solid warm gray textile; mild attenuation |

### D. Signal Heatmap (Stepped Discrete Iso-Bands)
**Critical Directive:** No smooth gradient interpolation. Signal distribution is rendered as distinct, stepped iso-contour bands matching engineering field analysis tools:

| Signal Level (RSSI) | Link Quality | Solid Flat Color | Real-World User Impact |
| :--- | :--- | :--- | :--- |
| $\ge -50\text{ dBm}$ | **Excellent** | `#10B981` (Emerald) | Flawless 4K/8K streaming, ultra-low ping gaming |
| $-51\text{ to } -65\text{ dBm}$ | **Good** | `#3B82F6` (Blue) | Fast downloads, seamless HD video conferencing |
| $-66\text{ to } -75\text{ dBm}$ | **Fair** | `#F59E0B` (Amber) | Standard browsing; potential latency under load |
| $-76\text{ to } -85\text{ dBm}$ | **Poor** | `#EF4444` (Red) | Noticeable buffering, packet drops, weak link |
| $< -85\text{ dBm}$ | **Dead Zone** | `#1F2937` (Dark Gray) | Disconnected / connection drops completely |

---

## 3. Typography & Numerical Formatting
- **Font Stack:** Clean monospace/system sans-serif (`Inter`, `Segoe UI`, or `JetBrains Mono` for spatial coordinates and dBm values).
- **Metric Formatting:** Every dimension and RF value must explicitly show standard SI units:
  - Floor Size: `12.0 m × 8.0 m`
  - Wall Thickness: `0.15 m` (15 cm)
  - Signal Level: `-58 dBm`
  - Frequency Band: `2.4 GHz` / `5.0 GHz` / `6.0 GHz`
  - Estimated Throughput: `350 Mbps`

---

## 4. UI Layout & Viewport Hierarchy

```
+-------------------------------------------------------------------------------+
| TOP BAR: [Project Title] | Space: [ 12.0 ] x [ 8.0 ] m | View: [ 3D CAD | 2D Plan ] |
+-------------------------------------------------------------------------------+
| TOOLBAR   | 3D CAD INTERACTIVE VIEWPORT                  | PROPERTY INSPECTOR |
| [Select]  |                                              | [Router Agent #1]  |
| [Router]  |  +----------------------------------------+  | - Tx Power: 20 dBm |
| [Wall]    |  |               (Router)                 |  | - Band: 5 GHz      |
| [Door]    |  |                 )))                    |  | - Height: 1.2 m    |
| [Window]  |  |  [Concrete]===========                 |  |                    |
| [Client]  |  |                     [Laptop] -58dBm    |  | [Coverage Stats]   |
| [Ruler]   |  +----------------------------------------+  | Coverage: 84.5%    |
| [Heatmap] |  Metric Grid (1m x 1m), X/Y/Z Axes, Dimensions | Dead Zone: 15.5%   |
+-------------------------------------------------------------------------------+
| STATUS BAR: Cursor: (X: 5.40m, Y: 3.20m) | Active Tool: Place Wall (Snap: 0.25m)|
+-------------------------------------------------------------------------------+
```

---

## 5. User Experience (UX) & Interaction Principles
1. **Intelligent Grid Snapping:**
   - Walls and devices snap cleanly to 0.25m or 0.50m increments, ensuring architectural consistency without frustrating micro-adjustments.
2. **Two-Click Wall Drawing:**
   - Click once to anchor the wall start point; click again to set the end point. Wall length and orientation angle are displayed dynamically during drafting.
3. **Real-Time Simulation Feedback:**
   - Moving a router or wall immediately updates client device signal meters and heatmap contours without perceptible lag.
4. **Standard CAD Camera Controls:**
   - **Scroll Wheel:** Zoom in / Zoom out toward cursor position.
   - **Right Click + Drag:** 3D Orbit / Perspective rotation.
   - **Middle Click (or Shift + Left Click) + Drag:** Pan viewport.
   - **Spacebar / Hotkey:** Instant toggle between Top-Down 2D Floor Plan and 3D Isometric View.
