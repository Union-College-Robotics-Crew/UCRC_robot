import board
import analogio
from ulab import numpy as np
from adafruit_motorkit import MotorKit
import rotaryio
import neopixel

# Built in LED
pixel = neopixel.NeoPixel(board.NEOPIXEL, 1)
pixel.brightness = 0.3

Color= {"red": (255, 0, 0),
        "green": (0, 255, 0),
        "blue": (0, 0, 255),
        "cyan": (0, 255, 255),
        "purple": (255, 0, 255),
        "yellow": (255, 255, 0),
        "white": (255, 255, 255),
        "neon": (127, 127, 0),
        "off": (0, 0, 0)}

kit = MotorKit()
# Motors Configured:
l_motorKit = kit.motor1
r_motorKit = kit.motor2

# Encoder Pins Configured:
r_encA = board.D13
r_encB = board.D12
l_encA = board.D10
l_encB = board.D11 

# IR Sensor Pins Configured:
lAng_ir = analogio.AnalogIn(board.A4) 
rAng_ir = analogio.AnalogIn(board.A1)
l_ir = analogio.AnalogIn(board.A3) 
r_ir = analogio.AnalogIn(board.A2)
lFwd_ir = analogio.AnalogIn(board.A5)
rFwd_ir = analogio.AnalogIn(board.A0)