import time
import board
import config
from src.motor import Motor
from src.encoder import Encoder
from src.ir_sensor import IR_sensor
from adafruit_motorkit import MotorKit
import rotaryio
import analogio
from src.robot import Robot

NUM_CELLS = 4

# Temporary Encoder Configuration:
encL = rotaryio.IncrementalEncoder(config.l_encA, config.l_encB)
encR = rotaryio.IncrementalEncoder(config.r_encA, config.r_encB)

time.sleep(10)

test_robot = Robot(encL, encR)

# continueForward() always returns True --> one forward call = infinite
iteration = 0
while (iteration < 4):
    test_robot.forward()
    iteration += 1

test_robot.brake()
