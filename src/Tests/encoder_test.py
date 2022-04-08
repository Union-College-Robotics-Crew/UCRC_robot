import rotaryio
import board
import time
from src.encoder import Encoder

class EncoderTest:
    
    def run_test():
        """ Testing ENCODER without Encoder class """
        pin_A= board.D5
        pin_B= board.D6
        encoder = rotaryio.IncrementalEncoder(pin_A, pin_B)

        while True:
            print(encoder.position / 3)
            time.sleep(0.5)


