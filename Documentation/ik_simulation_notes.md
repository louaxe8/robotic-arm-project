# Inverse Kinematics — 2DOF Planar Arm
**Lou | May 2026**
**File:** `Code/fk_2dof.py`

---

## What This Solves

Given a target point (x, y) in the plane, compute the two joint angles (θ1, θ2) that place the end-effector at that point. This is the inverse of FK — instead of angles → position, it's position → angles.

---

## Derivation

**Starting point — FK equations:**

```
x = L1·cos(θ1) + L2·cos(θ1 + θ2)
y = L1·sin(θ1) + L2·sin(θ1 + θ2)
```

**Step 1 — Isolate θ2.**

Square both equations and add them:

```
x² + y² = L1² + L2² + 2·L1·L2·cos(θ2)
```

The θ1 terms cancel via the Pythagorean identity (sin² + cos² = 1) and the cosine subtraction identity. This leaves a single equation in θ2 only.

Solve for cos(θ2):

```
cos(θ2) = (x² + y² − L1² − L2²) / (2·L1·L2)
```

Apply `np.clip(cos_θ2, -1, 1)` before arccos — floating point arithmetic can push the value just outside [-1, 1] for targets on the workspace boundary, which would crash arccos.

```
θ2 = arccos(cos_θ2)
```

**Step 2 — Solve for θ1.**

Define:

```
k1 = L1 + L2·cos(θ2)
k2 = L2·sin(θ2)
```

Then:

```
θ1 = atan2(y, x) − atan2(k2, k1)
```

`atan2` is used (not `atan`) because it correctly handles all four quadrants. Regular `atan` would give wrong results for targets in Q2 and Q3.

---

## Boundary Checks

Before solving, check whether the target is reachable:

```python
d = sqrt(x² + y²)

if d > L1 + L2:   # too far — outside outer boundary
    raise ValueError(...)

if d < |L1 - L2|:  # too close — inside inner boundary (donut hole)
    raise ValueError(...)
```

---

## Roundtrip Verification

```
FK(45°, 30°, L1=15, L2=13) → (x, y)
IK(x, y, L1=15, L2=13)     → (44.9996°, 30.0009°)
```

Error is floating point only (~0.001°). Correct.

---

## The Solution This Computes

`arccos` always returns a value in [0°, 180°], so this IK gives the **elbow-up** configuration only — θ2 is always positive (elbow bends upward).

The elbow-down solution exists (θ2 negative) and is the mirror image. For the current 2DOF simulation, elbow-up is sufficient. Elbow-down selection will matter when the physical arm has joint limits that block certain configurations.

---

## Simulation Functions

### `animate_ik(x1, y1, x2, y2, L1, L2)`
Animates the arm moving from one point to another. Linearly interpolates θ1 and θ2 between the start and end IK solutions. Saves to `Simulations/arm_animation.gif`.

### `animate_trajectory(points, L1, L2, home=None)`
Animates the arm visiting a sequence of target points, starting and ending at a home position. Each segment linearly interpolates the joint angles. All target points are shown in red; the active target is highlighted in green. Saves to `Simulations/arm_animation.gif`.

**Example used:**
```python
points = [(5, 10), (28, 0), (5, 20), (15, 10)]
animate_trajectory(points, L1=15, L2=13, home=(-5, -20))
```

---

## What the Simulation Demonstrates

- The arm correctly reaches each waypoint in sequence.
- Joint angle interpolation produces smooth motion (no jumps).
- The IK boundary checks correctly reject unreachable points before the animation starts.
- The workspace is the annular region between radius `|L1−L2|` and `L1+L2`.

---

## Output Files

| File | Description |
|---|---|
| `Simulations/arm_animation.gif` | animate_trajectory output — multi-waypoint motion |
| `Simulations/arm_pose.png` | Static arm pose at a single configuration |
| `Simulations/workspace.png` | Full 2DOF reachable workspace scatter plot |

---

## What Is Not Implemented Yet

- Elbow-down IK (negative θ2 branch)
- Joint velocity limits
- Collision avoidance between links
- 3D extension (requires full 3D FK/IK, different math)
