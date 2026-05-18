# Wiring Diagram — MG90S + ESP32
**Lou | May 2026**
**Stage:** Learning build — USB power only (MG90S)

---

## Connection Table

| MG90S Wire | Color  | Connects To       | ESP32 Pin |
|------------|--------|-------------------|-----------|
| Ground     | Brown  | GND               | Any GND   |
| Power      | Red    | 5V (USB power)    | VIN / 5V  |
| Signal     | Orange | PWM signal output | GPIO 18   |

---

## ASCII Diagram

```
ESP32 Dev Board
┌─────────────────┐
│                 │
│   GPIO 18  ─────┼──────────── Orange (Signal)  ┐
│                 │                               │
│   VIN (5V) ─────┼──────────── Red    (Power)   ├── MG90S
│                 │                               │
│   GND      ─────┼──────────── Brown  (Ground)  ┘
│                 │
└─────────────────┘

Power source: USB cable → ESP32 VIN → MG90S Red
Signal source: ESP32 GPIO 18 → MG90S Orange
Common ground: ESP32 GND → MG90S Brown
```

---

## Important Rules

**Common GND is mandatory.**
The ESP32 and servo must share the same ground reference. Without it, the signal wire has no return path and the servo behaves erratically or not at all.

**ESP32 does NOT power the DS3235.**
This setup works only because MG90S is a small servo (max ~250mA stall). When moving to the DS3235 shoulder servo, an external 6V power supply is required. The DS3235 draws 1–3A under load — USB will collapse and reset the ESP32.

**Signal voltage is 3.3V — and that's fine.**
ESP32 GPIO outputs 3.3V logic. Standard servo signal is specified at 5V, but the MG90S (and most modern servos including DS3235) accepts 3.3V signal correctly. No level shifter needed.

---

## When Moving to DS3235 (external power setup)

```
External 6V PSU
┌──────────────┐
│  V+ (6V) ───┼──────────────────────── Red    (DS3235 Power)  ┐
│             │         ┌── 1000µF cap                          │
│  GND    ────┼──────┬──┘  across V+/GND                       ├── DS3235
│             │      │                                           │
└──────────────┘      └──────────────────────── Brown  (Ground) ┘
                      │
              ESP32 GND (shared)
                      │
              ESP32 GPIO 18 ───────────────── Orange (Signal)

⚠️  ESP32 GND must connect to the external PSU GND — common ground.
⚠️  ESP32 VIN does NOT connect to the 6V supply — only GND is shared.
⚠️  1000µF capacitor across the servo power rails reduces voltage spikes.
```

---

## Code Reference

- **Library:** ESP32Servo (by Kevin Harrington)
- **Signal pin:** GPIO 18
- **PWM frequency:** 50Hz (standard servo)
- **Angle range:** 0° – 180°
- **File:** `Code/servo_control.ino`
