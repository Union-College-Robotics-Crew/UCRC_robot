import time
from adafruit_motorkit import MotorKit
from encoder import Encoder
import board
import config

# NEEDS TO BE CALCULATED!
COUNT_TO_THROTTLE = 1
THROTTLE_TO_COUNT = 1
CHECK_PERIOD = 10

class Motor:

    def __init__(self, motor_config, enc_pinA, enc_pinB):
        self.motor = motor_config
        self.pos = 0
        self.encoder = Encoder(enc_pinA, enc_pinB)
        self.prev_error = 0

    def __repr__(self):
        return str(self.actual_speed)

    #Temporary run method, without PID control
    #Returns encoder position 
    def run(self, given_speed):
        self.motor.throttle = given_speed
        self.pos = self.encoder.get_position()
        return self.encoder.get_position()

    # Questionable brake method
    def brake(self):
        # STEADY/GRADUAL STOP
        self.kit.motor1.throttle = None
        time.sleep(0.5)
        self.kit.motor1.throttle = 0

    def get_speed(self, interval=CHECK_PERIOD):
        current_pos = self.encoder.get_postiion()
        rate = (current_pos - self.pos) / interval
        self.pos = current_pos 
        return rate


    # Returns the encoder count; starting point is the robot's initialization 
    def position(self):
        return self.encoder.get_position()

    