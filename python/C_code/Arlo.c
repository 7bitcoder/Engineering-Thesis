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
typedef int bool;
//napięcia na pinach 3.3V
bool sa = true;
const char mobileRobot = 1;
const char pc = 2;
const char empty = 1;
const char commandAccepted = 2;
const char commandExecuted = 3;
const char commandError = 4;
const char robotError = 5;
const char RobotReady = 6;
const char accessDenyed = 7;

const char* secourityCode = "QV9GVE3SYFJ8768CCNL";

char messageId = 1;
int gotBytes = 0;
bool message = false;
char frame[6] = {0};

char deviceId;
char messageIdExternal;
char additionalInfo;
char command;
char commandId;

enum State{
  waiting,
  commandAccept,
  commandExecutution,
  commandEnded
};

volatile bool unlock = false;
volatile bool newConnection = false;
enum State state = waiting;
char formatBuff[200];

fdserial *ble; //bluetooth serial interface

void test();
bool checkNewConnection();
void checkConnections();
void readData();
void checkData();

int main()                                    // Main function
{
  ble = fdserial_open(Rx, Tx, 0, 9600);//open ble communication
  test();
  cog_run(checkConnections, 128);
  while(1){
    if(newConnection){
      unlock = checkNewConnection();
      if(unlock) // error led state
        low(LOCKLED);
      else
        high(LOCKLED);
    }
    if(unlock) {
      readData();
      if(message)
        checkData();
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
    frame[0] = mobileRobot;
    frame[1] = 1;
    frame[2] = 1;
    frame[3] = messageId++;
    frame[4] = accessDenyed;
    frame[5] = '\0';
    strcpy(frame + 5, "Access denyed");
    dprint(ble, frame);
    return false;
  } else {
    frame[0] = mobileRobot;
    frame[1] = 1;
    frame[2] = 1;
    frame[3] = messageId++;
    frame[4] = RobotReady;
    frame[5] = '\0';
    dprint(ble, frame);
    print("Access to robot confirmed\n");
    return true;
  }   
}

void readData(){
   if(fdserial_rxReady(ble) != -1) {   // if HM10 sends something then read
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

    frame[0] = mobileRobot;
    frame[1] = command;
    frame[2] = commandId;
    frame[3] = messageId++;
    frame[4] = commandAccepted;
    frame[5] = '\0';
    dprint(ble, frame);
    print(frame);
    //show();
    state = commandAccept;
    message = false;
    print("komenda w trakcie wykonywania, id: %d\n", commandId);
    pause(5000);
    frame[4] = commandExecuted;
    frame[3] = messageId++;
    dprint(ble, frame);
    print(frame);
    //show();
    state = commandEnded;
    print("komenda wykonana, id: %d\n", commandId);
}