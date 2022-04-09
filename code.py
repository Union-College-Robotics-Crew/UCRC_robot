import time
import board
from src.button import Button
import config
from src.motor import Motor
from src.encoder import Encoder
from src.ir_sensor import IR_sensor
from adafruit_motorkit import MotorKit
import rotaryio
import analogio
from src.robot import Robot
from src.magnetometer import Magnetometer


from digitalio import DigitalInOut, Direction, Pull

NUM_CELLS = 4

# Temporary Encoder Configuration:
encL = rotaryio.IncrementalEncoder(config.l_encA, config.l_encB)
encR = rotaryio.IncrementalEncoder(config.r_encA, config.r_encB)

time.sleep(5)
# led = DigitalInOut(board.LED)
# led.direction = Direction.OUTPUT
# switch = DigitalInOut(board.D9)

# switch.direction = Direction.INPUT
# switch.pull = Pull.UP
test_robot = Robot(encL, encR)
# while True:
#     print(encL.position)
test_robot.turnLeft()
# while True:
#     # We could also do "led.value = not switch.value"!
#     # if switch.value:
#     #     led.value = False
#     #     print("here"*100)
#     # else:
#     #     led.value = True
#     #     time.sleep(0.01)
#     #     print("no"*30)
#     if not switch.value:

#         print(switch.value)
#     time.sleep(0.01)


# test_button = Button()
# while True:
#     test_button.colorTesting()


# continueForward() always returns True --> one forward call = infinite
# iteration = 0
# while (iteration < 8):
#     test_robot.forward()
#     iteration += 1

# test_robot.brake()
# while True:
#     test_robot.showAllIr()
#     time.sleep(.05)

# Calibrate Magnetometer:
# mag = Magnetometer()
# mag.calibrate()
#
# Test Heading:
# while True:
#     mag.heading()
#     time.sleep(0.5)
