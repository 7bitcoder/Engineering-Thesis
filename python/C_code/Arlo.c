#include "simpletools.h"                      // Include simple tools
#include "arlodrive.h"                        // Include arlo drive
#include "fdserial.h"
#include "mstimer.h"

#define INTERRUPT 3
#define LOCKLED 12
#define Rx 2
#define Tx 4
#define false 0
#define true 1
#define halfTurn 500

typedef int bool;
//napięcia na pinach 3.3V
//command frame dates and meaining
//byte 1: device
const char mobileRobot = 1;
const char pc = 2;
//byte 5 additional info
const char empty = 1;
const char commandAccepted = 2;
const char commandExecuted = 3;
const char commandError = 4;
const char robotError = 5;
const char RobotReady = 6;
const char accessDenyed = 7;

const char* secourityCode = "QV9GVE3SYFJ8768CCNL";
//comunication data
char messageId = 1;
int gotBytes = 0;
bool message = false;
char frame[6] = {0};

char deviceId;
char messageIdExternal;
char additionalInfo;
char command;
char commandId;
char executionCommand;
char executionCommandId;

//commands states
enum State{
  locked,
  waiting,
  commandAccept,
  commandExecution,
  commandEnded
};

//commands
const char def = 1;
const char turnLeft = 2;
const char turnRight = 3;
const char turnAround = 4;
const char forward = 5;
const char backward = 6;
const char speedUp = 7;
const char slowDown = 8;
const char biggerTurnAngle = 9;
const char smallerTurnAngle = 10;
const char biggerStep = 11;
const char smallerStep = 12;
const char stopCommand = 13;
const char start = 14;

//connection handle
volatile bool unlock = false;
volatile bool newConnection = false;
volatile bool disconnected = true;
enum State state = waiting;
char formatBuff[200];

//motors movement data
//360 full round 144 ticks

//changing steps with settings 
const int turnOffest = halfTurn/(2*5); //18 deg
const int speedOffest = 127/8; //max 127
const int stepOffest = 80;

const int minSpeed = 10;
const int maxSpeed = 120;
const int maxStep = 800;
const int minStep = 50;
const int maxTurn = halfTurn; //180 deg
const int minTurn = halfTurn/18; //10 deg
//default
int step = halfTurn;
int speed = 30;
int turn = halfTurn/4;

int left = 0;
int right = 0;
int leftEnd = 0;
int rightEnd = 0;

fdserial *ble; //bluetooth serial interface

void test();
bool checkNewConnection();
void checkConnections();
void readData();
void checkData();
void stop();
void setExecutionParameters();
void checkIfExecuted();

//help functions
void setFrame(int a, int b, int c, int d, int e);
int sign(int x){
  if(!x) //0
    return 0;
  else if(x > 0)
    return 1;
  else 
    return -1; 
}  

int main()
{
  ble = fdserial_open(Rx, Tx, 0, 9600);//open ble communication
  test();
  cog_run(checkConnections, 128); // run new connection detector
  while(1){
    if(newConnection){// new connection, check it!!
      unlock = checkNewConnection();
      disconnected = false;
      if(unlock) 
        low(LOCKLED);
      else //if connection is wrong then set lock led
        high(LOCKLED);
    }
    else if(disconnected && unlock ){//if disconnected lock devide
      stop();
      unlock = false;
    }      
    if(unlock) {
      readData();
      if(message)
        checkData();
      if(state == commandExecution){
        checkIfExecuted();
      }        
    }
  }    
}

 void test(){
  char *s;
  freqout(4, 2000, 3000);                     // Beep -> program starting
  print("Program running...\n");              // Program running msg
  s = dhb10_com("HWVER\r");                   // Request hardware version
  print("Hardware\n  HWVER = %s", s);         // Display reply
  s = dhb10_com("VER\r");                     // Request firmware version
  print("Firmware\n  VER = %s", s);           // Display reply
} 

