# Robotic Arm Project — מפת דרכים
**Lou | שנה ג' הנדסה מכנית | 2026**

---

## הפרויקט

**זרוע רובוטית שולחנית מודפסת בתלת-ממד.**

לא "ללמוד רובוטיקה". לבנות מערכת אמיתית — כל נושא נכנס לפרויקט ונותן תוצר מוחשי.

> **Learn it → Build it → Document it**
> כל נושא מסתיים ב: קוד עובד | סימולציה | גרף | מודל CAD | חלק מודפס | ניסוי | תיעוד | וידאו

---

## ⚠️ כלל הפוקוס

**אם עולה רצון לקפוץ ל-YOLO / SLAM / Gazebo / ROS2 לפני הזמן:**

> השלב הנוכחי הוא:
> **Python → FK/IK → CAD → Servo control בסיסי**
>
> ROS2 מגיע רק אחרי שיש זרוע פיזית עובדת. הכל השאר ממתין.

---

## מבנה תיקיות (מקומי קודם, GitHub בסוף שבוע 1–2)

```
robotic-arm-project/
├── CAD/
├── Code/
├── Simulations/
├── Electronics/
├── Documentation/
└── Images/
```

---

# 4 שבועות קרובים — תוכנית עבודה מפורטת

---

## שבוע 1 — הגדרה + FK + ציור זרוע

**יעד השבוע:** להבין FK ולכתוב קוד שמחשב ומצייר מיקום קצה הזרוע.

---

### לוז יומי

#### שלישי — פתיחה (30–45 דקות)
**בוקר:**
פתח `Documentation/project_definition.md` וענה על 5 שאלות:
1. מה הזרוע צריכה לעשות?
2. כמה מפרקים יהיו?
3. אילו מנועים יש לי?
4. מה הגודל המשוער?
5. מה התוצר שאני רוצה עד סוף החודש?

**ערב:** מנוחה — או סרטון אחד על Forward Kinematics (YouTube).

---

#### רביעי — FK ראשון (2–3 שעות בוקר)
כתוב `Code/fk_2dof.py`:

```python
import numpy as np

def forward_kinematics(theta1, theta2, L1, L2):
    """
    קלט: זוויות במעלות, אורכי מקטעים בס"מ
    פלט: מיקום קצה הזרוע (x, y)
    """
    t1 = np.radians(theta1)
    t2 = np.radians(theta2)
    x = L1 * np.cos(t1) + L2 * np.cos(t1 + t2)
    y = L1 * np.sin(t1) + L2 * np.sin(t1 + t2)
    return x, y

# בדיקה
print(forward_kinematics(45, 30, 10, 8))
```

**ערב (45 דקות):** צור תיקיות מקומיות. כתוב `Documentation/log_week1.md`:
- מה עשיתי?
- מה עבד?
- מה לא עבד?
- מה הצעד הבא?

---

#### חמישי — ציור הזרוע (1.5–2 שעות בוקר)
הוסף ל-`fk_2dof.py`:

```python
import matplotlib.pyplot as plt

def plot_arm(theta1, theta2, L1, L2):
    t1 = np.radians(theta1)
    t2 = np.radians(theta2)
    
    x0, y0 = 0, 0
    x1 = L1 * np.cos(t1)
    y1 = L1 * np.sin(t1)
    x2 = x1 + L2 * np.cos(t1 + t2)
    y2 = y1 + L2 * np.sin(t1 + t2)
    
    plt.figure(figsize=(6, 6))
    plt.plot([x0, x1, x2], [y0, y1, y2], 'bo-', linewidth=3, markersize=8)
    plt.xlim(-L1-L2-2, L1+L2+2)
    plt.ylim(-L1-L2-2, L1+L2+2)
    plt.axis('equal')
    plt.grid(True)
    plt.title(f'θ1={theta1}°, θ2={theta2}°')
    plt.savefig('Simulations/arm_pose.png', dpi=150)
    plt.show()

plot_arm(45, 30, 10, 8)
```

**ערב:** סרטון אחד — "2DOF robotic arm forward kinematics visualization".

---

#### שישי — בונוס: Workspace + CAD ראשון (2–3 שעות בוקר)
**אם יש כוח — זה בונוס, לא חובה:**

