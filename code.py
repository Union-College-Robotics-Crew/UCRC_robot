
import rotaryio
import board
import time
from src.encoder import Encoder


pin_A= board.D5
pin_B= board.D6
encoder1= Encoder(pin_A,pin_B)

while True:
    #motor.run(0
    time.sleep(.01)
    print(encoder1.count())



