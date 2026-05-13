# Forward Kinematics — 2DOF Robotic Arm
# Lou | May 2026
# Computes end-effector position from joint angles
import numpy as np
import matplotlib.pyplot as plt

def forward_kinematics(theta1,theta2,L1,L2):
    angle_rad1 = np.radians(theta1)
    angle_rad2 = np.radians(theta2)
    x = np.cos(angle_rad1)*L1 + np.cos(angle_rad1+angle_rad2)*L2
    y = np.sin(angle_rad1)*L1 + np.sin(angle_rad1+angle_rad2)*L2 
    return x,y


def plot_arm(theta1, theta2, L1, L2):
    x0,y0 = 0,0
    x1,y1 = forward_kinematics(theta1,0,L1,0)
    x2,y2 = forward_kinematics(theta1,theta2,L1,L2)
    plt.plot([x0, x1, x2], [y0, y1, y2], 'k*-', linewidth=3)
    plt.axis('equal')
    plt.grid(True)
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
    plt.show()

plot_workspace(15,13)


