#include <LiquidCrystal.h>
int trig = 9;
int echo = 10;
int contra = 7;
LiquidCrystal lcd(12, 11, 13, 4, 3, 2);
//LcdBarGraph lbg(&lcd, 16, 0,1);
const int trigpin = 9;
const int echopin = 10;
long duration;
float distance;
int door_Height =190;
float length;
float OK = 0;
const int buzzer = 8;

void setup() 
{
  Serial.begin(9600);
  lcd.begin(16,2);
  pinMode(trigpin, OUTPUT);
  pinMode(echopin, INPUT);
  pinMode(contra, OUTPUT);
  pinMode(buzzer,OUTPUT);
  analogWrite(contra,50);
}
void loop() 
{
  lcd.clear();
  lcd.setCursor(1,1);
  lcd.print("GLA University");
  digitalWrite(trigpin, LOW);        
  delayMicroseconds(2);              
  digitalWrite(trigpin, HIGH);
  delayMicroseconds(10);           
  digitalWrite(trigpin, LOW);
  duration = pulseIn(echopin, HIGH);
  distance = duration*0.034/2;
  lcd.setCursor(1,0);
  lcd.print("Height : ");
  length =  (door_Height - distance)/30.48;
  Serial.println(length);
  if (length >= 5.41 && length <= 6.23) {
    lcd.print(length);
    if (OK == length) {
      for (int i = 0;i < 4;i++) {
        tone(buzzer,2500);
        delay(100);
        noTone(buzzer);
        delay(100);
      }
      delay(5000);
    }
    OK = length;
    delay(500);
  }
  else {
    lcd.setCursor(9,0);
    lcd.print("None");
    delay(1000);
  }
}
