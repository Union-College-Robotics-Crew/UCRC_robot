import board
import analogio
from ulab import numpy as np
from adafruit_motorkit import MotorKit
import rotaryio

kit = MotorKit()
# Available: motor1, motor2, motor3, and motor4 
l_motorKit = kit.motor1
r_motorKit = kit.motor2
test_motorKit = kit.motor4

# Encoder pins in use currently:
pin_D5 = board.D5
pin_D6 = board.D6

# Issue with IncrementalEncoder in config file; will simply use pins from above 

#encoder_pins = [board.D5, board.D6, board.D9, board.D10, board.D11, board.D12, board.D13]
#l_encoder = rotaryio.IncrementalEncoder(encoder_pins[0], encoder_pins[1])
#r_encoder = rotaryio.IncrementalEncoder(encoder_pins[2], encoder_pins[3])

lAng_ir = analogio.AnalogIn(board.A0) 
rAng_ir = analogio.AnalogIn(board.A1)
l_ir = analogio.AnalogIn(board.A2)
r_ir = analogio.AnalogIn(board.A3)
lFwd_ir = analogio.AnalogIn(board.A4)
rFwd_ir = analogio.AnalogIn(board.A5)