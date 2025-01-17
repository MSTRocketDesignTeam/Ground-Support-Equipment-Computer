
#include <Servo.h>

Servo myservo;  // create servo object to control a servo

int pos = 0;

void setup() {
  myservo.attach(6);  // attaches the servo on pin 9 (GPIO6) to the servo object
  pinMode(0, INPUT);
  pinMode(1, INPUT);
}

void loop() {
  if (digitalRead(0) == HIGH) {
    myservo.write(90);
  }
  if (digitalRead(0) == LOW) {
    myservo.write(0);
  }
  
}