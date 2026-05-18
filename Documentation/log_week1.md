# Week 1 Log

---

## Day 1

### What did I do?
I wrote my first Forward Kinematics code for a 2DOF robotic arm.
The code calculates the end-effector position from two joint angles and link lengths.
I also added plots for the arm position and the full workspace.

### What did I understand well?
I understood how theta1 and theta2 affect the final x,y position of the arm.
I also understood that the workspace is the visualization of all the possible angles positions created by checking many angle combinations.

### What is still unclear?
I still need to better understand how to connect the math to the real physical arm dimensions and servo limits.

---

## Day 2

### What did I do?
I started the CAD phase of the project. Before opening SolidWorks, I prepared two reference documents:
- A full CAD design brief covering the base box and shoulder pitch joint architecture, including dimensions, design principles, servo selection, and tolerance guidelines.
- A CAD Session 1 checklist — a scoped block layout guide with no detail geometry, only blocks to verify the mechanical architecture.

I then opened SolidWorks and built the Session 1 block model step by step:
1. Base box: 150 × 180 × 70 mm solid block, centered on the origin.
2. U-bracket: extruded on top of the base, two arms separated by 50mm inner gap, 60mm tall, opening toward the front (-Z direction).
3. DS3235 placeholder block: a simple rectangular block representing the servo body, placed outside the left bracket arm on its outer face.
4. Shoulder rotation axis (Axis2): a reference axis running along the X axis at the mid-height of the DS3235 block, defined using two planes (Plane1 offset from the DS3235 bottom face + Front Plane). Confirmed to run along X by checking the right side view (Ctrl+4) — axis appeared as a point.
5. Link 1 placeholder beam: a 25×25mm cross-section beam extruded from the outer face of the right bracket arm, extending 150mm outward along X, centered on Axis2.

I also had a key architecture clarification session — I initially had the servo block inside the gap and Link 1 in the wrong position. After working through it step by step and comparing against a reference image, I understood the correct layout.

### What did I understand well?
**The shoulder pitch joint architecture (Option A):**
- The DS3235 servo body is fixed outside the left bracket arm.
- The servo output shaft passes through the left cheek into the gap.
- The Link 1 hub sits between the two bracket cheeks, driven by the servo horn.
- The Link 1 beam exits past the right cheek and extends 150mm outward.
- An M8 support axle on the right cheek carries the load on the non-servo side.
- The rotation axis runs horizontally along X through both cheeks — this is a shoulder pitch axis, not a yaw axis.

**Why this matters:** the servo shaft carries rotation torque only. Bending load is shared across both sides of the bracket. This is the correct mechanical principle for a joint using a strong servo like the DS3235.

**SolidWorks workflow learned:**
- How to center a sketch on the origin using midpoint relations.
- How to use Reference Geometry → Axis (Two Planes) to define a reference axis.
- How to confirm an axis runs along X by checking it appears as a point in the right side view (Ctrl+4).
- How to identify the correct face to sketch on when extruding a beam along a specific axis.

### What is still unclear?
- The exact shaft height of the DS3235 on the servo body — the rotation axis position is approximate until I have the physical servo or its exact datasheet.
- The inner spacing of the U-bracket needs to be recalculated once I know the real hub + servo horn + washer stack thickness.

### What is the next step?
In the next session I will complete the block model:
1. Add a small Link 1 hub placeholder block inside the gap, centered on Axis2, representing where the hub connects to the servo horn.
2. Confirm Link 1 beam exits cleanly from the right cheek, centered on Axis2.
3. Add the M8 support axle stub on the right cheek outer face.
4. Do the axis alignment check: visually confirm DS3235, hub, beam, and axle stub are all on the same horizontal line.
5. Do the rotation clearance check: visually confirm Link 1 can swing up/down without hitting the base.

---

## Day 3

### What did I do?
Completed the SolidWorks block model assembly and brought Link 1 to a fully defined state.

Before making any changes, I cross-checked the proposed workflow with two assistants to make sure the architecture and SolidWorks approach were correct. The key confirmation: Link 1 (hub + beam) must be a separate rotating part — not merged with the fixed U-bracket. The current geometry (beam entering the gap at one cheek face and extending outward) is valid for a block model — the gap section represents the hub and the extending section represents the beam.

