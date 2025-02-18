import asyncio
import logging
import threading
from builtins import object
import time
from enum import Enum
from bleak import _logger as logger
from bleak import BleakClient
from PyQt5.QtCore import QObject, pyqtSignal
import serial
import threading


def main(ble):
    loop = asyncio.new_event_loop()
    loop.run_until_complete(ble.run(loop))


class Signals(QObject):
    '''
    Defines the signals available from a running worker thread.
    '''
    finished = pyqtSignal()
    lock = pyqtSignal(int)
    print = pyqtSignal(object)


class Commands(object):
    """command executor class it sends commands, check them and maintain errors"""

    class commands(Enum):
        default = 1
        turnLeft = 2
        turnRight = 3
        turnAround = 4
        forward = 5
        backward = 6
        speedUp = 7
        slowDown = 8
        biggerTurnAngle = 9
        smallerTurnAngle = 10
        biggerStep = 11
        smallerStep = 12
        stopCommand = 13

    class additionalInfo(Enum):
        empty = 1
        commandStarted = 2
        commandEnded = 3
        commandError = 4
        MobileRobotError = 5
        RobotReady = 6
        accessDenyed = 7

    class deviceId(Enum):
        pc = 2
        mobileRobot = 1

    class robotWatchDog(object):
        """command timers waiting for proper execution"""

        class commandState(Enum):
            sending = 1
            executing = 2
            done = 3

        class commandTimes(Enum):
            """in sec"""
            sendingTime = 10
            executingTime = 60

        def __init__(self, command, commandId, mainPtr, print):
            self.mainPtr = mainPtr
            self.command = command
            self.commandId = commandId
            self.state = self.commandState.sending
            self.timer = threading.Timer(self.commandTimes.sendingTime.value, self)
            self.timer.start()
            self.print = print

        def __call__(self):
            self.print(
                "Command: {}, id {}. Command time is up, robot did not changed {} state\n".format(self.command.name,
                                                                                                  self.commandId,
                                                                                                  self.state))
            self.mainPtr.delete(self)

    def __init__(self):
        self.comunicator = None
        self.messageId = 1
        self.commandId = 1
        self.ble = SerialComunicator(self.gotData)
        self.watchDog = []
        self.signals = Signals()

    def run(self):
        self.comunicator = threading.Thread(target=main, args=(self.ble,), daemon=True)
        self.comunicator.start()

    def delete(self, ptr):
        self.watchDog.remove(ptr)

    def executeCommand(self, command):
        data = bytearray(
            [self.deviceId.pc.value, command.value, self.commandId, self.messageId, self.additionalInfo.empty.value])
        #self.signals.print.emit(data)
        # self.print(str(data))
        self.watchDog.append(self.robotWatchDog(command, self.commandId, self, self.print))
        self.ble.setData(data)
        prefix = "Command: {}, commandId: {} - ".format(command.name, self.commandId)
        self.commandId %= 255
        self.messageId %= 255
        self.messageId += 1
        self.commandId += 1
        self.print("{} initialization".format(prefix))

    def print(self, str):
        self.signals.print.emit(str)

    def gotData(self, data):
        try:
            self.checkData(data)
        except Exception as e:
            self.print("An exception occurred while getting data: " + str(e))
        finally:
            pass

    def disconnect(self):
        self.ble.disconnect()

    def checkData(self, data):
        deviceId = self.deviceId(data[0])
        command = self.commands(data[1])
        commandId = data[2]
        messageId = data[3]
        additionalInfo = self.additionalInfo(data[4])
        prefix = "Command: {}, commandId: {} - ".format(command.name, commandId)
        # print("{} {} {} {} {}".format(deviceId, messageId, additionalInfo, command, commandId))
        if self.checkCommands(deviceId, command, commandId, messageId, additionalInfo):
            return
        if deviceId != self.deviceId.mobileRobot:
            self.print("Wrong device Id, should be 1 - mobile Robot")
        if additionalInfo == self.additionalInfo.commandError:
            self.print("{}Error".format(prefix))
        if additionalInfo == self.additionalInfo.MobileRobotError:
            self.print("Robot error")
        found = False
        for watchDog in self.watchDog:
            if commandId == watchDog.commandId:
                watchDog.timer.cancel()
                found = True
                if additionalInfo == self.additionalInfo.commandStarted:
                    watchDog.state = self.robotWatchDog.commandState.executing
                    watchDog.timer = threading.Timer(self.robotWatchDog.commandTimes.executingTime.value, watchDog)
                    watchDog.timer.start()
                    self.print("{}Under execution".format(prefix))
                elif additionalInfo == self.additionalInfo.commandEnded:
                    watchDog.state = self.robotWatchDog.commandState.done
                    self.print("{}Executed".format(prefix))
                    watchDog.timer.cancel()
                    self.delete(watchDog)
                    break
        if not found:
            self.print("None of watchdog commands found, error")

    def checkCommands(self, deviceId, command, commandId, messageId, additionalInfo):
        if command == self.commands.stopCommand and additionalInfo == self.additionalInfo.commandEnded:
            self.print("Stop command executed, robot has cancelled executing commands")
            for watchDog in self.watchDog:
                watchDog.timer.cancel()
            self.watchDog.clear()
            return True
        if additionalInfo == self.additionalInfo.empty:
            return False
        elif additionalInfo == self.additionalInfo.commandError:
            self.print("Command error occurred, id {}".format(commandId))
            return True
        elif additionalInfo == self.additionalInfo.accessDenyed:
            self.print("Access to robot denied, wrong security code sent")
            self.ble.timer.cancel()
            return True
        elif additionalInfo == self.additionalInfo.RobotReady:
            self.print("Robot is ready")
            self.ble.timer.cancel()
            return True
        elif additionalInfo == self.additionalInfo.MobileRobotError:
            self.print("Mobile robot error")
            return True
        else:
            return False


