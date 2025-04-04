import pyfirmata
import time

pin = 13
port = "COM7"
board = pyfirmata.Arduino(port)
while True:
    board.digital[pin].write(1)
    print("on")
    time.sleep(1)

    board.digital[pin].write(0)
    print("off")
    time.sleep(1)