Workspace ב-`fk_2dof.py`:
```python
def plot_workspace(L1, L2, n=300):
    points = []
    for t1 in np.linspace(0, 2*np.pi, n):
        for t2 in np.linspace(-np.pi, np.pi, n // 5):
            x, y = forward_kinematics(
                np.degrees(t1), np.degrees(t2), L1, L2
            )
            points.append((x, y))
    xs, ys = zip(*points)
    plt.figure(figsize=(7, 7))
    plt.scatter(xs, ys, s=0.3, alpha=0.2, c='steelblue')
    plt.axis('equal')
    plt.grid(True)
    plt.title('Workspace — 2DOF')
    plt.savefig('Simulations/workspace.png', dpi=150)
    plt.show()
```

**SolidWorks (אם יש זמן):** פתח חלון חדש — רק חשוב על צורה כללית של הבסיס. לא לסיים, לא להתחייב. ראה מה מרגיש נכון.

**ערב:** שמור screenshots אם עשית CAD. כתוב 2–3 שורות הערות.

---

#### שבת — מחקר קל (80 דקות)
60 דקות: חפש "3D printed robotic arm joints" ב-YouTube + Printables + Thingiverse.
שים לב: איך נראים מפרקים קיימים? מה הם פתרו?

20 דקות: כתוב `Documentation/design_research.md` — 3–5 insights בלבד.

---

#### ראשון — סיכום + GitHub (30–45 דקות ערב)
- צור GitHub repo: `robotic-arm-project`
- העלה את מה שיש (תיקיות + קוד + גרפים)
- כתוב README ראשוני: שורה אחת — מה הפרויקט

---

### ✅ Checkpoint שבוע 1

| תוצר | סטטוס |
|---|---|
| `Documentation/project_definition.md` | **חובה** |
| `Code/fk_2dof.py` — מחשב (x,y) | **חובה** |
| `Simulations/arm_pose.png` — גרף זרוע | **חובה** |
| `Simulations/workspace.png` | בונוס |
| CAD ראשוני — סתם לפתוח ולחשוב | בונוס |
| `Documentation/design_research.md` | בונוס |
| GitHub repo עם README | חובה (יכול להיות ראשון) |

**שאלת הבדיקה:** האם הקוד מחשב נכון את (x,y) עבור (θ1=90°, θ2=0°, L1=10, L2=8)?
תשובה נכונה: x ≈ 0, y ≈ 18.

---

## שבוע 2 — Workspace + חישוב מומנט + CAD בסיס

**יעד השבוע:** להבין כמה כוח צריך הסרוו, ולהתחיל תכנון CAD ריאלי.

---

### לוז יומי

#### ראשון / שני — Workspace + מומנט (2–3 שעות בוקר)

**Workspace** — אם לא עשית בשבוע שעבר, עכשיו זה חובה.

**חישוב מומנט נדרש:**

```
Torque_required [kg·cm] = weight [kg] × distance [cm]
```

דוגמה לזרוע 2DOF:
```
מקטע 2 (forearm): 0.15kg × 10cm = 1.5 kg·cm
מקטע 1 (upper arm) נושא את מקטע 2 + מוטור 2:
  (0.15 + 0.2)kg × 15cm = 5.25 kg·cm

→ מוטור מפרק 2: צריך לפחות 1.5 kg·cm → בחר ≥ 3–5 kg·cm
→ מוטור מפרק 1: צריך לפחות 5.25 kg·cm → בחר ≥ 10–15 kg·cm
```

כתוב `Documentation/torque_calculation.md`:
- משקל כל מקטע (אומדן)
- מרחק ממרכז כובד למפרק
- Torque נדרש
- סרוו שבחרת + מקדם ביטחון

**ערב (30 דקות):** רשום רכיבים נדרשים — סרווים, ESP32, כבלים, נשאים (bearings).

---

#### שלישי — SolidWorks: בסיס (2–3 שעות בוקר)

בנה `CAD/base_v1.SLDPRT`:

| אלמנט | פרטים |
|---|---|
| גוף חיצוני | ~80×80×60mm, עובי דפנות 2.5mm |
| חלל למשקולת | תחתית, גישה מלמטה |
| חלל לבקר | ESP32: 52×28mm + מרווח 3mm |
| תעלות חיווט | קוטר ≥ 6mm, 2 מיקומים |
| מכסה | snap-fit או M3 ×4 |
| flange עליון | חיבור למפרק 1: 4× M3, PCD=30mm |

**ערב (30 דקות):** שמור 2–3 screenshots ב-`Images/`. עדכן log.

---

