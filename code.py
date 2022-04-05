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
from src.ble_comm import BLE_Comm

NUM_CELLS = 4

# Temporary Encoder Configuration:
encL = rotaryio.IncrementalEncoder(config.l_encA, config.l_encB)
encR = rotaryio.IncrementalEncoder(config.r_encA, config.r_encB)

time.sleep(5)

test_robot = Robot(encL, encR)

# continueForward() always returns True --> one forward call = infinite
iteration = 0
# while (iteration < 4):
#     test_robot.forward()
#     iteration += 1

ble = BLE_Comm()

while True:
    ble.send("hello")

# while True:
#     test_robot.isCornerBeam()
#     test_robot.forward()

test_robot.brake()
