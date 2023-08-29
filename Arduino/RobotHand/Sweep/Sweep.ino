/* Sweep
 by BARRAGAN <http://barraganstudio.com>
 This example code is in the public domain.

 modified 8 Nov 2013
 by Scott Fitzgerald
 https://www.arduino.cc/en/Tutorial/LibraryExamples/Sweep
*/

#include <Servo.h>

Servo myservo1,myservo2,myservo3,myservo4;  // create servo object to control a servo
// twelve servo objects can be created on most boards

int pos = 90;    // variable to store the servo position

void setup() {
  myservo1.attach(5);
  myservo2.attach(6);
  myservo3.attach(7);
  myservo4.attach(8);
  myservo1.write(pos);
  myservo2.write(pos);
  myservo3.write(pos);
  myservo4.write(pos);// attaches the servo on pin 9 to the servo object
} // 40 - 120 3 height
// 50-170 2 To Fro
// 0-180 1 BASE
// 20-110 4 Claw

void loop() {
  for (pos = 0; pos <= 110; pos += 1) { // goes from 0 degrees to 180 degrees
    // in steps of 1 degree
    myservo4.write(pos);              // tell servo to go to position in variable 'pos'
    delay(15);                       // waits 15 ms for the servo to reach the position
  }
  delay(2000);
  for (pos = 110; pos >= 20; pos -= 1) { // goes from 180 degrees to 0 degrees
    myservo4.write(pos);              // tell servo to go to position in variable 'pos'
    delay(15);                       // waits 15 ms for the servo to reach the position
  }
  delay(4000);
 
}
