from hashlib import new
import time
from adafruit_motorkit import MotorKit
from encoder import Encoder
import board

# NEEDS TO BE CALCULATED!
COUNT_TO_THROTTLE = 1
THROTTLE_TO_COUNT = 1
CHECK_PERIOD = 10

class Motor:

    def __init__(self, motor_pin_A, motor_pin_B, enc_pin_A, enc_pin_B):
        self.motor = MotorKit(i2c=board.I2C())
        self.speed = 0
        self.encoder = Encoder(enc_pin_A, enc_pin_B)
        self.prev_error = 0

    def __repr__(self):
        return str(self.actual_speed)

    def run(self, speed, encoder):
        throttle_speed = speed * COUNT_TO_THROTTLE
        self.kit.motor1.throttle = throttle_speed
        time.sleep(0.002)
        self.actual_speed = self.get_speed(encoder, 0.002)
        self.brake()

        return self.actual_speed

    def brake(self):
        # STEADY/GRADUAL STOP
        self.kit.motor1.throttle = None
        time.sleep(0.5)
        self.kit.motor1.throttle = 0

    def get_speed(self, start_enc_val):
        return (start_enc_val - self.encoder.count()) / CHECK_PERIOD

    def set_speed(self,new_speed):
        self.speed=new_speed

    def run(self, desired_speed):
        """
        later async
        PID for speed control
        while
        run the motor with speed variable
            motorkit has built run (calculated pwm)
        monotnic timer goes to certain interval
        get_speed()
        error_calc()
        get new pwm value
        """
        if time.monotonic-start_time >= CHECK_PERIOD:
            self.get_speed(start_enc)
        # actual_speed = encoder.count() / time_interval
        # return actual_speed