class SerialComunicator(object):
    """bluetooth low level comunicator"""

    def __init__(self, fnct):
        self.connected = False
        self.nmb = 7
        self.port = 'COM{}'.format(self.nmb)  ##port com
        self.secourityCode = b'QV9JKMNASKJNWKJSNKWJ'
        self.serial_port = serial.Serial()
        self.baud = 9600
        self.data = b''
        self.gotData = b''
        self.event = threading.Event()
        self.onDataFunction = fnct
        self.disc = False
        self.signals = Signals()
        self.timer = threading.Timer(10, self.secourityCodeTimeUp)

    def print(self, str):
        self.signals.print.emit(str)

    def setData(self, data):
        self.data = data
        self.event.set()

    def disconnect(self):
        self.disc = True
        self.event.set()

    def runRx(self):
        while not self.disc:
            data = self.serial_port.read(9999999999)
            if len(data) > 0:
                print("raw Data: {}".format(data))
                if self.gotData:
                    self.gotData += data
                    if len(self.gotData) == 5:
                        self.onDataFunction(self.gotData)
                        self.gotData = b''
                if data[0] == 3:
                    data = data[1:]
                    if len(data) != 5:
                        self.gotData = data
                    else:
                        #print("command: {}".format(data[1:]))
                        self.onDataFunction(data)
                        self.gotData = b''

    async def run(self, loop):
        self.print("Running communicator interface")
        try:
            self.serial_port.baudrate = self.baud
            self.serial_port.port = self.port
            self.serial_port.timeout = 0
            if self.serial_port.isOpen():
                self.serial_port.close()
            self.serial_port.open()
            t1 = threading.Thread(target=self.runRx, args=())
            t1.start()
            self.signals.lock.emit(1)
            time.sleep(1)
            self.print("Connected to mobile robot")
            time.sleep(1)
            self.serial_port.write(self.secourityCode)
            self.timer = threading.Timer(10, self.secourityCodeTimeUp)
            self.timer.start()
            while not self.disc:
                self.event.wait()
                if self.disc:
                    break
                self.serial_port.write(self.data)
                self.event.clear()
            self.print("Disconnected")
        except Exception as e:
            self.print("An exception occurred: " + str(e))
        finally:
            time.sleep(1)
            self.serial_port.close()
            self.timer.cancel()
            self.print("Communicator closed")
            self.signals.lock.emit(2)
            self.disc = False

    def getData(self, data):
        self.onDataFunction(data)

    def secourityCodeTimeUp(self):
        self.print("Time for accept connection is up")
        self.signals.lock.emit(2)
        self.disc = True
        self.event.set()


if __name__ == "__main__":
    command = Commands()
    command.run()
    while True:
        time.sleep(12)
        print("command: {}\n".format(command.commandId))
        print(command.watchDog)
        command.executeCommand(command.commands.eg1)
        time.sleep(5)
