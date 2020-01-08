import serial
import threading
from time import sleep

serial_port = serial.Serial()


def read():
    while True:
        data = serial_port.read(9999999999)
        if len(data) > 0:
            print('Got:{}'.format(data))


def main():
    try:
        serial_port.baudrate = 9600
        serial_port.port = 'COM7'
        serial_port.timeout = 0
        if serial_port.isOpen(): serial_port.close()
        serial_port.open()
        t1 = threading.Thread(target=read, args=())
        t1.start()
        while True:
            try:
                command = input()
                command = bytearray(command, 'utf-8')
                serial_port.write(command)
            except KeyboardInterrupt:
                break
        serial_port.close()
    except Exception as e:
        print(e)
    finally:
        pass


if __name__ == "__main__":
    main()
