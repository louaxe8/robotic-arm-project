# CAD Design Brief — Base & Shoulder Pitch Joint
**Lou | May 2026**

---

## Context & Constraints

| Parameter | Value |
|---|---|
| Print volume | 256 × 256 × 256 mm (Bambu Lab P2S) |
| Layer orientation | Parts should be oriented to maximize Z-strength at stress points |
| Material | PLA (prototype) |
| Print tolerance (fits) | 0.2–0.4 mm clearance for servo pockets and rotating fits |
| Link 1 length (L1) | 150 mm |
| Link 2 length (L2) | 130 mm |
| Shoulder servo | DS3235 (coreless, ~35 kg·cm) |
| Learning / test servo | MG90S (PWM test only, not load-bearing) |

---

## Design Principles (from research)

1. Servo shaft must NOT carry full mechanical load — dual-side joint support required.
2. Reserve space for bearing or bolt-axle support on the non-servo side of each joint.
3. Wiring: external/semi-external with open channels and slack loops at each joint.
4. No thin flat links — use box cross-section or ribbed profiles.
5. Screw holes: minimum 3–4 mm wall thickness around any hole.
6. Print tolerances: 0.2–0.4 mm for servo pockets and rotating fits.

---

## Kinematic Clarification — v1 Joint Layout

**Joint 1 — Shoulder pitch:** rotates around a **horizontal axis**, lifting Link 1 up and down against gravity. This is the only joint in v1 that is physically built.

**Joint 2 — Elbow pitch:** also rotates around a **horizontal axis**, bending the forearm relative to the upper arm. Simulated in FK/IK now; built in the next phase.

**Base yaw (waist rotation):** rotates around a **vertical axis**, spinning the whole arm left/right. This is a natural addition when scaling to 5–6DOF, but is **not part of v1**. See the Future Joints section at the end of this document.

The v1 base is a **fixed, stable box**. It does not rotate. The shoulder U-bracket sits rigidly on top of it.

---

## Part 1 — Base

### Function
- Anchor the entire arm rigidly to the table
- House the ESP32 and power electronics
- Provide a stable, tip-resistant footprint
- Mount the shoulder U-bracket on top via 4× M3/M4 bolts

### Target Dimensions

| Feature | Dimension | Reasoning |
|---|---|---|
| Footprint (W × D) | 150 × 180 mm | Wider front-to-back than side-to-side; arm reaches forward, not sideways |
| Height | 60–80 mm | Enough for ESP32 + wiring + access cover |
| Wall thickness | 3–4 mm minimum | PLA structural minimum; thicker near screw bosses |
| Top plate thickness | 5–6 mm | Must handle shoulder reaction forces |
| Corner radius (exterior) | 5–8 mm | Reduces stress concentration, easier to print |

### Internal Layout (top view)

```
  ┌─────────────────────────────┐  ← Top plate (5–6 mm thick)
  │  [4× M3 boss — U-bracket]  │  ← Shoulder U-bracket mounts here
  │                             │
  │  [ESP32 tray]   [wires]     │  ← ESP32 footprint: ~52 × 28 mm
  │                             │
  │  [Ballast pockets]          │  ← 2–4 × M8 nut recesses in base floor
  │                             │
  └─────────────────────────────┘  ← Bottom plate
           ↑ removable access cover on one side wall
```

### Features to Model

- [ ] **Outer shell** — rectangular box body with rounded corners
- [ ] **Top plate** with 4× M3 or M4 tapped/boss holes for shoulder U-bracket mounting (no center bore needed in v1 — that was for yaw, not pitch)
- [ ] **ESP32 tray** — snap-fit or 2-screw tray on interior wall. ESP32 footprint ≈ 52 × 28 mm; keep 2 mm clearance each side
- [ ] **Ballast pockets** — 2–4 recesses for M8 hex nuts or metal weights in the base floor, toward the rear (counterbalances the arm reaching forward)
- [ ] **Cable entry slot** — 10 × 5 mm slot on the front or top plate for servo cable routing up to the shoulder
- [ ] **Access cover** — one removable side panel held by 2× M3 screws
- [ ] **Rubber feet pockets** — 4 corner recesses, 10 mm diameter × 2 mm deep, for adhesive rubber feet

---

## Part 2 — Shoulder Pitch Joint

