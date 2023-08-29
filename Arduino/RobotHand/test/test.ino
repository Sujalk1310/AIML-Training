#include <Servo.h>
#include <SoftwareSerial.h>
Servo myServo1,myServo2,myServo3,myServo4;
int s1=5;
int s2=6;
int s3=7;
int s4=8;
int bluetoothTx = 10;
int bluetoothRx = 11;
int Signal;
float SignalSmoothed;
float SignalPrev;
SoftwareSerial bluetooth(bluetoothTx,bluetoothRx);
void setup() {
  Serial.begin(9600);
  bluetooth.begin(9600);
  myServo1.attach(s1);
  myServo2.attach(s2);
  myServo3.attach(s3);
  myServo4.attach(s4);
}
void loop() {
  if (bluetooth.available()>= 2) {
    unsigned int servopos = bluetooth.read();
    unsigned int servopos1 = bluetooth.read();
    unsigned int realservo = (servopos1*256)+servopos;
    Serial.println(realservo);
//    if (realservo >= 1040 && realservo <= 1120) {
//      int servo1 = realservo;
//      servo1 = map(servo1,1040,1120,40,120);
//      Signal = servo1*100;
//      SignalSmoothed = (Signal * 0.05) + (SignalPrev * 0.95);
//      SignalPrev = SignalSmoothed;
//      myServo1.write(SignalSmoothed);
//      Serial.println("Height Servo :");
//      Serial.println(SignalSmoothed);
//      delay(10);
//    }
//    if (realservo >= 2050 && realservo <= 2170) {
//      int servo2 = realservo;
//      servo2 = map(servo2,2050,2170,50,170);
//      myServo2.write(servo2);
//      Serial.println("To & Fro Servo :");
//      Serial.println(servo2);
//      delay(10);
//    }
//    if (realservo >= 3000 && realservo <= 3180) {
//      int servo3 = realservo;
//      servo3 = map(servo3,3000,3180,0,180);
//      myServo3.write(servo3);
//      Serial.println("Base Servo :");
//      Serial.println(servo3);
//      delay(10);
//    }
//    if (realservo == 110 || realservo == 20) {
//      int servo4 = realservo;
//      servo4 = map(servo4,20,110,20,110);
//      myServo4.write(servo4);
//      Serial.println("Claw Servo :");
//      Serial.println(servo4);
//      delay(10);
//    }
  }
  delay(10);
}
