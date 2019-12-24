/*
 One Shot
 Kudos to marguskohv - he sowed the seed....
Serial monitor is just aide memoire
 */
#include <SoftwareSerial.h>
SoftwareSerial ble(2, 4); // RX | TX
#define INTERRUPT 3
#define LOCKLED 12

namespace indentificator{
  const char mobileRobot = 1;
  const char pc = 2;
  const char empty = 1;
  const char commandAccepted = 2;
  const char commandExecuted = 3;
  const char commandError = 4;
  const char robotError = 5;
  const char RobotReady = 6;
  const char accessDenyed = 7;
}
const char* secourityCode = "QV9GVE3SYFJ8768CCNL";
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

bool unlock = false;
int resetPin = 12;
bool newConnection = false;
State state = State::waiting;
char formatBuff[200];

void interrupt(){
  Serial.println("new Connection");
  newConnection = true;
}

void show(){
  sprintf(formatBuff, "Bajt1 = %d, Bajt2 = %d, Bajt3: = %d, Bajt4 = %d, Bajt5 = %d",int(frame[0]),int(frame[1]),int(frame[2]),int(frame[3]),int(frame[4]) );
  Serial.println(formatBuff);
}
bool checkNewConnection();
void readData();
void checkData();

void setup()
{
  pinMode(LOCKLED, OUTPUT);
  digitalWrite(LOCKLED, LOW);
  Serial.begin(9600);
  Serial.println("Robot Started");
  ble.begin(9600); // set HM10 serial at 9600 baud rate
  attachInterrupt(digitalPinToInterrupt(INTERRUPT), interrupt, RISING);
}

void loop()
{
  if(newConnection){
    unlock = checkNewConnection();
    digitalWrite(LOCKLED, unlock ? LOW : HIGH);
  }
  if(unlock) {
    readData();
    checkData();
  }
}

bool checkNewConnection(){
  int i=0;
    newConnection = false;
    unsigned long time = millis() + 3000;
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
      Serial.println("Access to robot denyed");
    frame[0] = indentificator::mobileRobot;
    frame[1] = 1;
    frame[2] = 1;
    frame[3] = messageId++;
    frame[4] = indentificator::accessDenyed;
    frame[5] = '\0';
    strcpy(frame + 5, "Access denyed");
    ble.write(frame);
    return false;
    } else {
    frame[0] = indentificator::mobileRobot;
    frame[1] = 1;
    frame[2] = 1;
    frame[3] = messageId++;
    frame[4] = indentificator::RobotReady;
    frame[5] = '\0';
    ble.write(frame, 5);
    Serial.println("Access to robot confirmed");
    return true;
    }
    
}

void readData(){
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
 
}
void checkData(){
   if (message) {           // Read user input if available.
    deviceId = frame[0];
    command = frame[1];
    commandId = frame[2];
    messageIdExternal = frame[3];
    additionalInfo = frame[4];

    frame[0] = indentificator::mobileRobot;
    frame[1] = command;
    frame[2] = commandId;
    frame[3] = messageId++;
    frame[4] = indentificator::commandAccepted;
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
