#include <SoftwareSerial.h>
SoftwareSerial arlo(4, 5); // RX | TX
int resetPin = 12;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  arlo.begin(2400);
  Serial.println("AT");
}

void loop() {
  // put your main code here, to run repeatedly:
  if(Serial.available()){
    char ch = Serial.read();
    Serial.write(ch);
    arlo.write(ch);
  }
    if(arlo.available()){
    char ch = arlo.read();
    Serial.write(ch);
  }
}
