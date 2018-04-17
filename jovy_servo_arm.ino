#include <Servo.h>

/*
 * 6 DoF
 * |- Finger: 70 ~ 110
 * |- Wrist (rotating): 0 ~ 180
 * |- Wrist (bending): 90 ~ 180
 * |- Elbow: 0 ~ 100
 * |- Shoulder: 0 ~ 180
 * └- Base: 0 ~ 180
 * 
 */

Servo servos[6];
int servoPins[6] = {3, 5, 6, 9, 10, 11};
int servoPositions[6] = {90, 120, 20, 180, 60, 110};
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
  delay(1000);

  /*
   *  reading command (interactive)
   */
  if(Serial.available()) {
    cmd = Serial.readStringUntil('\n');
    
    // Get or Set
    char action = cmd.charAt(0);
    if(action == 'g' || action == 'G') {
      
      int spaceIndex = cmd.indexOf(' ');
      int s = cmd.substring(spaceIndex + 1).toInt();
      Serial.println(servoPositions[s]);
      
    } else if(action == 's' || action == 'S') {
      
      int spaceIndex = cmd.indexOf(' ');
      int secondSpaceIndex = cmd.indexOf(' ', spaceIndex + 1);
      int s = cmd.substring(spaceIndex + 1, secondSpaceIndex).toInt();
      int p = cmd.substring(secondSpaceIndex + 1).toInt();
      servoPositions[s] = p;
      Serial.println("done.");
      
    }
  }
}