#### שישי — SolidWorks: מפרק 1 ראשוני (2–3 שעות בוקר)

בנה `CAD/joint1_v1.SLDPRT` — לא חייב להיות מושלם:
- גוף שמחזיק את הסרוו במקום
- מקום ל-bearing (אם יש)
- stop מכני בזוויות קצה
- התחברות לבסיס מלמטה

**לא לנסות לבנות הכל בבת אחת.** מבנה פשוט שמחזיק סרוו — זה מספיק לעכשיו.

**ערב/אחה"צ:** שמור תמונות. כתוב הערות: מה עדיין חסר, מה לא פתור.

---

### ✅ Checkpoint שבוע 2

| תוצר | סטטוס |
|---|---|
| `Simulations/workspace.png` | **חובה** |
| `Documentation/torque_calculation.md` — מספרים אמיתיים | **חובה** |
| `CAD/base_v1.SLDPRT` — בסיס עם רכיבים פנימיים | **חובה** |
| `CAD/joint1_v1.SLDPRT` — מפרק ראשוני | **חובה** |
| רשימת רכיבים לרכישה | **חובה** |
| GitHub מעודכן עם כל הקבצים | **חובה** |
| Animation/motion study ב-SolidWorks | בונוס |
| חישוב מומנט גם למפרק 2 | בונוס |

---

## שבוע 3 — Prototype 0: מכוער אבל עובד

**יעד השבוע:** מפרק פיזי אחד שזז על פי פקודה. לא יפה — עובד.

**עיקרון Prototype 0:** מדפיסים מהר, בודקים מהר, לומדים מהר. מושלם בא אחרי שיש לנו data אמיתי.

---

### שלב 3A — הדפסה ראשונה

**מה להדפיס (Bambu Studio):**
- גרסה פשוטה ולא מושלמת של מפרק 1
- הגדרות: PLA, 30% infill, 2 perimeters, 0.3mm layer height (מהיר)
- זמן הדפסה: להעדיף תוצאה מהירה ולא מושלמת

**לא לחכות לגרסה מושלמת.** המטרה היא לראות מה לא עובד.

---

### שלב 3B — ESP32 + סרוו ראשון (2–3 שעות בוקר)

**עיקרי האלקטרוניקה:**

```
מקור כוח 5–6V חיצוני ──→ V+ + GND של הסרוו
ESP32 (GPIO pin) ────────→ Signal של הסרוו
ESP32 GND ──────────────→ GND משותף (חייב!)
ESP32 לא מאכיל את הסרוו — רק שולח signal
```

כתוב `Code/servo_control.ino`:

```cpp
#include <ESP32Servo.h>

Servo myServo;
const int SERVO_PIN = 18;

void setup() {
  Serial.begin(115200);
  myServo.attach(SERVO_PIN);
  myServo.write(90); // home position
}

void moveServoSmooth(int targetAngle, int delayMs = 10) {
  int current = myServo.read();
  int step = (targetAngle > current) ? 1 : -1;
  while (current != targetAngle) {
    current += step;
    myServo.write(current);
    delay(delayMs);
  }
}

void homePosition() {
  moveServoSmooth(90);
}

void emergencyStop() {
  myServo.detach(); // מנתק PWM מיידית
}

void loop() {
  // בדיקה: 0° → 90° → 180° → 90°
  moveServoSmooth(0);   delay(500);
  moveServoSmooth(90);  delay(500);
  moveServoSmooth(180); delay(500);
  moveServoSmooth(90);  delay(1000);
}
```

**ערב (30 דקות):** צלם וידאו של הסרוו זז. שמור ב-`Images/`.

---

### שלב 3C — בדיקות מכניות

אחרי שהסרוו זז:
- [ ] הגוף המודפס מחזיק את הסרוו במקום?
- [ ] יש רעידות? מאיפה? (backlash / חיבור רופף / אספקת כוח?)
- [ ] הסרוו מחזיק את עצמו + משקל ריק?
- [ ] הזוויות הקצה לא פוגעות במבנה?

כתוב `Documentation/prototype0_notes.md`: מה עבד, מה לא, מה לשנות ב-v2.

---

### ✅ Checkpoint שבוע 3

