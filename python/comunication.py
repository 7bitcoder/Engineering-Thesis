import asyncio
import logging
import threading
from builtins import object
import time
from enum import Enum
from bleak import _logger as logger
from bleak import BleakClient


def main(ble):
    print("starting low level comunication")
    loop = asyncio.new_event_loop()
    loop.run_until_complete(ble.run(loop))


class Commands(object):
    """command executor class it sends commands, check them and maintain errors"""

    class commandsEnum(Enum):
        stop = 15
        start = 16
        eg1 = 1
        eg2 = 2

    class additionalInfoEnum(Enum):
        empty = 0
        commandStarted = 1
        commandEnded = 2
        commandError = 3
        MobileRobotError = 4

    class deviceIdEnum(Enum):
        pc = 0
        mobileRobot = 1

    class robotWatchDog(object):
        """command timers wathing for proper execution"""

        class commandState(Enum):
            sending = 1
            executing = 2
            done = 3

        class commandTimes(object):
            sendingTime = 10  # s
            executingTime = 120  # s

        def __init__(self, commandId):
            self.commandId = commandId
            self.state = self.commandState.sending
            self.timer = threading.Timer(self.commandTimes.sendingTime, self)

        def __call__(self):
            print("Command time is up, robot did not changed {} state".format(self.state))

    def __init__(self):
        """dict - name of command = id"""
        self.comunicator = None

        self.messageId = 0
        self.commandId = 0
        self.ble = BleComunicator(self.gotData)
        self.watchDog = []

    def run(self):
        print("running thread for low level comunicator")
        self.comunicator = threading.Thread(target=main, args=(self.ble,), daemon=True)
        self.comunicator.start()

    def executeCommand(self, command):
        data = bytearray([1, self.messageId, 0, command, self.commandId])
        self.messageId += 1
        self.commandId += 1
        watchDog = self.robotWatchDog(self.commandId)
        self.watchDog.append()
        self.ble.setData(data)

    def gotData(self, data):
        self.checkData(data)
        print("got data" + str(data))

    def checkData(self, data):
        if (data[0] != 1):
            print("Wrong device Id, should be 1 - mobile Robot")


class BleComunicator(object):
    """bluetooth low level comunicator"""

    def __init__(self, fnct):
        self.connected = False
        self.address = "01:02:03:04:1A:DF"  ##bluetooth mac address
        self.uartUUID = "0000ffe1-0000-1000-8000-00805f9b34fb"  ##transmision characteristic
        self.data = b''
        self.event = threading.Event()
        self.onDataFunction = fnct

    def setData(self, data):
        self.data = data
        self.event.set()

    async def run(self, loop):
        try:
            async with BleakClient(self.address, loop=loop) as client:
                # client.set_disconnected_callback(self.disconnected)
                x = await client.is_connected()
                print("Connected to mobileRobot")
                await client.start_notify(self.uartUUID, self.getData)
                while True:
                    self.event.wait()
                    await client.write_gatt_char(self.uartUUID, self.data)
                    self.event.clear()
        except Exception as e:
            print("An exception occurred: " + str(e))
        finally:
            print("Disconnected")

    def getData(self, sender, data):
        self.onDataFunction(data)


if __name__ == "__main__":
    command = Commands()
    command.run()
    i = 0
    while True:
        i += 1
        time.sleep(10)
        g = 'xDDDDDDDDDD {} \n'.format(i)
        print("sth")
        command.executeCommand(g)
