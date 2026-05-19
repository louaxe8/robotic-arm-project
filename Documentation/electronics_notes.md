# Electronics Notes — ESP32 + Servo Control
**Lou | May 2026**

---

## Build 1: ESP32 + MG90S (Learning Build)

**Purpose:** Learn servo control fundamentals before working with the DS3235 shoulder servo.

**Hardware:**
- ESP32 Dev Board
- MG90S micro servo (9g)
- USB power only (no external PSU needed at this stage)

**Library:** ESP32Servo by Kevin Harrington

**Wiring:** See `Electronics/wiring_mg90s_esp32.md` for full connection table and ASCII diagram.

---

## Features Implemented

### Smooth movement
Moves one degree at a time with a configurable delay between steps. This avoids current spikes and mechanical shock that occur when jumping directly to the target angle.

```cpp
void moveServoSmooth(int targetAngle, int delayMs) {
    targetAngle = constrain(targetAngle, MIN_ANGLE, MAX_ANGLE);
    int currentAngle = myServo.read();
    while (currentAngle != targetAngle) {
        currentAngle += (targetAngle > currentAngle) ? 1 : -1;
        myServo.write(currentAngle);
        delay(delayMs);
    }
}
```

**Speed control:** adjust `delayMs`. 5ms = fast, 15ms = slow/safe.

### Software angle limits
`constrain()` enforces `MIN_ANGLE` and `MAX_ANGLE` before any movement. The servo physically cannot be commanded outside [0°, 180°]. When the physical arm has mechanical stops, these values will be tightened to match.

### Home position
On boot, the servo immediately goes to 0° (forces a known state), then moves smoothly to 90° (home). This guarantees the software and hardware are in sync at startup — `myServo.read()` after boot returns 90°, not garbage.

```cpp
void homePosition() {
    moveServoSmooth(90, 15);  // slow move to center
}
```

### Known starting position on boot
The line `myServo.write(0); delay(500);` before `homePosition()` forces the servo to a known physical position before any `read()` call. Without this, `read()` returns unpredictable values on the first call (ESP32Servo does not read the actual servo position — it only tracks the last command).

---

## Key Lessons Learned

**`myServo.read()` does not read the physical servo position.** It returns the last angle you wrote. On first boot, before any write, the value is undefined. Always write a known angle before relying on `read()`.

**Common GND is mandatory.** The ESP32 and servo must share the same ground reference. Without it, the PWM signal has no return path and the servo behaves erratically.

**3.3V signal works fine.** ESP32 GPIO outputs 3.3V logic. Standard servo signal is specified at 5V, but the MG90S (and DS3235) accept 3.3V signal correctly. No level shifter needed.

**USB power is not enough for DS3235.** The MG90S draws ~250mA stall — USB can handle that. The DS3235 draws 1–3A under load. USB will collapse and reset the ESP32. An external 6V supply is mandatory for the DS3235.

---

## What Changes for DS3235 (Next Build)

| Item | MG90S Build | DS3235 Build |
|---|---|---|
| Power supply | USB → ESP32 VIN | External 6V PSU → DS3235 directly |
| ESP32 VIN | Powered from USB | Still powered from USB (NOT from 6V PSU) |
| Common GND | ESP32 GND → servo GND | ESP32 GND + PSU GND tied together |
| Capacitor | Not needed | 1000µF across servo power rails (reduces voltage spikes) |
| Angle range | 0°–180° | Will be set to physical range of shoulder joint once confirmed |
| delayMs | 5ms typical | May need tuning — DS3235 is much more powerful, overshoot possible |

**See:** `Electronics/wiring_mg90s_esp32.md` for the DS3235 wiring diagram.

---

## Files

| File | Description |
|---|---|
| `Code/servo_control.ino` | Main sketch — smooth movement, home position, angle limits |
| `Electronics/wiring_mg90s_esp32.md` | Full wiring table, ASCII diagrams for both MG90S and DS3235 setups |
