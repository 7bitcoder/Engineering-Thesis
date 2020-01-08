#include "arlodrive.h"                        // Include arlo drive
#include "fdserial.h"
#include "mstimer.h"
#include "simpletools.h"  

#define INTERRUPT 3
#define LOCKLED 12
#define Rx 9
#define Tx 11
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

const char* secourityCode = "QV9";
const char* secourityCode2 = "Q9GVE3SYFJ8768CCN";
//comunication data
char messageId = 1;
int gotBytes = 0;
bool message = false;
volatile char frame[6] = {0};

volatile char deviceId;
volatile char messageIdExternal;
volatile char additionalInfo;
volatile char command;
volatile char commandId;
volatile char executionCommand;
volatile char executionCommandId;

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
char formatBuff[20];

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
int speed = 50;
int turn = halfTurn/4;

int left = 0;
int right = 0;
int leftEnd = 0;
int rightEnd = 0;

fdserial *ble; //bluetooth serial interface
fdserial *arduino; //bluetooth serial interface

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
  bool driving = false;
  int setSpeedL = 0;
  int setSpeedR = 0;
  drive_feedback(0);                          // Disable encoder feedback
  drive_clearTicks();    
      // Disable encoder feedback
  ble = fdserial_open(Rx, Tx, 0, 2400);//open ble communication
  arduino = fdserial_open(0,1, 0, 9600);//open ble communication
  test();
  //drive_feedback(0);                          // Disable encoder feedback                         // Clear encoder values
  stop();
  cog_run(checkConnections, 40); // run new connection detector
  dprint(arduino, "halo");
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
      if(message){
       deviceId = frame[0];
       command = frame[1];
       commandId = frame[2];
       messageIdExternal = frame[3];
       additionalInfo = frame[4];
       message = false;
      if(command == def){ //def
          return;
        print("def\n");      
      }      
      int signR, signL;
      bool error = false;
      if(command >= speedUp){ //controll setting commands executed instant
       print("noramal commands\n");
       if(command == speedUp){
         print("Speedup\n");
          speed += speedOffest;
          if(speed > maxSpeed)
            speed = maxSpeed;
         } 
        else if(command == slowDown){
          print("Slow dup\n");
          speed -= speedOffest;
          if(speed < minSpeed)
            speed = minSpeed;
         } 
        else if(command == biggerTurnAngle){
          print("bigget dup\n");
          turn += turnOffest;
          if(turn > maxTurn)
            turn = maxTurn;
        } 
        else if(command == smallerTurnAngle){
          print("smaller dup\n");
         turn -= turnOffest;
          if(turn < minTurn)
            turn = minTurn;
        } 
        else if(command == biggerStep){
          print("biget step dup\n");
          step += stepOffest;
          if(step > maxStep)
            step = maxStep;
        } 
        else if(command == smallerStep){
          print("amsller step\n");
          step -= stepOffest;
          if(step < minStep)
            step = minStep;
        } else if(command == stopCommand) {
          print("Stop\n");
           stop(); 
        }      
        else{
          error = true;
          print("else\n");
        }      
        dprint(arduino, "exectuaoidsjasdjal xD\n");
        print("komenda nastawcza wykonana, id: %d\n", commandId);
        frame[0] = mobileRobot;
        frame[1] = command;
        frame[2] = commandId;
        frame[3] = messageId++;
        frame[4] = error ? commandError : commandExecuted;
        frame[5] = '\0';
        dprint(arduino, "kaj\n");
        print(frame);
        dprint(ble, frame);
        print("dended");
        }
      else { //executable commands  
      print("executable commands\n");
      //drive_clearTicks();    
        if(command == forward){
          print("forward, %d\n", speed);
          leftEnd = step;
          rightEnd = step;
          setSpeedL = speed;
          setSpeedR = speed;
          driving = true;
          print("after, %d\n", speed);
        } else if(command == backward){
          print("fback\n");
          leftEnd = step;
          rightEnd = step;
          drive_speed(-speed, -speed);
        } else if(command == turnLeft){
          print("letf\n");
          leftEnd = turn;
          rightEnd = turn;
          drive_speed(-speed, speed);
        } else if(command == turnRight){
          print("right\n");
          leftEnd = turn;
          rightEnd = turn;
          drive_speed(speed, -speed);
        } else if(command == turnAround){
          leftEnd = halfTurn;
          print("around\n");
          rightEnd = halfTurn;
          drive_speed(speed, -speed);
        } else {
          error = true;
          print("else\n");
        }
        frame[0] = mobileRobot;
        frame[1] = command;
        frame[2] = commandId;
        frame[3] = messageId++;
        frame[4] = error ? commandError : commandExecution;
        frame[5] = '\0';
        dprint(ble, frame);
        state = commandExecution;
        executionCommand = command;
        executionCommandId = commandId;
        print("komenda w trakcie wykonywania, id: %d\n", commandId);
      }  
      }  
               
      if(state == commandExecution){
        //checkIfExecuted();
      }        
    }
    if(1){
      print("driving %d %d", setSpeedL, setSpeedR);
      pause(3000);
      drive_speed(speed,speed);
      pause(3000);
      drive_speed(0,0);
      driving = false;  
     }     
     if(driving){
        print("driving2 %d %d", setSpeedL, setSpeedR);
       pause(3000);
      drive_speed(speed, speed);
      pause(3000);
      drive_speed(0,0); 
      unlock = true;
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
  mstime_reset();
  mstime_start();
  int end = 3000;
  int len = strlen(secourityCode);
  while( mstime_get() < end) {
    ///print("get %d", mstime_get());
    if(fdserial_rxReady(ble) != -1){
      char ch = fdserial_rxChar(ble);
      formatBuff[i] = ch;
      i++;
      print("got new char %d\n", i);
      print("time: %d %c\n", mstime_get(),ch );
      if(i == len)
        break;
    }
  }
  mstime_stop();
  formatBuff[i] = '\0';
  print("number of chars from code got: %d\n",i);
  print(formatBuff);
  int secourity = strcmp(formatBuff, secourityCode);
  print("after check\n");
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
    dprint(arduino, "yeeesoiajdisoadjadawdAD");
    return true;
  }   
}

void readData(){
  print("reading data\n");
   if(fdserial_rxReady(ble) != -1) { 
    char ch = fdserial_rxChar(ble);
    frame[gotBytes++] = ch;
    print("%d\n", ch);
    //show();
    if(gotBytes == 5){ //got data frame
    print("got data\n");
    dprint(arduino, "mam data\n");
      message = true;
      gotBytes = 0;
    }    
  }
 
}

void stop(){
  drive_speed(0, 0);
  state = waiting;
}  

void setExecutionParameters(){
  
}    

void checkIfExecuted(){
  drive_getTicks(&left, &right);
  int get = abs(right);
  if ( get > rightEnd){
    stop(); 
    setFrame(mobileRobot, command, commandId, messageId++, commandExecuted);
    dprint(arduino, frame);
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
    print("frame setting");
}
