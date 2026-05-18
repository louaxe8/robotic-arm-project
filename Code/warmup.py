import numpy as np

def circle_point(angle_deg, radius):
    ang_rad = np.radians(angle_deg)
    x = np.cos(ang_rad)*radius
    y = np.sin(ang_rad)*radius
    return x,y

x1, y1 = circle_point(45, 10)
print(f"x1={x1:.2f}, y1={y1:.2f}")

x2,y2 = circle_point(10,0)
print(f"x2 = {x2:.2f}, y2= {y2:.2f}")

x3,y3 = circle_point(0,10)
print(f"x3 = {x3:.2f}, y3= {y3:.2f}")