void checkConnections(){
  int state = input(INTERRUPT);
  int lastState = state;
  while(1){
    state = input(INTERRUPT);
    if(state > lastState){
      newConnection = true;
    }   
    else if(state < lastState){
      disconnected = true; 
    }         
    lastState = state;
  }    
}  
bool checkNewConnection(){
  print("begin checkking\n");
  int i=0;
  newConnection = false;
  mstime_start();
  int end = 3000;
  print("time: %d\n", time);
  while( mstime_get() < end) {
    if(fdserial_rxReady(ble) != -1){
      formatBuff[i] = fdserial_rxChar(ble);
      i++;
    }
  }
  mstime_stop();
  formatBuff[i] = '\0';
  print("number of chars from code got: %d\n",i);
  print(formatBuff);
  int secourity = strcmp(formatBuff, secourityCode);
  print("afted check\n");
  if(secourity){
    //wrong code = disconnect
    print("Access to robot denyed\n");
    setFrame(mobileRobot, 1, 1, messageId++, accessDenyed);
    strcpy(frame + 5, "Access denyed");
    dprint(ble, frame);
    return false;
  } else {
    setFrame(mobileRobot, 1, 1, messageId++, RobotReady);
    dprint(ble, frame);
    print("Access to robot confirmed\n");
    return true;
  }   
}

void readData(){
   if(fdserial_rxReady(ble) != -1) { 
    char ch = fdserial_rxChar(ble);
    frame[gotBytes++] = ch;
    //show();
    if(gotBytes == 5){ //got data frame
      message = true;
      gotBytes = 0;
    }    
  }
 
}

void checkData(){
  // check command
    deviceId = frame[0];
    command = frame[1];
    commandId = frame[2];
    messageIdExternal = frame[3];
    additionalInfo = frame[4];
    message = false;
    setExecutionParameters();
}

void stop(){
  drive_speed(0, 0);
  state = waiting;
}  

void setExecutionParameters(){
  if(command == def) //def
      return;
  int signR, signL;
  bool error = false;
  if(command >= speedUp){ //controll setting commands executed instant
   if(command == speedUp){
      speed += speedOffest;
      if(speed > maxSpeed)
        speed = maxSpeed;
     drive_getSpeed(&signR, &signL);
     drive_speed(sign(signR)*speed, sign(signL)*speed);
    } 
    else if(command == slowDown){
      speed -= speedOffest;
      if(speed < minSpeed)
        speed = minSpeed;
     drive_getSpeed(&signR, &signL);
     drive_speed(sign(signR)*speed, sign(signL)*speed);
    } 
    else if(command == biggerTurnAngle){
      turn += turnOffest;
      if(turn > maxTurn)
        turn = maxTurn;
    } 
    else if(command == smallerTurnAngle){
     turn -= turnOffest;
      if(turn < minTurn)
        turn = minTurn;
    } 
    else if(command == biggerStep){
      step += stepOffest;
      if(step > maxStep)
        step = maxStep;
    } 
    else if(command == smallerStep){
      step -= stepOffest;
      if(step < minStep)
        step = minStep;
    } else if(command == stopCommand) {
       stop(); 
    }      
    else{
      error = true;
    }      
    setFrame(mobileRobot, command, commandId, messageId++, error ? commandError : commandExecuted);
    dprint(ble, frame);
    print("komenda nastawcza wykonana, id: %d\n", commandId);
  }
  else { //executable commands  
    drive_feedback(0);
    drive_clearTicks();
    if(command == forward){
      leftEnd = step;
      rightEnd = step;
      drive_speed(speed, speed);
    } else if(command == backward){
      leftEnd = step;
      rightEnd = step;
      drive_speed(-speed, -speed);
    } else if(command == turnLeft){
      leftEnd = turn;
      rightEnd = turn;
      drive_speed(-speed, speed);
    } else if(command == turnRight){
      leftEnd = turn;
      rightEnd = turn;
      drive_speed(speed, -speed);
    } else if(command == turnAround){
      leftEnd = halfTurn;
      rightEnd = halfTurn;
      drive_speed(speed, -speed);
    } else {
      error = true;
    }
    setFrame(mobileRobot, command, commandId, messageId++, error ? commandError : commandAccepted);
    dprint(ble, frame);
    print(frame);
    //show();
    state = commandExecution;
    executionCommand = command;
    executionCommandId = commandId;
    print("komenda w trakcie wykonywania, id: %d\n", commandId);
  }  
}    

void checkIfExecuted(){
  drive_getTicks(&left, &right);
  if (abs(left) > leftEnd || left < -leftEnd  || right > rightEnd || right < -rightEnd){
    stop(); 
    setFrame(mobileRobot, command, commandId, messageId++, commandExecuted);
    dprint(ble, frame);
    print(frame);
    //show();
    print("komenda wykonana, id: %d\n", commandId);
  }     
}  


void setFrame(int a, int b, int c, int d, int e){
    frame[0] = a;
    frame[1] = b;
    frame[2] = c;
    frame[3] = d;
    frame[4] = e;
    frame[5] = '\0';
}