| תוצר | סטטוס |
|---|---|
| `Code/servo_control.ino` — smooth + home + e-stop | **חובה** |
| `Electronics/wiring_diagram.png` — תרשים חיווט | **חובה** |
| `Images/prototype0_moving.mp4` — וידאו זז | **חובה** |
| `Documentation/prototype0_notes.md` — מה למדת | **חובה** |
| CAD joint v2 על בסיס הבדיקות | בונוס |
| הדפסה שנייה עם שיפורים | בונוס |
| בדיקת עומס — משקל ידוע על הזרוע | בונוס |

---

## שבוע 4 — שיפור + IK ראשון

**יעד השבוע:** מפרק משופר + הבנת IK.

---

### שלב 4A — CAD v2 (בוקר ראשון)

על בסיס `prototype0_notes.md`:
- תקן מה שלא עבד מכנית
- שפר גישה לברגים / חיווט
- הדפס גרסה 2 עם הגדרות איכות (0.2mm layer height, 40% infill)

---

### שלב 4B — Inverse Kinematics ראשון (2–3 שעות בוקר)

הוסף ל-`Code/fk_2dof.py`:

```python
def inverse_kinematics(x, y, L1, L2):
    """
    קלט: נקודת יעד (x, y), אורכי מקטעים
    פלט: (theta1, theta2) במעלות
    """
    d = np.sqrt(x**2 + y**2)
    
    # בדיקה: האם הנקודה בטווח?
    if d > L1 + L2:
        raise ValueError(f"נקודה ({x},{y}) מחוץ ל-workspace")
    if d < abs(L1 - L2):
        raise ValueError(f"נקודה ({x},{y}) קרובה מדי")
    
    # IK analytic
    cos_t2 = (x**2 + y**2 - L1**2 - L2**2) / (2 * L1 * L2)
    cos_t2 = np.clip(cos_t2, -1, 1)  # מניעת שגיאות numerical
    theta2 = np.arccos(cos_t2)
    
    k1 = L1 + L2 * np.cos(theta2)
    k2 = L2 * np.sin(theta2)
    theta1 = np.arctan2(y, x) - np.arctan2(k2, k1)
    
    return np.degrees(theta1), np.degrees(theta2)

# בדיקה: FK(45, 30, 10, 8) → קבל נקודה → IK → קבל בחזרה 45, 30
x, y = forward_kinematics(45, 30, 10, 8)
t1, t2 = inverse_kinematics(x, y, 10, 8)
print(f"FK: ({x:.2f}, {y:.2f})")
print(f"IK: θ1={t1:.1f}°, θ2={t2:.1f}°")  # אמור להחזיר ≈45, 30
```

**ערב (45 דקות):** תיעוד — הסבר IK ב-3 משפטים ב-`Documentation/ik_notes.md`.

---

### ✅ Checkpoint שבוע 4

| תוצר | סטטוס |
|---|---|
| `Code/fk_2dof.py` — FK + IK + בדיקת roundtrip | **חובה** |
| `CAD/joint1_v2.SLDPRT` — גרסה משופרת | **חובה** |
| `Images/joint_v2_photo.jpg` | **חובה** |
| `Documentation/ik_notes.md` — הסבר + תוצאות | **חובה** |
| GitHub מעודכן | **חובה** |
| אנימציה Python: זרוע נעה בין שתי נקודות | בונוס |
| חיבור IK ל-ESP32 — שליחת נקודת יעד | בונוס |

---

## מה מגיע אחרי 4 השבועות האלה

הסדר הנכון — כל שלב בתנאי שהקודם עובד:

```
חודש 2: ESP32 + 2 סרווים + חיבור IK לחומרה
חודש 3: 2DOF פיזי שמגיע לנקודות מוגדרות
חודש 4: OpenCV + ArUco marker → הזרוע מגיבה
אחרי כן: ROS2 — nodes, topics, TF2, RViz
```

---

## מפת הדרכים הרחבה — לזכירה בלבד

| פאזה | תוכן | מתי |
|---|---|---|
| 0 | Python + Setup + FK ראשון | שבועיים (עכשיו) |
| 1 | FK + Workspace + CAD בסיס + מומנט | חודש 1 |
| 2 | Prototype 0 + ESP32 + סרוו | חודש 2 |
| 3 | 2DOF פיזי + IK | חודש 3 |
| 4 | OpenCV + ArUco + הזרוע מגיבה | חודש 4 |
| 5 | ROS2 — רק אחרי שהכל עובד | אחרי כן |

**נדחה בכוונה:** YOLO, SLAM, Gazebo מורכב, Nav2, RRT*, LQR, Docker.
