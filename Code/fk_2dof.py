# Forward Kinematics — 2DOF Robotic Arm
# Lou | May 2026
# Computes end-effector position from joint angles
import numpy as np
import matplotlib.pyplot as plt
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SIM_DIR = os.path.join(SCRIPT_DIR, '..', 'Simulations')
os.makedirs(SIM_DIR, exist_ok=True)

def forward_kinematics(theta1,theta2,L1,L2):
    angle_rad1 = np.radians(theta1)
    angle_rad2 = np.radians(theta2)
    x = np.cos(angle_rad1)*L1 + np.cos(angle_rad1+angle_rad2)*L2
    y = np.sin(angle_rad1)*L1 + np.sin(angle_rad1+angle_rad2)*L2 
    return x,y

def joint_positions(theta1,theta2,L1,L2):
    t1 = np.radians(theta1)
    t2 = np.radians(theta2)
    x0,y0 = 0.0,0.0
    x1 = L1 * np.cos(t1)
    y1 = L1 * np.sin(t1)
    x2 = x1 + L2 * np.cos(t1 + t2)
    y2 = y1 + L2 * np.sin(t1 + t2)
    return (x0, y0), (x1, y1), (x2, y2)




def plot_arm(theta1, theta2, L1, L2):
    (x0, y0), (x1, y1), (x2, y2) = joint_positions(theta1, theta2, L1, L2)
    plt.figure(figsize=(6,6))
    plt.plot([x0, x1, x2], [y0, y1, y2], 'bo-', linewidth=3, markersize=8)
    plt.axis('equal')
    plt.title(f'θ1={theta1}°, θ2={theta2}° | end: ({x2:.2f}, {y2:.2f}) cm')
    plt.grid(True)
    plt.savefig(os.path.join(SIM_DIR, 'arm_pose.png'), dpi=150)
    plt.show()


def plot_workspace(L1, L2):
    xs = []
    ys = []
    
    for theta1 in np.linspace(0, 360, 300):
        for theta2 in np.linspace(-180, 180, 50):
            x, y = forward_kinematics(theta1,theta2,L1,L2)
            xs.append(x)
            ys.append(y)
    
    plt.scatter(xs, ys, s=0.5, alpha=0.2)
    plt.axis('equal')
    plt.grid(True)
    plt.savefig(os.path.join(SIM_DIR, 'workspace.png'), dpi=150)
    plt.show()

def run_verification():
    x, y = forward_kinematics(90, 0, 10, 8)
    passed = abs(x) < 0.01 and abs(y - 18) < 0.01
    print('── Verification ──────────────────────')
    print(f'FK(90°, 0°, L1=10, L2=8) → x={x:.4f}, y={y:.4f}')
    print(f'Expected: x≈0, y≈18')
    print(f'Result: {"✅ PASS" if passed else "❌ FAIL"}')
    print('──────────────────────────────────────')

plot_arm(45, 30, 15, 13)
plot_workspace(15, 13)
run_verification()
