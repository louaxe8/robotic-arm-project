# Torque Calculation — 2DOF Robotic Arm
**Lou | May 2026**

---

## Purpose

This document estimates the minimum torque required at each joint of the 2DOF robotic arm. The goal is to select servos with enough margin for safe, reliable operation — and to establish a baseline before scaling toward a 5–6DOF arm.

---

## Important Assumptions

This is a **first-order static torque estimate only.**

It assumes the arm is fully extended horizontally and held still — the worst-case static position. This calculation does **not** fully account for:

- Dynamic acceleration loads (moving fast multiplies effective torque demand)
- Backlash, friction, and mechanical losses
- Fasteners, wires, servo horns, and bearings
- Wrist servo, gripper, and payload mass
- Real servo torque drop under continuous use (stall torque ≠ working torque)

**Conclusion:** The numbers below are a lower bound, not a complete picture. Always select a servo with significant margin above the calculated requirement — especially at the shoulder.

---

## Arm Dimensions & Mass Estimates

| Component | Length | Estimated Mass | Notes |
|---|---|---|---|
| Link 1 (upper arm) | 15 cm | ~120 g | Hollow PLA, motor mount included |
| Link 2 (forearm) | 13 cm | ~90 g | Hollow PLA, lighter than upper arm |
| Joint 2 servo (at elbow) | — | ~55 g | MG996R class |
| Future gripper / payload | — | ~50–100 g | Not included in first prototype, but critical for final design |

**Note on future payload:** Once a wrist servo, gripper, or any payload is added, the effective torque at the shoulder increases significantly — because that mass sits at the far end of the arm. Even a 100g gripper adds roughly 2.85 kg·cm to the shoulder (100g × 28.5cm effective distance). This must be recalculated before finalizing servo selection for any version beyond the early prototype.

---

## Joint 2 — Elbow

**What it lifts (simplified first model):** forearm (Link 2) only.

```
T2 = mass_forearm × (L2 / 2)
T2 = 0.09 kg × 6.5 cm
T2 = 0.585 kg·cm
```

**With 2.5× safety factor:**
```
T2_required = 0.585 × 2.5 = 1.46 kg·cm
```

**Important:** This simplified model only accounts for the forearm. In a more complete model — especially as the arm grows toward 5–6DOF — Joint 2 must also carry the wrist servo, wrist links, gripper, fasteners, wires, and any payload. When those are added, the elbow requirement increases substantially and MG996R may no longer be sufficient.

**For the early lightweight prototype:** MG996R (~10 kg·cm) is acceptable. It gives a large margin over the current 1.46 kg·cm requirement, with room to absorb some wiring and fastener mass.

**For a more serious 5–6DOF arm:** A stronger servo in the 15–25+ kg·cm range should be considered for the elbow as downstream mass grows.

---

## Joint 1 — Shoulder

**What it lifts:** upper arm + elbow servo + forearm (worst case: all horizontal)

```
T1 = (mass_link1 × L1/2) + (mass_elbow_servo × L1) + (mass_link2 × (L1 + L2/2))

T1 = (0.12 × 7.5) + (0.055 × 15) + (0.09 × 21.5)
T1 = 0.90 + 0.825 + 1.935
T1 = 3.66 kg·cm
```

**With 2.5× safety factor:**
```
T1_required = 3.66 × 2.5 = 9.15 kg·cm
```

This 9.15 kg·cm figure **does not include** wrist, gripper, payload, dynamic forces, or friction. In practice, the real demand is higher.

**Why MG996R is not enough for the shoulder:**
MG996R at ~10 kg·cm sits almost exactly at the calculated requirement with safety factor applied — leaving virtually no margin for the factors not included in this model. That is not a safe design choice.

**Recommendation: DS3235-class servo, ~35 kg·cm, for the shoulder joint.**

The DS3235 gives a practical safety margin of ~3.8× over the calculated static requirement, which provides genuine headroom for dynamic loads, wires, fasteners, and future wrist/gripper/payload mass. For a modular arm intended to grow toward 5–6DOF, this is the right choice.

DS3225 (~25 kg·cm) is a weaker alternative that technically passes the static calculation, but is not the preferred option here given the design intent to scale up.

---

## Servo Summary

| Joint | Static Requirement (2.5× safety) | Selected Servo | Torque | Status |
|---|---|---|---|---|
| Joint 1 (shoulder) | 9.15 kg·cm | **DS3235** | ~35 kg·cm | Preferred — large practical margin |
| Joint 2 (elbow) | 1.46 kg·cm | **MG996R** | ~10 kg·cm | Acceptable for early lightweight prototype |
| Learning / gripper | — | **MG90S** | ~2.2 kg·cm | PWM learning and basic tests only |

---

## MG90S — Where It Actually Fits

| Use Case | Suitable? |
|---|---|
| Learning PWM and servo control with ESP32 | ✅ Yes |
| Basic servo control code development | ✅ Yes |
| Very light gripper (early prototype only) | ⚠️ Marginal |
| Elbow joint on real arm | ❌ No |
| Shoulder joint | ❌ No |

**Important:** The MG90S torque rating (2.2 kg·cm) is a **stall torque** — the maximum torque before the servo stops completely. Comfortable continuous working torque is significantly lower. Do not treat the stall figure as a reliable working load.

---

## Note on Scaling to 5–6DOF

The final target for this project is a 5DOF or 6DOF arm with the following structure:

```
Base (rotation) → Shoulder → Elbow → Wrist pitch → Wrist roll → Gripper
```

**Critical point:** When scaling from 2DOF to 5–6DOF, the torque calculation must be **fully redone for every joint.** Each joint carries the mass of all downstream links, servos, gripper, and payload. The shoulder of a 6DOF arm carries far more than the shoulder of a 2DOF arm. Never assume the current numbers carry over.

The plan is to scale this one stage at a time. These calculations will be revisited at each new phase.

---

## Next Steps

- [ ] Weigh printed parts once available and update mass estimates with real measurements
- [ ] Recalculate with real masses before finalizing servo order
- [ ] **Purchase: DS3235 for shoulder joint**
- [ ] MG996R for elbow when ready to build 2DOF physically
- [ ] Keep MG90S for ESP32 PWM learning and early servo control code
- [ ] Redo full torque analysis before adding wrist / gripper / payload