### Function
- Rotate Link 1 (upper arm) in the **vertical plane**, lifting it up and down against gravity
- Rotation axis is **horizontal**, parallel to the table surface
- DS3235 drives the link from one side; an M8 bolt axle or bearing supports the other side
- Neither the servo shaft nor the printed bracket alone carries the full load — it is shared across both sides

### Corrected Joint Architecture

The joint uses a **U-bracket** bolted to the base top plate. Link 1 sits between the two arms of the U-bracket and rotates on a shared horizontal axle.

**Side view — shoulder pitch motion:**

```
                          Link 1 (pitches up/down)
                         ┌──────────────────────────────►
                         │
      ────────────────── ● ──────────────────  ← horizontal rotation axis
                         │
              ┌──────────┴──────────┐
              │    U-bracket body   │
              └──────────┬──────────┘
              ┌──────────┴──────────┐
              │   BASE TOP PLATE    │
              └─────────────────────┘
              ┌─────────────────────┐
              │       BASE BOX      │
              │  [ESP32]  [ballast] │
              └─────────────────────┘
```

**Front view — dual-side support:**

```
   DS3235 side                        Support side
   (servo body fixed                  (M8 bolt axle
    to bracket arm)                    or 608 bearing)
        │                                   │
   ┌────┴────┐                         ┌────┴────┐
   │ bracket │                         │ bracket │
   │  arm    │──────[ Link 1 hub ]─────│  arm    │
   └────┬────┘         ▲               └────┬────┘
        │        rotation axis               │
        └──────────────┬────────────────────┘
                       │  U-bracket base
              ┌────────┴────────┐
              │  BASE TOP PLATE │
              └─────────────────┘
```

**How it works:**
- The DS3235 servo body is screwed rigidly into one arm of the U-bracket (servo does NOT move).
- The servo horn is bolted to the hub on the Link 1 side facing the servo. When the servo drives, the horn rotates and takes Link 1 with it.
- The opposite end of Link 1's hub passes through the other bracket arm and is supported by an M8 bolt axle (v1) or 608 bearing (v2 upgrade). This side carries the bending load, not the servo shaft.
- Link 1 rotates freely between the two bracket arms around the horizontal axis.

### Key Dimensions

| Feature | Dimension | Notes |
|---|---|---|
| Link 1 length | 150 mm | FK dimension; measured from shoulder axis to elbow axis |
| Link cross-section | 25 × 25 mm box | Minimum for stiffness; 30 × 30 if in doubt |
| Link wall thickness | 3 mm | Hollow box = light + stiff |
| U-bracket arm spacing (inner) | ~50–60 mm | Must fit DS3235 body width + 2 mm clearance each side |
| U-bracket arm thickness | 5–6 mm | Load-bearing; do not go thinner |
| U-bracket base plate | 5 mm thick | Bolts to base top plate with 4× M3/M4 |
| DS3235 body footprint | ~54 × 54 × 36 mm | **Measure your specific unit before modeling** |
| DS3235 output shaft | 25T spline | Check your specific horn interface |
| Servo horn bolt | M3 × 6 mm | Center screw into servo horn |
| Support-side bore | 8.3–8.4 mm (for M8 axle) | Sliding fit: add 0.3–0.4 mm to nominal |
| Rotation axis height above base | ~80–100 mm | High enough for Link 1 to swing without hitting the base |

### Features to Model

**U-bracket (one part):**
- [ ] **Base plate** — flat plate, 4× M3/M4 clearance holes, bolts to base top plate
- [ ] **Servo-side arm** — vertical wall with DS3235 pocket (body seated flush) and 4× servo mounting M3 holes
- [ ] **Support-side arm** — vertical wall with 8.3 mm through-bore (M8 axle) or 22 mm pocket (608 bearing)
- [ ] **Servo cable slot** — 8 × 4 mm slot in servo-side arm for cable exit

**Shoulder link — Link 1 (one part):**
- [ ] **Hub — servo side** — boss that mates with DS3235 horn. Center bore matches horn shaft. 4× M3 holes matching horn bolt pattern. This is what the servo drives.
- [ ] **Hub — support side** — matching boss with 8 mm through-bore for M8 axle, or step for bearing seat
- [ ] **Link body** — 150 mm hollow box beam (25 × 25 mm, 3 mm walls) extending from the hub toward the elbow
- [ ] **Wire channel** — 10 × 5 mm groove along the top face of the link for routing the elbow servo cable
- [ ] **Elbow interface** — flat end face with 4× M3 holes for elbow joint bracket (design this in Phase 2)

