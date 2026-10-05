---
trigger: always_on
description: WiFi & Electromagnetic Wave Physics, Mathematical Models, and Material Attenuation Matrix
---

# SPECS.md — WiFi & Electromagnetic Wave Domain Specifications

This document defines the physics, mathematical models, RF parameters, and material attenuation benchmarks used by the **3D CAD WiFi Simulator**.

---

## 1. Core Physics & RF Fundamentals

### 1.1 Why WiFi Location Matters
Electromagnetic waves in the RF spectrum undergo three fundamental phenomena when traveling indoors:
1. **Free-Space Dispersion:** Sinyal melemah seiring kuadrat jarak (Inverse-Square Law).
2. **Material Absorption (Penetration Loss):** Gelombang diserap oleh molekul material (terutama air dan kepadatan massa pada beton/bata), mengubah energi RF menjadi panas mikroskopis.
3. **Frequency-Dependent Attenuation:** Semakin tinggi frekuensi gelombang ($5\text{ GHz}$ vs $2.4\text{ GHz}$), semakin pendek panjang gelombangnya ($\lambda$), sehingga semakin sulit menembus partikel padat dan semakin cepat teredam.

### 1.2 Frequency Comparison Table
| Parameter | 2.4 GHz Band | 5.0 GHz Band | 6.0 GHz (WiFi 6E) |
| :--- | :--- | :--- | :--- |
| **Wavelength ($\lambda = c/f$)** | $\approx 12.5\text{ cm}$ | $\approx 6.0\text{ cm}$ | $\approx 5.0\text{ cm}$ |
| **Indoor Penetration** | Strong (penetrates 2-3 walls) | Moderate (loses ~50% per solid wall) | Weak (best for line-of-sight) |
| **Channel Bandwidth** | $20\text{ MHz}$ (congested) | $40 / 80 / 160\text{ MHz}$ (wide) | Up to $160\text{ MHz}$ (clean) |
| **Max Practical Speed** | $\approx 150 - 300\text{ Mbps}$ | $\approx 800 - 1300\text{ Mbps}$ | $\approx 1800+\text{ Mbps}$ |

---

## 2. Mathematical Propagation Models

### 2.1 Free Space Path Loss (FSPL)
For an unobstructed direct path over Euclidean distance $d$ (in meters) and frequency $f$ (in MHz):

$$\text{FSPL}(d, f) = 20 \log_{10}(d) + 20 \log_{10}(f) - 27.55$$

*Example Constants:*
- At $2.4\text{ GHz}$ ($f = 2400\text{ MHz}$): $\text{FSPL}(d) \approx 40.04 + 20 \log_{10}(d)\text{ dB}$
- At $5.0\text{ GHz}$ ($f = 5000\text{ MHz}$): $\text{FSPL}(d) \approx 46.42 + 20 \log_{10}(d)\text{ dB}$

### 2.2 Multi-Wall Cost231 / Motley-Keenan Model
In real residential buildings, signals pass through multiple walls. The total path loss ($\text{PL}$) is calculated as:

$$\text{PL}(d) = \text{FSPL}(d, f) + \sum_{i=1}^{k} \left( W_i \cdot \alpha_i \right)$$

Where:
- $k$ = Total number of obstacle types intersected along the ray line.
- $W_i$ = Number of walls of material type $i$ traversed.
- $\alpha_i$ = Empirical attenuation coefficient for material $i$ in $\text{dB}$.

### 2.3 Received Signal Strength (RSSI) Equation
The final signal power reaching a client device or probe sensor is:

$$\text{RSSI} (\text{dBm}) = P_{\text{tx}} + G_{\text{tx}} - \text{PL}(d) + G_{\text{rx}}$$

Where:
- $P_{\text{tx}}$: Router Transmit Power (typically $+20\text{ dBm} = 100\text{ mW}$).
- $G_{\text{tx}}$: Router Antenna Gain (typically $+3\text{ dBi}$).
- $G_{\text{rx}}$: Client Antenna Gain (typically $0\text{ dBi}$ for mobile/laptop).

