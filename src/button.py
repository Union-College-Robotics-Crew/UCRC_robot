import time

from sympy import re
import board
from digitalio import DigitalInOut, Direction, Pull
import config

class Button:
    def __init__(self, enc_config):
        self.switch = DigitalInOut(board.D6)
        self.switch.direction = Direction.INPUT
        self.switch.pull = Pull.UP

    def clicked(self):
        time.sleep(0.01) #debounce delay
        return not self.switch.value
    
    def waitTillBluetooth(self):
        while not self.clicked():
            pass
    
    def colorTesting(self):
        if self.clicked():
            config.pixel.fill(config.Color["green"])
        else:
            config.pixel.fill(config.Color["red"])