### Assembly Sequence (mental model before CAD)

1. Base box complete with ESP32 tray, ballast, and access cover.
2. U-bracket bolted to base top plate with 4× M3/M4 screws.
3. DS3235 servo seated and screwed into servo-side arm of U-bracket.
4. Servo horn pressed onto servo output shaft and secured with center M3 bolt.
5. Link 1 hub (servo side) slid over the horn and bolted to the horn with 4× M3 screws.
6. Link 1 hub (support side) inserted through the support-side arm of the bracket.
7. M8 bolt threaded through the bracket arm and hub bore. M8 nut tightened with washer — snug but not binding so Link 1 rotates freely.
8. Test: Link 1 should swing freely with no wobble. If it binds, ease the M8 nut slightly.

---

## First SolidWorks Session — Recommended Order

1. **Base body** — Extrude outer shell → Shell command (3–4 mm walls) → top plate → bottom plate
2. **Base top plate bosses** — 4× M3/M4 boss features for U-bracket mounting
3. **ESP32 tray pocket** — rectangular extruded cut inside base
4. **Ballast pockets** — extruded cuts in base floor (rear half)
5. **Cable entry slot** — cut on front or top wall
6. **Access cover cutout** — one open face + separate cover part with 2× M3 screw posts
7. **U-bracket** — new part: base plate → servo-side arm (with DS3235 pocket) → support-side arm (with bore)
8. **Link 1** — new part: servo-side hub boss → link body (extrude 150 mm) → shell → support-side hub bore → wire channel
9. **Assembly** — mate all 4 parts, verify Link 1 swings freely around horizontal axis

---

## Open Questions to Decide Before Modeling

| Question | Options | Suggested Default |
|---|---|---|
| Support-side axle | M8 bolt vs. 608 bearing | M8 bolt for v1 (simpler, upgradeable later) |
| Link cross-section | 25×25 vs. 30×30 mm | 25×25 for light prototype |
| U-bracket | Single printed part vs. two separate arms | Single U-bracket (stiffer, fewer joints) |
| Access cover retention | M3 screws vs. snap clips | M3 screws (more reliable in PLA) |
| Ballast placement | Base floor rear vs. base floor center | Rear (counterbalances arm reaching forward) |

---

## Files to Create in SolidWorks

| File | Type | Notes |
|---|---|---|
| `arm_base.SLDPRT` | Part | Main base body |
| `arm_base_cover.SLDPRT` | Part | Removable access panel |
| `shoulder_ubracket.SLDPRT` | Part | U-bracket with servo pocket + support bore |
| `shoulder_link1.SLDPRT` | Part | Link 1 beam + hub (both sides) |
| `arm_assembly_v1.SLDASM` | Assembly | All 4 parts mated, verify rotation axis |

Save all to: `CAD/` folder in the project repo.

---

## Notes on Tolerances for 3D Printing

| Fit type | Clearance to add |
|---|---|
| Press fit (bearing into pocket) | −0.1 to 0 mm (interference) |
| Sliding fit (bolt axle in bore) | +0.3 to +0.4 mm over nominal |
| Servo pocket (body seated in bracket) | +0.3 mm per side |
| Screw boss (M3 self-tapping into PLA) | 2.5 mm hole |
| Screw clearance (M3 through hole) | 3.3 mm hole |
| Screw clearance (M4 through hole) | 4.3 mm hole |

Print a tolerance test piece before committing to a full build — especially for the DS3235 pocket and the M8 axle bore.

---

## Future — Base Yaw Joint (not v1)

When scaling to 5–6DOF, a base yaw joint will be added between the fixed base box and the shoulder U-bracket. This joint rotates the entire arm assembly left/right around a **vertical axis**.

At that stage the 608 bearing concept is relevant: a 22 mm bore in a rotating platform above the base, with a 608 bearing (8 mm ID, 22 mm OD, 7 mm wide) taking the radial load. A second, stronger servo (or stepper motor) drives the platform.

**Do not design for this now.** The shoulder U-bracket bolt pattern on the base top plate should be on a symmetric grid so it can be replaced with a yaw platform later without redesigning the base box.
