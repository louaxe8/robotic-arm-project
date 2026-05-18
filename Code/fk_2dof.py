# Forward Kinematics — 2DOF Robotic Arm
# Lou | May 2026
# Computes end-effector position from joint angles
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
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

def forward_kinematics_n(thetas,lengths):
    if len(thetas) != len(lengths):
        raise ValueError("amount of thetas or lengthes are not equal")
    x,y,angle = 0,0,0
    cordinate_arr = [(0,0)]
    for theta,length in zip(thetas,lengths):
        theta = np.radians(theta)
        angle = angle+theta 
        x = x + length * np.cos(angle)
        y = y + length * np.sin(angle)
        cordinate_arr.append((x,y))
    for i, (x, y) in enumerate(cordinate_arr):
        print(f"Joint {i}: x={x:.4f}, y={y:.4f}")
    return cordinate_arr

def inverse_kinematics(x,y,L1,L2):
    d = np.sqrt(x**2 + y**2)
    if d > L1 + L2:
        raise ValueError(f"Target ({x}, {y}) is out of reach — too far (d={d:.2f}, max={L1+L2})")
    if d < abs(L1 - L2):
        raise ValueError(f"Target ({x}, {y}) is out of reach — too close (d={d:.2f}, min={abs(L1-L2)})")
    cos_theta2 = (x**2 + y**2 -L1**2 -L2**2)/(2*L1*L2)
    cos_theta2 = np.clip(cos_theta2,-1,1)
    theta2 = np.arccos(cos_theta2)
    k1 = L1+L2*np.cos(theta2)
    k2 = L2*np.sin(theta2)
    theta1 = np.arctan2(y,x) - np.arctan2(k2,k1)
    return np.degrees(theta1),np.degrees(theta2)

def animate_ik(x1, y1, x2, y2, L1, L2):
    t1_start,t2_start = inverse_kinematics(x1,y1,L1,L2)
    t1_end,t2_end = inverse_kinematics(x2, y2, L1, L2)
    fig, ax = plt.subplots(figsize=(6,6))
    total_frames = 100
    def update(frame):
        ax.clear()
        ax.set_xlim(-L1-L2, L1+L2)
        ax.set_ylim(-L1-L2, L1+L2)
        ax.axis('equal')
        ax.grid(True)
        t = min(frame / total_frames, 1.0)
        theta1 = t1_start + (t1_end - t1_start) * t
        theta2 = t2_start + (t2_end - t2_start) * t
        (x0,y0), (x1,y1), (x2,y2) = joint_positions(theta1, theta2, L1, L2)
        ax.plot([x0,x1,x2],[y0,y1,y2],'bo-',linewidth=3,markersize=8)
        ax.set_title(f'θ1={theta1:.1f}°, θ2={theta2:.1f}° | end: ({x2:.2f}, {y2:.2f})')
    ani = FuncAnimation(fig, update, frames=total_frames + 60, interval=50)
    ani.save(os.path.join(SIM_DIR, 'arm_animation.gif'), writer='pillow', fps=20)
    plt.show()
    return t1_start,t2_start, t1_end,t2_end

def animate_trajectory(points,L1,L2, home=None):
    if len(points) == 0:
        raise ValueError("points list cannot be empty")
    if home is None:
        home = (0,L1+L2)
    points = [home] + points + [home]
    angles = []
    for (x, y) in points:
        angles.append(inverse_kinematics(x, y, L1, L2))
    fig, ax = plt.subplots(figsize=(6,6))
    total_frames = 100
    pause_frames =30
    def update(frame):
        ax.clear()
        ax.set_xlim(-L1-L2, L1+L2)
        ax.set_ylim(-L1-L2, L1+L2)
        ax.axis('equal')
        ax.grid(True)
        segment_size = total_frames + pause_frames
        segment = frame // segment_size
        t = min((frame % segment_size) / total_frames,1.0)
        t1_start, t2_start = angles[segment]
        t1_end, t2_end = angles[segment + 1]
        theta1 = t1_start + (t1_end - t1_start) * t
        theta2 = t2_start + (t2_end - t2_start) * t
        (x0,y0), (x1,y1), (x2,y2) = joint_positions(theta1, theta2, L1, L2)
        ax.plot([x0,x1,x2],[y0,y1,y2],'bo-',linewidth=3,markersize=8)
        px, py = zip(*points)
        ax.scatter(px, py, c='red', s=50, zorder=5)
        ax.scatter(*points[segment + 1], c='green', s=100, zorder=6)
        ax.set_title(f'Segment {segment + 1}/{len(points) - 1} | θ1={theta1:.1f}°, θ2={theta2:.1f}° | end: ({x2:.2f}, {y2:.2f})')
    ani = FuncAnimation(fig, update, frames=(total_frames + pause_frames) * (len(points) - 1), interval=50)
    plt.show()
    ani.save(os.path.join(SIM_DIR, 'arm_animation.gif'), writer='pillow', fps=20)
    


#x, y = forward_kinematics(45, 30, 15, 13)
#t1, t2 = inverse_kinematics(x, y, 15, 13)
#t1_start, t2_start, t1_end, t2_end = animate_ik(-15, 13, 1, 10, 15, 13)
points = [(5, 10), (28, 0), (5, 20), (15, 10)]
animate_trajectory(points, 15, 13,home=(-5,-20))
#print(f"Angles for point 1 are: {t1_start:.2f}°, θ2={t2_start:.2f}°")
#print(f"Angles for point 2 are: {t1_end:.2f}°, θ2={t2_end:.2f}°")
