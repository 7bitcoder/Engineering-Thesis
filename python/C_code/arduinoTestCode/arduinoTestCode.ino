/*
 One Shot
 Kudos to marguskohv - he sowed the seed....
Serial monitor is just aide memoire
 */
#include <SoftwareSerial.h>
SoftwareSerial ble(2, 4); // RX | TX
#define INTERRUPT 3

namespace indentificator{
  const char mobileRobot = 1;
  const char pc = 2;
  const char empty = 1;
  const char commandAccepted = 2;
  const char commandExecuted = 3;
  const char commandError = 4;
  const char robotError = 5;
}
const char* secourityCode = "V9GV-LSYF-876G-CCNL";
char messageId = 1;
int gotBytes = 0;
bool message = false;
char frame[6] = {0};

char deviceId = frame[0];
char messageIdExternal = frame[1];
char additionalInfo = frame[2];
char command = frame[3];
char commandId = frame[4];

    
enum State{
  waiting,
  commandAccept,
  commandExecutution,
  commandEnded
};

int resetPin = 12;
bool newConnection = false;
State state = State::waiting;
char formatBuff[200];
void interrupt(){
  Serial.println("new Connection");
  newConnection = true;
}
void setup()
{
    digitalWrite(resetPin, HIGH);
  pinMode(resetPin, OUTPUT);   
  Serial.begin(9600);
  Serial.println("HM10 serial started at 9600");
  ble.begin(9600); // set HM10 serial at 9600 baud rate
  attachInterrupt(digitalPinToInterrupt(INTERRUPT), interrupt, RISING);
}
void show(){
  sprintf(formatBuff, "Bajt1 = %d, Bajt2 = %d, Bajt3: = %d, Bajt4 = %d, Bajt5 = %d",int(frame[0]),int(frame[1]),int(frame[2]),int(frame[3]),int(frame[4]) );
  Serial.println(formatBuff);
}
void loop()
{
  if(newConnection){
    int i=0;
    Serial.println("go");
    unsigned long time = millis() + 3000;
    Serial.println("after");
    while( millis() < time) {
      while(ble.available()){
        formatBuff[i] = ble.read();
        i++;
      }
    }
    formatBuff[i] = '\0';
    int secourity = strcmp(formatBuff, secourityCode);
    if(secourity){
      //wrong code = disconnect
      Serial.println("wrong code");
      Serial.println(formatBuff);
      Serial.println(i);
      digitalWrite(resetPin, LOW); //cut off ble power for 200ms
      delay(200);
      digitalWrite(resetPin, HIGH);
    } else {
     Serial.println("OK");
    }
    newConnection = false;
  }
  if(ble.available() == 5) {   // if HM10 sends something then read
    int i = 5;
    while(i--){
    char ch = ble.read();
    frame[gotBytes++] = ch;
    }
    //show();
    message = true;
    gotBytes = 0;
  }
  if (message) {           // Read user input if available.
    deviceId = frame[0];
    messageIdExternal = frame[1];
    additionalInfo = frame[2];
    command = frame[3];
    commandId = frame[4];
    frame[0] = indentificator::mobileRobot;
    frame[3] = messageId++;
    frame[4] = indentificator::commandAccepted;
    frame[1] = command;
    frame[2] = commandId;
    frame[5] = '\0';
    ble.write(frame, 5);
    Serial.write(frame, 5);
    show();
    state = State::commandAccept;
    message = false;
    Serial.print("komenda w trakcie wykonywania, id: ");
    Serial.println(int(commandId));
    delay(5000);
    frame[4] = indentificator::commandExecuted;
    frame[3] = messageId++;
    ble.write(frame, 5);
    Serial.write(frame, 5);
    show();
    state = State::commandEnded;
    Serial.print("komenda wykonana, id: ");
    Serial.println(int(commandId));
  }
}
