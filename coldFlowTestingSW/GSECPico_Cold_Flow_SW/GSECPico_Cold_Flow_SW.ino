#include <Servo.h>
Servo mainServo; //Initialize servo object
const int MAIN_PWM_PIN = 6; //Attach servo to GPIO 6 (pin 9)
const int MAIN_CMD_PIN = 7; //Specify the servo logic command pin as GPIO 7 (pin 10)
const int CTRL_ANGLE = 90; //Define the angle that means "open"

void setup() {
  mainServo.attach(MAIN_PWM_PIN);
  pinMode(MAIN_CMD_PIN, INPUT);
}

//Detect if the logic control data pin's state, and adjust the position of the servo accordingly
void loop() {
  if (digitalRead(0) == LOW) { //Logic "flipped" due to GSEC's (a Raspberry Pi 5) GPIO being set to high upon bootup on output pin. Adjust accordingly, if different GSEC GPIO used
    mainServo.write(CTRL_ANGLE);
  }
  if (digitalRead(0) == HIGH) {
    mainServo.write(0);
  }
  
}