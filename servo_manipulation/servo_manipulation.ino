#include <Servo.h>

Servo servos[6];
// servo order: Finder(0) - Base(5)
int servoPins[6] = {3, 5, 6, 9, 10, 11};
int servoPositions[6] = {180, 90, 90, 90, 90, 0};
String cmd;

void setup() {
  Serial.begin(9600);

  /* 
   * attach the servos 
   */
  for(int i=0; i< 6; i++) {
    servos[i].attach(servoPins[i]);
  }
  
  /*
   * read initial positions
   */
//  for(int i=0; i<6; i++) {
//    Serial.println(servos[i].read());
//  }
}

void loop() {

  /*
   *  writing to servos
   */
  
  for(int i=0; i<6; i++) {
    servos[i].write(servoPositions[i]);
  }
  delay(100);

  /*
   *  reading command (interactive)
   */
  if(Serial.available()) {
    cmd = Serial.readStringUntil('\n');
    int startIndex = 0;
    for(int i=0; i<6; i++) {
      int spaceIndex = cmd.indexOf(' ', startIndex);
      int value = cmd.substring(startIndex, spaceIndex).toInt();
      servoPositions[i] = value;
      Serial.println(value);
      startIndex = spaceIndex + 1;
    }
    Serial.println("done.");
  }
}

