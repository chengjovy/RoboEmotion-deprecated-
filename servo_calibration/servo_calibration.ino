#include <Servo.h>

int SERVO_PIN = 9;

Servo servo;
int counter;


void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  counter = 0;
  servo.attach(SERVO_PIN);
}

void loop() {
  servo.write(0);
  return;
  // put your main code here, to run repeatedly:
  for(int pos=0; pos<=180; pos += 20) {
    servo.write(pos);
    delay(100);
  }
  for(int pos=180; pos>=0; pos -= 20) {
    servo.write(pos);
    delay(100);
  }
  counter += 1;
}
