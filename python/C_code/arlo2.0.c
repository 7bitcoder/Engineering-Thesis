/*
  XBee UART Loopback.c
*/

#include "simpletools.h"
#include "fdserial.h"
#include "arlodrive.h"

volatile fdserial *xbee;
volatile int ready = 0;
volatile int commandEnded = 0;
volatile int emergency = 0;
volatile int speedL = 0;
volatile int speedR = 0;
volatile int end = 500;

void myWait() {
  while(fdserial_rxReady(xbee) == -1)
    ;      
};

void getData() {
  xbee = fdserial_open(1,2, 0, 9600);
  //dprint(xbee, "Click this terminal, \n");
  //dprint(xbee, "and type on keyboard...\n\n");
  char c = 1;
  while(1){
    //dprint(xbee, "begin\n"); 
    //freqout(4, 500, 2000);  
    while(c != 184)
      c = fdserial_rxChar(xbee);
    myWait();
    c = fdserial_rxChar(xbee);
    speedL = 127 - (int)c;
    if(!speedL){
     emergency = 1;
     continue; 
    }      
    //dprint(xbee, "You typed: %d %d %d\n", speedR, speedL, end);
    myWait();
    c = fdserial_rxChar(xbee);
    speedR = 127 - (int)c;
    if(!speedR){
     emergency = 1;
     continue;
    }
    //dprint(xbee, "You typed: %d %d %d\n", speedR, speedL, end);
    myWait();
    c = fdserial_rxChar(xbee);
    end = 4 * (int)c;
    if(!end){
     emergency = 1;
     continue; 
    }
    //dprint(xbee, "You typed: %d %d %d\n", speedR, speedL, end);
    ready = 1;
    while(ready){
        if(fdserial_rxReady(xbee) == 1){
          c = fdserial_rxChar(xbee);
          emergency = 1;
        }                   
    }      
    commandEnded = 0; 
    //freqout(4, 500, 3000);  
    dprint(xbee, "r");        
    //freqout(4, 500, 3000);  
  }  
}

int main()
{
  int ticksL = 0;
  int ticksR = 0; 
  freqout(4, 500, 2000);   
  //print("starting\n");
  cog_run(getData, 128);  
  

  drive_feedback(0);                          // Disable encoder feedback
  drive_clearTicks(); 
 
  while(1)
  {
    //print("before\n");
    while(!ready)
      ;
    freqout(4, 500, 3000);
    //print("before2\n");
    drive_clearTicks();
    drive_speed(speedL, speedR);
    ticksR = 0;
    //print("before3\n");                        // 20/127 of full power to motors
    while(abs(ticksR) < end && !emergency)
      drive_getTicks(&ticksL, &ticksR);
    drive_speed(0,0);
    emergency = 0;
    ready = 0;
    freqout(4, 500, 3000);
    //print("before4\n");
  }  
}