/*
 One Shot
 Kudos to marguskohv - he sowed the seed....
Serial monitor is just aide memoire
 */
#include <SoftwareSerial.h>
SoftwareSerial HM10(2, 4); // RX | TX

void setup()
{
  Serial.begin(9600);
  Serial.println("HM10 serial started at 9600");
  HM10.begin(9600); // set HM10 serial at 9600 baud rate
}

void loop()
{
  if(HM10.available()) {   // if HM10 sends something then read
    Serial.write(HM10.read());
  }
  if (Serial.available()) {           // Read user input if available.
    HM10.write(Serial.read());
  }
}
