#include <Servo.h>
Servo myservo; //Initialize servo object

void setup() {
  Serial.begin(115200); // Initialize serial communication
  randomSeed(analogRead(0));
  myservo.attach(6); //Attach servo to GPIO 6 (pin 9)
  pinMode(0, INPUT); //Specify the servo logic control data pin as GPIO 0 (pin 1)
}

void loop() {
  int randomNumbers[7]; 
  // Generate 7 random integers and store them in an array
  for (int i = 0; i < 7; i++) {
    randomNumbers[i] = random(0, 100); // Random integer between 0 and 99
  }
  
  //Send the random integers to the GSEC
  for (int i = 0; i < 7; i++) {
    Serial.print(randomNumbers[i]);
    Serial.print(" ");  //Space-separated values
  }
  Serial.println();  //Newline to indicate end of data

  //Detect if the logic control data pin's state, and adjust the position of the servo accordingly
  if (digitalRead(0) == HIGH) {
    myservo.write(90);
  }
  if (digitalRead(0) == LOW) {
    myservo.write(0);
  }
}