I then added a Symmetric mate to link1_block using the assembly's Front Plane, centering Link 1 perfectly in the Z direction (front-to-back) inside the U-bracket gap. This mate, combined with the existing Distance6 mate already in place, brought link1_block from under-defined (-) to fully defined. The support axle placeholder remains floating (-) — accepted for block model stage.

I also confirmed the current mates in the assembly:
- arm_base is fixed (f)
- shoulder_ubracket_block and ds3235_placeholder are fully defined through existing mates
- link1_block is now fully defined ✅
- support_axle_placeholder still floating — not critical at this stage

The block model architecture is now confirmed. Created `Documentation/cad_block_model_notes.md` capturing all confirmed geometry, open questions, and what comes next.

### What did I understand well?
**The difference between floating and architecturally wrong.** Link 1 was geometrically in the right place — hub inside the gap, beam extending outward on the support side — but it was floating because the mates weren't complete. Fixing the mates didn't change the geometry, it just locked it in place. These are two separate problems and it's important not to confuse them.

**When a block model is done.** A block model is done when it answers the questions it was built to answer: which parts are fixed, which rotate, where the rotation axis is, and whether there's enough clearance. It does not need to be pretty, detailed, or perfect. The moment you can answer those questions, you stop and move on.

**Why not to rebuild geometry unnecessarily.** There was a suggestion to rebuild link1 as two separate explicit features (hub block + beam block). After review, this adds complexity with no architectural insight. The current single-block geometry communicates the same information. In engineering, always ask: what question does this change answer? If the answer is "none," don't make it.

### What is still unclear?
- The exact DS3235 shaft height — the rotation axis position is still approximate. The real position depends on the specific manufacturer's unit and must be measured from the physical servo before the detailed cheek design.
- The U-bracket inner gap final value — the current gap is a rough estimate. The real value depends on the servo horn + hub + washer stack thickness, which requires hardware selection first.
- Rotation clearance check result — not yet done. This is the last mandatory step before declaring Block Model v1 complete.

### What is the next step?
1. Do the rotation clearance check: manually rotate Link 1 in SolidWorks through -30° to +150° and confirm it does not clip the base box.
2. Save 4 screenshots into `Images/`: isometric, front view, right side view, and link1 at maximum rotation angle.
3. Declare Block Model v1 complete.
4. Begin planning the detailed shoulder joint design — starting point is the U-bracket cheeks, but gated on having the physical DS3235 in hand (or a verified manufacturer-specific datasheet).

---

## Day 4

### What did I do?
Implemented Inverse Kinematics (IK) for the 2DOF planar arm and added it to `Code/fk_2dof.py`.

Derived the analytical IK solution step by step:
1. Started from the FK equations and squared both sides.
2. Added x² + y², used the Pythagorean identity and the cosine subtraction identity to eliminate θ1 — leaving a single equation in θ2 only.
3. Solved for cos(θ2), applied np.clip to handle floating point edge cases, then arccos to get θ2.
4. Defined k1 and k2 from θ2, then solved for θ1 using atan2.
5. Added boundary checks for unreachable targets (too far and too close) with informative error messages.

Verified with a roundtrip test: FK(45°, 30°, L1=15, L2=13) → (x, y) → IK → (44.9996°, 30.0009°). Floating point error only — correct.

### What did I understand well?
**Why squaring and adding the FK equations works.** When you compute x² + y², the θ1 terms collapse via trig identities, leaving only θ2. This is why the analytical approach is clean for 2DOF — you can isolate one unknown at a time.

**Why atan2 instead of atan.** atan2(y, x) correctly handles all four quadrants. Regular atan would give wrong results for targets in the second and third quadrant.

**Why np.clip before arccos.** Floating point arithmetic can push cos(θ2) just outside [-1, 1] even for valid targets. arccos would crash without the clip.

**The difference between analytical IK and Jacobian IK.** Analytical works here because 2DOF has a closed-form solution. For higher DOF arms (5–6 joints, 3D space) there is no clean closed form — that's when the Jacobian method is needed. Already familiar with Jacobian from coursework.

### What is still unclear?
- The "elbow down" solution — arccos always returns the elbow-up configuration. How to select between solutions will matter when the physical arm has joint limits.

### What is the next step?
1. SolidWorks: rotation clearance check + 4 screenshots → declare Block Model v1 complete (still pending from Day 3).
2. Save animation as GIF or MP4 to `Simulations/` for portfolio.
3. GitHub — push everything.