---

## 3. Material Attenuation Database (Empirical Standards)

Standard attenuation losses measured across international wireless benchmarks (ITU-R P.1238 & NIST studies):

| Obstacle Material | Thickness (Typical) | Attenuation @ 2.4 GHz | Attenuation @ 5.0 GHz | CAD Visual Color |
| :--- | :--- | :--- | :--- | :--- |
| **Reinforced Concrete** | $15 - 20\text{ cm}$ | $14.0\text{ dB}$ | $22.0\text{ dB}$ | `#718096` |
| **Red Brick Wall** | $12 - 15\text{ cm}$ | $8.0\text{ dB}$ | $14.0\text{ dB}$ | `#C25E40` |
| **Drywall / Gypsum** | $10\text{ cm}$ | $3.0\text{ dB}$ | $5.0\text{ dB}$ | `#CBD5E1` |
| **Solid Wood / Timber**| $5 - 10\text{ cm}$ | $4.0\text{ dB}$ | $7.0\text{ dB}$ | `#A2714B` |
| **Interior Wooden Door**| $4\text{ cm}$ | $2.5\text{ dB}$ | $4.0\text{ dB}$ | `#855836` |
| **Window Glass (Standard)**| $0.6\text{ cm}$| $2.0\text{ dB}$ | $3.5\text{ dB}$ | `#60A5FA` |
| **Low-E Coated Glass** | $0.8\text{ cm}$ | $8.0\text{ dB}$ | $12.0\text{ dB}$ | `#38BDF8` |
| **Metal Door / Sheet** | $0.2 - 0.5\text{ cm}$| $28.0\text{ dB}$ | $35.0\text{ dB}$ | `#475569` |

---

## 4. Signal Quality Tiers & Performance Estimation

Assuming a typical indoor thermal noise floor of $-95\text{ dBm}$:

| RSSI Range | Quality Tier | Signal-to-Noise Ratio (SNR) | Estimated Link Speed | Real-World Experience |
| :--- | :--- | :--- | :--- | :--- |
| $\ge -50\text{ dBm}$ | **Excellent** | $> 45\text{ dB}$ | $100\%$ Max Capacity | Max speed, ultra-low jitter, ideal for cloud gaming |
| $-51\text{ to } -65\text{ dBm}$ | **Good** | $30 - 44\text{ dB}$ | $75\% - 90\%$ Capacity | Seamless 4K streaming, smooth Zoom/Teams HD calls |
| $-66\text{ to } -75\text{ dBm}$ | **Fair** | $20 - 29\text{ dB}$ | $40\% - 60\%$ Capacity | Web browsing OK; occasional video drops under load |
| $-76\text{ to } -85\text{ dBm}$ | **Poor** | $10 - 19\text{ dB}$ | $10\% - 25\%$ Capacity | Frequent buffering, high packet loss, slow sync |
| $< -85\text{ dBm}$ | **Dead Zone** | $< 10\text{ dB}$ | $0\text{ Mbps}$ (Unusable) | Device disconnects or repeatedly fails handshake |

---

## 5. Geometric Ray Intersection Algorithm
To evaluate wall penetrations between Emitter $E(x_1, y_1)$ and Receiver $R(x_2, y_2)$ against a Wall segment $W$ from $P_1(x_3, y_3)$ to $P_2(x_4, y_4)$:

$$\vec{r} = R - E, \quad \vec{s} = P_2 - P_1$$

Intersection occurs if and only if there exist scalar parameters $t, u \in [0, 1]$ satisfying:

$$t = \frac{(P_1 - E) \times \vec{s}}{\vec{r} \times \vec{s}}, \quad u = \frac{(P_1 - E) \times \vec{r}}{\vec{r} \times \vec{s}}$$

When $\vec{r} \times \vec{s} \neq 0$ and $0 \le t \le 1$ and $0 \le u \le 1$, the ray passes through the wall segment, triggering the addition of that wall's attenuation $\alpha_i$ to the path loss.
