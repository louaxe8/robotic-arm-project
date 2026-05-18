# Component Purchase List
**Lou | May 2026**

---

## Priority 1 — Needed for Shoulder Prototype

### DS3235 Servo (shoulder joint)
- **What:** High-torque coreless servo, ~35 kg·cm
- **Why:** Selected in torque_calculation.md — only servo with genuine margin for the shoulder
- **Spec to confirm before buying:** Output shaft height from the bottom of the servo body — this dimension varies by manufacturer and is needed before modeling the servo pocket in CAD
- **Voltage:** Check your specific unit — some run 4.8–6V, some 6–8.4V. Get the datasheet page from the seller.
- **Horn:** Buy with 25T spline horn included (most listings include this — verify)
- **Where to buy:** AliExpress (cheapest, 2–4 weeks), Amazon (faster)
- **Approx cost:** €10–20

### External Power Supply for Servo
- **What:** 6V DC power supply, minimum 3A (5A preferred for headroom)
- **Why:** ESP32 cannot power the DS3235 — it draws 1–3A under load. USB power will collapse.
- **Recommended:** 6V 5A DC wall adapter with 5.5mm barrel jack, OR adjustable bench power supply (more flexible for future work)
- **Note:** If you get a bench supply, it will serve you for the entire project. Worth the investment.
- **Approx cost:** €15–30 (wall adapter) / €40–80 (bench supply)

### Capacitor — Servo Power Stability
- **What:** 1000µF electrolytic capacitor, 10V or 16V rating
- **Why:** Servos draw current in spikes when they move. Without a capacitor on the power rail, the voltage drops momentarily and can reset the ESP32 or cause jitter. Place it across V+ and GND close to the servo connector.
- **Where:** Any electronics shop (Mouser, LCSC, AliExpress)
- **Approx cost:** <€1

---

## Priority 2 — Connectors and Wiring

### Jumper Wires
- **What:** Male-to-male and male-to-female dupont jumper wires, 20cm
- **Why:** Prototyping on breadboard
- **Note:** You probably have some already. If not, get an assorted pack.
- **Approx cost:** €3–5

### Breadboard
- **What:** Standard 830-point breadboard
- **Why:** Clean prototyping without soldering
- **Approx cost:** €3–5

---

## Priority 3 — Mechanical Hardware (order when ready to build)

### M3 Hardware
- **What:** M3 × 8mm screws, M3 × 12mm screws, M3 nuts, M3 heat-set inserts (for PLA)
- **Why:** All fasteners on the arm will be M3 (servo mounts, bracket joints, cover)
- **Recommended:** Get an M3 assortment kit — saves ordering multiple times
- **Approx cost:** €8–15 for a full kit

### M8 Support Axle
- **What:** M8 × 50mm stainless steel bolt (or smooth rod), M8 nut, M8 washers
- **Why:** Support axle on the non-servo side of the shoulder joint, carries bending load
- **Note:** Do not order until the bracket design is finalized — the exact length depends on cheek thickness and hub geometry
- **Approx cost:** <€5

### Bearings (optional at this stage)
- **What:** 8mm ID flanged bearings (608 or similar) for the support axle bore
- **Note:** Decide during detailed CAD whether to use a bearing or a plain M8 bore. Order after the bracket is modeled.

---

## Already Have ✅
- ESP32 dev board
- MG90S servo (learning/testing)
- Arduino IDE

---

## Order Sequence (recommended)

1. **Now:** DS3235 + 6V power supply + capacitor (long lead time if AliExpress)
2. **When starting electronics seriously:** breadboard + jumper wires if not already available
3. **When CAD is finalized:** M3 hardware kit + M8 axle parts
4. **When bracket is modeled:** bearings (if chosen)
