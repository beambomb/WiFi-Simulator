---
trigger: always_on
description: WiFi & Electromagnetic Physics, FSPL Formulas, and Wall Attenuation Standards
---

# WiFi & Electromagnetic Wave Physics

## 1. Propagation Models
- **Free Space Path Loss (FSPL):**
  $$\text{FSPL}(d, f) = 20\log_{10}(d) + 20\log_{10}(f) - 27.55$$
  Where $d$ in meters, $f$ in MHz ($2400\text{ MHz}$ or $5000\text{ MHz}$).
- **Motley-Keenan Multi-Wall Model:**
  $$\text{PL}(d) = \text{FSPL}(d, f) + \sum_{i=1}^{k} (W_i \cdot \alpha_i)$$
- **RSSI Calculation:**
  $$\text{RSSI} = P_{\text{tx}} + G_{\text{tx}} - \text{PL}(d)$$

## 2. Material Attenuation Database ($\text{dB}$)
- Concrete: $14.0\text{ dB}$ (2.4 GHz) / $22.0\text{ dB}$ (5.0 GHz)
- Brick: $8.0\text{ dB}$ (2.4 GHz) / $14.0\text{ dB}$ (5.0 GHz)
- Drywall: $3.0\text{ dB}$ (2.4 GHz) / $5.0\text{ dB}$ (5.0 GHz)
- Wood: $4.0\text{ dB}$ (2.4 GHz) / $7.0\text{ dB}$ (5.0 GHz)
- Wooden Door: $2.5\text{ dB}$ (2.4 GHz) / $4.0\text{ dB}$ (5.0 GHz)
- Glass Window: $2.0\text{ dB}$ (2.4 GHz) / $3.5\text{ dB}$ (5.0 GHz)
- Metal: $28.0\text{ dB}$ (2.4 GHz) / $35.0\text{ dB}$ (5.0 GHz)
