#include <SoftwareSerial.h>
SoftwareSerial ble(2, 4); // RX | TX
int resetPin = 12;

void setup() {
  // put your setup code here, to run once:
     digitalWrite(resetPin, HIGH);
  pinMode(resetPin, OUTPUT); 
  Serial.begin(9600);
  Serial.println("HM10 serial started at 9600");
  ble.begin(9600); // set HM10 serial at 9600 baud rate
}

void loop() {
  // put your main code here, to run repeatedly:
  if(Serial.available()){
    char ch = Serial.read();
    ble.write(ch);
    if(ch == ';'){
      Serial.println("reset");
      digitalWrite(resetPin, LOW);
      delay(200);
      digitalWrite(resetPin, HIGH);
    }
    
  }
  if(ble.available()){
    Serial.write(ble.read());
  }
}
