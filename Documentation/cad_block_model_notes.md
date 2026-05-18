# CAD Block Model v1 — Notes
**Lou | May 2026**
**Assembly file:** `CAD/arm_assembly_v1_BLOCKMODEL.SLDASM`

---

## Purpose

This block model was built to verify the mechanical architecture of the shoulder joint before committing to any detailed geometry. No part of this model is intended for printing. The goal was to confirm: component placement, axis alignment, part identity (rotating vs fixed), and basic clearances.

---

## Architecture Confirmed

```
[DS3235 servo body] — outside left cheek (fixed to bracket)
        ↓
[Left U-bracket cheek] — fixed
        ↓
[Link 1 hub zone] — inside gap (rotating)
        ↓
[Right U-bracket cheek] — fixed
        ↓
[Support axle] — passes through right cheek and Link 1 (rotating axis reference)
        ↓
[Link 1 beam] — extends outward to the right (rotating)
```

**Shoulder rotation axis:** horizontal, running left-right (along X), through both cheeks at approximately mid-height of the DS3235 block. This is a pitch axis — Link 1 swings up and down.

---

## Part Status

| Part | Role | Status in Model |
|---|---|---|
| `arm_base` | Fixed base box | Fixed (f), fully defined |
| `shoulder_ubracket_block` | Fixed bracket — holds servo and support side | Fully defined via mates |
| `ds3235_placeholder` | Servo body — fixed outside left cheek | Fully defined via mates |
| `link1_block` | Rotating Link 1 — hub zone + beam | Fully defined ✅ |
| `support_axle_placeholder` | Axle reference — passes through bracket + Link 1 | Still floating (-) — acceptable for block model |

---

## Placeholder Dimensions Used

These are working dimensions for architecture verification only. All are subject to change in the detailed design.

| Component | Dimensions |
|---|---|
| Base box | 150 × 180 × 70 mm |
| U-bracket (overall) | ~100mm wide, cheeks ~60mm tall, ~10mm thick |
| U-bracket inner gap | ~50mm (needs recalculation once hub stack is known) |
| DS3235 placeholder block | 54 × 54 × 36 mm |
| Link 1 beam cross-section | 25 × 25 mm |
| Link 1 beam length | 150 mm |
| Support axle diameter | 8 mm |

---

## What Was Confirmed

- ✅ Base is fixed and stable
- ✅ U-bracket mounts correctly on top of the base
- ✅ DS3235 servo body sits outside the bracket cheek — not inside the gap
- ✅ Link 1 is a **separate rotating part** — not merged with the U-bracket
- ✅ Link 1 passes through the hub zone (inside gap) and extends outward on the support side
- ✅ Shoulder rotation axis is horizontal (pitch joint)
- ✅ Support axle passes through both cheeks and through Link 1 on the correct axis
- ✅ Visual axis alignment: DS3235 centerline, Link 1 center, support axle are approximately on the same horizontal line
- ✅ Link 1 is centered depth-wise in the U-bracket gap (Symmetric mate applied)
- ✅ Link 1 is fully constrained in the assembly

---

## Rotation Clearance Check

**Status: PENDING — must be done before Block Model v1 is declared complete.**

Planned range: **-30° to +150°** from horizontal.

To perform:
- Drag or rotate Link 1 manually in SolidWorks through its full range
- Watch specifically: does the **shoulder end** of the beam (inside the gap) clip the top of the base box when Link 1 swings upward past ~90°?
- If it clips → raise the rotation axis height or reduce base box height in a v2

Result: [✅] Pass — visually estimated from right side view. Geometry appears clear at full range.
Notes: Formal motion study not required at block model stage.

---

## What Is NOT Modeled Yet

Everything below comes in the detailed design phase, not before:

- DS3235 servo pocket geometry in the bracket cheek
- M8 bore and bearing seat in the support-side cheek
- Hub geometry (servo horn connection, bolt pattern)
- Actual shaft height on the DS3235 (varies by manufacturer — must be measured from physical servo or verified datasheet)
- Fillets and chamfers
- Shell / wall thinning
- Ribs and gussets
- Cable channels
- Base internal features (ESP32 tray, ballast pockets, access cover)
- Mounting holes of any kind

---

## Open Questions for Detailed Design

1. **DS3235 shaft exact height** — the shaft is NOT at the center of the servo body. Exact position varies by manufacturer. Must measure or get datasheet from the specific unit before modeling the pocket.
2. **U-bracket inner gap final value** — depends on the hub + servo horn + washer stack thickness. Rough estimate: 30–40mm minimum. Needs calculation once hardware is sourced.
3. **Bearing or plain bore?** — if using a bearing on the support side, the bore geometry changes. Decision pending hardware selection.
4. **Link 1 beam final length** — 150mm is a placeholder. Final length depends on the desired reach and load arm for elbow joint placement.
5. **Rotation limits** — -30° to +150° is the planned range. Will be confirmed by the clearance check and by physical stop placement in the detailed model.

---

## What to Avoid Until Detailed Design Starts

- Adding holes, pockets, fillets, threads, or bearings to any part
- Printing any part from this block model
- Ordering components based on these placeholder dimensions
- Starting the detailed model before: (a) clearance check passes, and (b) physical DS3235 dimensions are confirmed

---

## Next Step

1. Complete the rotation clearance check (see above)
2. Save 4 screenshots into `Images/` (isometric, front, right side, clearance position)
3. Declare Block Model v1 complete
4. Begin detailed shoulder joint design — starting with the U-bracket cheeks once DS3235 physical dimensions are available
