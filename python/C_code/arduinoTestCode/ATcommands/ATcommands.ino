#include <SoftwareSerial.h>
SoftwareSerial ble(3, 4); // RX | TX
int resetPin = 12;

void setup() {
  // put your setup code here, to run once:
  digitalWrite(resetPin, HIGH);
  pinMode(resetPin, OUTPUT); 
  Serial.begin(2400);
  Serial.println("AT");
  ble.begin(2400); // set HM10 serial at 9600 baud rate
}

void loop() {
  // put your main code here, to run repeatedly:
  if(Serial.available()){
    char ch = Serial.read();
    ble.write(ch);
  }
  if(ble.available()){
    Serial.write(ble.read());
  }
}
