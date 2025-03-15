#include <Servo.h>

const int LED_Pin = D5;
const int SERVO_Pin = D4;

const int servo_angle_on = 50;
const int servo_angle_off = 180;

Servo myServo;

void setup() {
  pinMode(LED_Pin, OUTPUT);
  myServo.attach(SERVO_Pin);
}

void loop() {
  // Turn the LED on - when feeding tunnel is open
  digitalWrite(LED_Pin, HIGH);
  myServo.write(servo_angle_on);
  delay(1000);

  // Turn the LED off - when feeding tunnel is closed
  digitalWrite(LED_Pin, LOW);
  myServo.write(servo_angle_off);
  delay(3000);
}