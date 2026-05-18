# CAD Session 1 — Block Layout Only
**Lou | May 2026**

**Goal:** Verify the mechanical architecture — proportions, axis alignment, clearances, and spacing. No detail, no holes, no fillets. If something doesn't fit at this stage, fix it now before committing to a detailed model.

---

> ⚠️ **WARNING — Do not finalize the DS3235 pocket dimensions or bolt hole positions until you have the exact servo measurements from a datasheet AND have the physical servo in hand. DS3235 clones vary between manufacturers. Model the servo as a plain block for now. All pocket/hole geometry comes later.**

---

## Checklist

### 1 — Base Box
- [ ] Extrude a solid block: **150 mm (W) × 180 mm (D) × 70 mm (H)**
- [ ] No internal features, no fillets, no holes — solid block only
- [ ] Confirm it fits the print volume (256 × 256 × 256 mm) ✓

---

### 2 — U-Bracket (rough block)
- [ ] Add a simple U-bracket on top of the base — three rectangular blocks forming a U-shape (base plate + two vertical arms)
- [ ] Bracket base plate: ~100 mm (W) × 60 mm (D) × 8 mm thick, centered on the base top face
- [ ] Each arm: ~60 mm tall × 10 mm thick — these are placeholder dimensions, not final
- [ ] Inner spacing between arms: leave as a variable for now (see step 5 below)
- [ ] No servo pocket, no bore, no screw holes yet
- [ ] Confirm the bracket sits flat on the base top face and doesn't overhang the footprint

---

### 3 — DS3235 Placeholder Block
- [ ] Create a simple rectangular block representing the DS3235 body: **54 × 54 × 36 mm**
- [ ] Place it flush against the inner face of the servo-side bracket arm
- [ ] Position the block so its output shaft centerline is at an **approximate mid-height of the bracket arms** — use this as a working assumption only
- [ ] Mark or note the shaft centerline position as a reference axis for Session 1
- [ ] **Do not model the servo pocket or mounting holes yet**

> ⚠️ **Note:** In the real DS3235, the output shaft is **not necessarily at the center of the servo body.** The exact shaft height varies by manufacturer. The position used in this block model is approximate and for layout purposes only. Do not use it to set the rotation axis height in the detailed model — that dimension must come from the physical servo or its datasheet.

---

### 4 — Shoulder Rotation Axis
- [ ] Create a **reference axis** (or centerline sketch) running horizontally through both bracket arms at the DS3235 shaft centerline height
- [ ] This axis must be:
  - Horizontal (parallel to the base top face)
  - Perpendicular to the front face of the base
  - At equal height on both the servo side and the support side
- [ ] Visually confirm the axis passes cleanly through both arms with no offset

---

### 5 — U-Bracket Inner Spacing Check
- [ ] The inner gap between bracket arms must fit: **Link 1 hub (servo side) + servo horn thickness + spacer/washer + Link 1 hub (support side)**
- [ ] Rough estimate of stack:
  - Servo horn thickness: ~5–8 mm
  - Link 1 hub flange (each side): ~8–10 mm
  - Washers/spacers: ~2–3 mm total
  - Clearance (link rotating freely): ~1–2 mm per side
  - **Estimated total inner gap needed: ~30–40 mm minimum**
- [ ] Adjust bracket arm inner spacing accordingly — not just "servo body width + clearance"
- [ ] Update the bracket model to reflect this spacing before moving on

---

### 6 — Link 1 Placeholder Beam
- [ ] Model Link 1 as a **solid rectangular beam: 25 × 25 × 150 mm**
- [ ] Position it between the bracket arms, centered on the rotation axis
- [ ] One end of the beam sits at the rotation axis (shoulder); the other end extends 150 mm forward (toward where the elbow will be)
- [ ] No hub geometry, no wire channel, no hollowing yet

---

### 7 — Support Side Placeholder
- [ ] On the support-side bracket arm, add a **simple 8 mm cylinder** passing through the arm and into the Link 1 beam end — this represents the M8 bolt axle
- [ ] No threads, no nut, no washer geometry yet
- [ ] Confirm the cylinder centerline is exactly on the rotation axis from step 4

---

### 8 — Axis Alignment Check ✓
- [ ] Zoom in and verify: **DS3235 shaft centerline = support axle centerline = reference axis from step 4**
- [ ] There should be zero vertical or horizontal offset between the two sides
- [ ] If they are misaligned, fix the bracket geometry before continuing — misalignment here will bind the joint under load

---

### 9 — Rotation Clearance Check ✓
- [ ] Rotate Link 1 mentally (or use SolidWorks motion/collision check) through its full intended range
- [ ] Planned range: approximately **-30° to +150°** from horizontal (full swing upward and slightly below horizontal)
- [ ] Check that Link 1 does not hit the base box at any point in this range
- [ ] If it clips the base: either raise the rotation axis height, widen the bracket, or reduce the base height
- [ ] Check the back end of the beam (shoulder end) does not clip the bracket arms during full upward swing

---

### 10 — Sanity Review Before Saving
- [ ] All placeholder dimensions are within the 256 × 256 × 256 mm print volume individually
- [ ] The rotation axis is at a sensible height — Link 1 clears the base box at all rotation angles
- [ ] The U-bracket inner spacing accommodates the full hub + horn + spacer stack (step 5)
- [ ] The DS3235 block sits fully inside or flush with the bracket arm — not protruding awkwardly
- [ ] Save the assembly as `arm_assembly_v1_BLOCKMODEL.SLDASM` — keep it separate from the detailed model

---

## What Comes Next (Session 2+)

Only after this block layout passes all checks:
- Add DS3235 pocket to servo-side bracket arm (after measuring the physical servo)
- Add M8 bore and bearing seat to support-side arm
- Add hub geometry and horn bolt pattern to Link 1
- Add base internal features (ESP32 tray, ballast pockets, access cover, cable slot)
- Add fillets, ribs, and wall thinning throughout
