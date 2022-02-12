from json import encoder
import time
import board
from src import config
from src.motor import Motor
from src.encoder import Encoder
from src.ir_sensor import IR_sensor
from adafruit_motorkit import MotorKit
import rotaryio

NUM_READINGS = 1000

test_motor = Motor(config.test_motorKit, config.l_encoder)

plot_speed = True
plot_position = False

speed = 0
actual_speed = 0
while (plot_speed):
    while (speed < 1):
        start_position = test_motor.run(speed)
        time.sleep(1)
        actual_speed = test_motor.get_speed(start_position, 1)
        print((actual_speed,))

        speed += 0.1

    while (speed > 0):
        start_position = test_motor.run(speed)
        time.sleep(1)
        actual_speed = test_motor.get_speed(start_position, 1)
        speed -= 0.1

speed = 0
while (plot_position):
    while (speed < 1):
        test_motor.run(speed)
        time.sleep(1)
        cur_position = test_motor.get_enc_position
        print((cur_position,))
        speed += 0.1

    while (speed > 0):
        test_motor.run(speed)
        time.sleep(1)
        cur_position = test_motor.get_enc_position
        print((cur_position,))
        speed -= 0.1

