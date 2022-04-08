import time
from adafruit_motorkit import MotorKit
from src.encoder import Encoder
import board
import config

MAX_SPEED = 1
MIN_SPEED = 0.2

class Motor:

    def __init__(self, motor_config, enc_config):
        self.motor = motor_config
        self.pos = 0
        self.encoder = Encoder(enc_config)
        self.prev_error = 0

    def __repr__(self):
        return str(self.actual_speed)

    #Run method, without PID control
    #Returns encoder position 
    def run(self, given_speed):
        if (given_speed > MAX_SPEED):
            self.motor.throttle = MAX_SPEED
        elif (given_speed < MIN_SPEED):
            self.motor.throttle = MIN_SPEED
        else:
            self.motor.throttle = given_speed
        self.pos = self.encoder.get_position()
        return self.encoder.get_position()

    def brake(self):
        self.motor.throttle = 0.0

    def get_speed(self, interval):
        current_pos = self.encoder.get_postiion()
        rate = (current_pos - self.pos) / interval
        self.pos = current_pos 
        return rate


    # Returns the encoder count; starting point is the robot's initialization 
    def position(self):
        return self.encoder.get_position()

    
