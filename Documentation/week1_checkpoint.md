# Week 1 Checkpoint — Phase 0 Complete
**Lou | May 2026**

---

## What This Phase Was

Phase 0: Build the foundation. Python, GitHub, FK, IK, servo control, and a verified CAD architecture — all before building anything physical.

The rule was: **Learn it → Build it → Document it.** One topic at a time, nothing deferred, nothing started without finishing the previous step.

---

## What Was Built

### Python — Forward & Inverse Kinematics
**File:** `Code/fk_2dof.py`

- 2DOF FK: computes end-effector (x, y) from two joint angles and link lengths
- N-DOF generalized FK: handles any number of links via a loop (not limited to 2 joints)
- 2DOF IK: analytical closed-form solution — derives θ1, θ2 from target (x, y)
- Boundary checks: raises informative errors for unreachable targets (too far and too close)
- Roundtrip verified: FK → IK error is floating point only (~0.001°)
- Workspace visualization: scatter plot of all reachable points
- Single-move animation (`animate_ik`): arm moves from point A to point B
- Multi-waypoint animation (`animate_trajectory`): arm visits a list of target points, starts and ends at home

### ESP32 + MG90S Servo Control
**File:** `Code/servo_control.ino`

- Smooth movement: one degree per step with configurable delay
- Software angle limits via `constrain()`
- Home position function: boots to a known state (0° → 90°)
- Known starting position enforced on every boot

### SolidWorks Block Model v1
**File:** `CAD/arm_assembly_v1_BLOCKMODEL.SLDASM`

Verified the shoulder joint architecture before committing to any detailed geometry:
- DS3235 servo body: fixed, outside left bracket cheek
- U-bracket: fixed, mounts to base
- Link 1 (hub + beam): separate rotating part, fully constrained
- Shoulder rotation axis: horizontal pitch axis along X
- Rotation clearance check: PASSED (−30° to +150°, no collision)
- 4 screenshots saved to `Images/`

---

## What Was Learned

**Kinematics:** why squaring and adding the FK equations isolates θ2; why atan2 handles all quadrants correctly; why `np.clip` is needed before arccos; the difference between analytical IK (2DOF, closed form) and Jacobian IK (higher DOF).

**Electronics:** `myServo.read()` returns the last commanded angle, not the physical position — always write a known angle at boot before reading; common GND is mandatory; USB power is not enough for the DS3235.

**CAD thinking:** the difference between a part being geometrically correct and being properly constrained; when a block model is done (the moment it answers its architectural questions — not when it looks detailed); why you don't rebuild geometry unless a specific question demands it.

---

## What Is Not Done Yet (Intentionally)

- DS3235 detailed shoulder CAD — **gated on physical servo in hand**
- Elbow-down IK (arccos always returns elbow-up) — needed later, not now
- 3DOF FK / 3D IK — Phase 3+ topic
- ROS2, Gazebo, SLAM, YOLO — future phases, not relevant now

---

## Output Files Summary

| Type | Files |
|---|---|
| Code | `Code/fk_2dof.py`, `Code/servo_control.ino` |
| Simulations | `Simulations/arm_animation.gif`, `Simulations/arm_pose.png`, `Simulations/workspace.png` |
| CAD | `CAD/arm_assembly_v1_BLOCKMODEL.SLDASM` |
| Images | `Images/block_model_v1_iso.png`, `_front.png`, `_side.png`, `_top.png` |
| Docs | `Documentation/` — design brief, CAD notes, IK notes, electronics notes, log |

---

## Next Phase — Mini 2DOF Physical Arm

**Goal:** Connect the IK output to the ESP32 servo control on a small physical arm that moves to target points.

**Why this is next:** IK computes the angles. Servo control executes the angles. The physical arm is the only missing link between them.

**Gate:** Hardware — two MG90S servos (or one MG90S + the DS3235 once it arrives), a printed or assembled 2-link arm structure.

**What success looks like:** Give the arm a target (x, y). It moves there.
