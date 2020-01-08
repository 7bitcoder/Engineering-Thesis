/*
  One Shot
  Kudos to marguskohv - he sowed the seed....
  Serial monitor is just aide memoire
*/
#include "SoftwareSerial.h"

SoftwareSerial ble(3, 4); // RX | TX
SoftwareSerial arlo(5, 6); // RX | TX
#define INTERRUPT 2
#define LOCKLED 12
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
enum State {
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
char formatBuff[30];

//motors movement data
//360 full round 144 ticks

//changing steps with settings
const int turnOffest = halfTurn / (2 * 5); //18 deg
const int speedOffest = 127 / 8; //max 127
const int stepOffest = 80;

const int minSpeed = 10;
const int maxSpeed = 120;
const int maxStep = 800;
const int minStep = 50;
const int maxTurn = halfTurn; //180 deg
const int minTurn = halfTurn / 18; //10 deg
//default
int step = halfTurn;
int speed = 50;
int turn = halfTurn / 4;

int left = 0;
int right = 0;
int leftEnd = 0;
int rightEnd = 0;

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
int sign(int x) {
  if (!x) //0
    return 0;
  else if (x > 0)
    return 1;
  else
    return -1;
}

void interrupt() {
  Serial.println("new Connection");
  newConnection = true;
}

void show() {
  sprintf(formatBuff, "Bajt1 = %d, Bajt2 = %d, Bajt3: = %d, Bajt4 = %d, Bajt5 = %d", int(frame[0]), int(frame[1]), int(frame[2]), int(frame[3]), int(frame[4]) );
  Serial.println(formatBuff);
  sprintf(formatBuff, "device = %d, commnad = %d, commandid = %d, messageid= %d, additional info= %d", deviceId, command, commandId, messageId, additionalInfo);
  Serial.println(formatBuff);
}
unsigned long beg = 0;
void drive_speed(int left, int right, int endD);
void setup()
{
  pinMode(LOCKLED, OUTPUT);
  digitalWrite(LOCKLED, LOW);
  Serial.begin(115200);
  Serial.println("Robot Started");
  ble.begin(2400); // set HM10 serial at 9600 baud rate
  char c = '?';
  //arlo.begin(9600);
  while(c == '?')
    c = arlo.read();
  Serial.println("yes started");
  attachInterrupt(digitalPinToInterrupt(INTERRUPT), interrupt, RISING);
}

void loop()
{
  if (newConnection) { // new connection, check it!!
    unlock = checkNewConnection();
    if (unlock)
      digitalWrite(LOCKLED, LOW);
    else //if connection is wrong then set lock led
      digitalWrite(LOCKLED, HIGH);
  }
  if (unlock) {
    readData();
    if (message)
      checkData();
    if (state == commandExecution) {
      checkIfExecuted();
    }
  }
}

bool checkNewConnection() {
  Serial.println("eg11111!!!!!!");
  int i = 0;
  newConnection = false;
  unsigned long time = millis() + 5000;
  Serial.println(time);
  while ( millis() < time) {
    while (ble.available()) {
      formatBuff[i] = ble.read();
      i++;
    }
  }
  formatBuff[i] = '\0';
  Serial.println(i);
  Serial.println(formatBuff);
  int secourity = 0;//strcmp(formatBuff, secourityCode);
  Serial.println("hereqwq qwd");
  if (secourity) {
    //wrong code = disconnect
    Serial.println("Access to robot denyed");
    setFrame(mobileRobot, 1, 1, messageId++, accessDenyed);
    strcpy(frame + 5, "Access denyed");
    ble.write(frame);
    return false;
  } else {
    setFrame(mobileRobot, 1, 1, messageId++, RobotReady);
    ble.write(frame, 5);
    Serial.println("Access to robot confirmed");
    return true;
  }

}

void readData() {
  if (ble.available()) {  // if HM10 sends something then read
    int i = 5;
    Serial.println("get");
    while (i--) {
      char ch = ble.read();
      frame[gotBytes++] = ch;
    }
    show();
    message = true;
    gotBytes = 0;
  }

}

void drive_speed(int , int) {

}

void checkData() {
  // check command
  Serial.println("checking data");
  deviceId = frame[0];
  command = frame[1];
  commandId = frame[2];
  messageIdExternal = frame[3];
  additionalInfo = frame[4];
  message = false;
  setExecutionParameters();
  //show();
  delay(100);
}

void stop() {
  Serial.println("stop");
  drive_speed(0, 0);
  state = waiting;
}

void setExecutionParameters() {
  Serial.println("exec params");
  if (command == def) { //def
    Serial.println("default");
    return;
  }
  if (command >= speedUp) { //controll setting commands executed instant
    Serial.println("settings");
    int signR, signL;
    bool error = false;
    if (command == speedUp) {
      speed += speedOffest;
      if (speed > maxSpeed)
        speed = maxSpeed;
    } else if (command == slowDown) {
      speed -= speedOffest;
      if (speed < minSpeed)
        speed = minSpeed;
    } else if (command == biggerTurnAngle) {
      turn += turnOffest;
      if (turn > maxTurn)
        turn = maxTurn;
    } else if (command == smallerTurnAngle) {
      turn -= turnOffest;
      if (turn < minTurn)
        turn = minTurn;
    } else if (command == biggerStep) {
      step += stepOffest;
      if (step > maxStep)
        step = maxStep;
    } else if (command == smallerStep) {
      step -= stepOffest;
      if (step < minStep)
        step = minStep;
    } else if (command == stopCommand) {
      stop();
    } else {
      error = true;
    }
    Serial.println("sending");
    setFrame(mobileRobot, command, commandId, messageId++, error ? commandError : commandExecuted);
    ble.write(frame, 5);
    Serial.print("komenda: ");
    Serial.println(int(command));
    Serial.print("komenda nastawcza wykonana, id: ");
    Serial.println(int(commandId));
  } else { //executable commands
    Serial.println("executalebe");
    bool error = false;
    if (command == forward) {
      leftEnd = step;
      rightEnd = step;
      drive_speed(speed, speed, step);
    } else if (command == backward) {
      leftEnd = step;
      rightEnd = step;
      drive_speed(-speed, -speed, step);
    } else if (command == turnLeft) {
      leftEnd = turn;
      rightEnd = turn;
      drive_speed(-speed, speed, turn);
    } else if (command == turnRight) {
      leftEnd = turn;
      rightEnd = turn;
      drive_speed(speed, -speed, turn);
    } else if (command == turnAround) {
      leftEnd = halfTurn;
      rightEnd = halfTurn;
      drive_speed(speed, -speed, halfTurn);
    } else {
      error = true;
    }
    setFrame(mobileRobot, command, commandId, messageId++, error ? commandError : commandAccepted);
    ble.write( frame, 5);
    Serial.print(frame);
    //show();
    state = commandExecution;
    executionCommand = command;
    executionCommandId = commandId;
    Serial.print("komenda: ");
    Serial.println(int(command));
    Serial.print("komenda w trakcie wykonywania, id: ");
    Serial.println(int(commandId));
  }
}

void checkIfExecuted() {
  if (arlo.available()) {
    char ch = ble.read();
    if(ch == 'r')
    Serial.println("OK");
    stop();
    setFrame(mobileRobot, command, commandId, messageId++, commandExecuted);
    ble.write(frame, 5);
    Serial.print(frame);
    //show();
    Serial.print("komenda: ");
    Serial.println(int(executionCommand));
    Serial.print("komenda wykonana, id: ");
    Serial.println(int(executionCommandId));
  }
}

void drive_speed(int left, int right, int endD){
char sec = 184;
arlo.write(sec);
char cleft = 127 + left;
arlo.write(cleft);
char cright = 127 + right;
arlo.write(cright);
char cend = 200; //endD;
arlo.write(cend);
}

void setFrame(int a, int b, int c, int d, int e) {
  frame[0] = a;
  frame[1] = b;
  frame[2] = c;
  frame[3] = d;
  frame[4] = e;
  frame[5] = '\0';
}
