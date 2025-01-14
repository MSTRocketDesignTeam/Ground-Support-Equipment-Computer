
#include <Servo.h>

//this code also works on an LED, making it cycle through brighter and dimmer
Servo myservo;  // create servo object to control a servo
// twelve servo objects can be created on most boards

int pos = 0;    // variable to store the servo position

void setup() {
  myservo.attach(6);  // attaches the servo on pin 9 to the servo object
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