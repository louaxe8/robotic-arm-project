// ============================================================
// servo_control.ino
// ESP32 + MG90S Servo — Learning Build
// Lou | May 2026
//
// Features:
// - Smooth servo movement (one degree at a time)
// - Angle limits with constrain()
// - Home position function
// - Known starting position on boot
// ============================================================

#include <ESP32Servo.h>

// --- Angle limits ---
const int MIN_ANGLE = 0;
const int MAX_ANGLE = 180;

// --- Pin and servo object ---
const int SERVO_PIN = 18;
Servo myServo;

void setup() {
  Serial.begin(115200);
  Serial.println("Servo control starting...");
  myServo.attach(SERVO_PIN);

  // Force known starting position before any read()
  myServo.write(0);
  delay(500);

  homePosition();
}

void loop() {
  Serial.println("Moving to 0 degrees");
  moveServoSmooth(0, 5);
  delay(1000);

  Serial.println("Moving to 90 degrees");
  moveServoSmooth(90, 5);
  delay(1000);

  Serial.println("Moving to 180 degrees");
  moveServoSmooth(180, 5);
  delay(1000);

  Serial.println("Moving to 90 degrees");
  moveServoSmooth(90, 5);
  delay(3000);
}

void moveServoSmooth(int targetAngle, int delayMs) {
  targetAngle = constrain(targetAngle, MIN_ANGLE, MAX_ANGLE);
  int currentAngle = myServo.read();
  while (currentAngle != targetAngle) {
    if (targetAngle > currentAngle) {
      currentAngle++;
      myServo.write(currentAngle);
      delay(delayMs);
    }
    else if (targetAngle < currentAngle) {
      currentAngle--;
      myServo.write(currentAngle);
      delay(delayMs);
    }
  }
}

void homePosition() {
  moveServoSmooth(90, 15);
}
