import asyncio
import logging
from bleak import BleakClient


class BleComunicator(object):
    """bluetooth low level comunicator"""

    def __init__(self, loop):
        self.connected = False
        self.address = "01:02:03:04:1A:DF"  ##bluetooth mac address
        self.MODEL_NBR_UUID = "0000ffe1-0000-1000-8000-00805f9b34fb"  ##transmision characteristic
        self.client = None

    async def initBle(self):
        async self.client = BleakClient(self.address, loop=loop)
        self.connected = self.client.connect()
        if (not self.connected):
            print('could not connect to bluetooth device')
        self.client.set_disconnected_callback(self.disconnected)

    def disconnected(self):
        print('bluetooth device disconnected')

    def getData(self, sender, data):
        print(f"{sender}: {data}")

    async def listenForData(self):
        self.client.start_notify(self.MODEL_NBR_UUID, self.getData)
        while True:
            await asyncio.sleep(10.0, loop=loop)

    async def sendData(self, data):
        await self.client.write_gatt_char(self.MODEL_NBR_UUID, data)

    def uart_data_received(sender, data):
        print("RX> {0}".format(data))


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    ble = BleComunicator(loop)
    loop.run_until_complete(ble.initBle())
    loop.run_until_complete(ble.listenForData())
