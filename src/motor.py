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

    def __init__(self, motor_config, enc_config):
        self.motor = motor_config
        self.speed = 0
        self.encoder = Encoder(enc_config)
        self.prev_error = 0

    def __repr__(self):
        return str(self.actual_speed)

    #Temporary run method, without PID control
    #Returns encoder position (for testing purposes)
    def run(self, given_speed):
        self.set_speed(given_speed)
        self.motor.throttle = self.speed
        return self.encoder.get_position()

    def brake(self):
        # STEADY/GRADUAL STOP
        self.kit.motor1.throttle = None
        time.sleep(0.5)
        self.kit.motor1.throttle = 0

    def get_speed(self, start_enc_val, interval=CHECK_PERIOD):
        return (self.encoder.get_position() - start_enc_val) / interval

    def set_speed(self,new_speed):
        self.speed = new_speed

    # Gets encoder position (for testing purposes)
    def get_enc_position(self):
        return self.encoder.get_position()
        

    # run method that will use PID control
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
        # if time.monotonic-start_time >= CHECK_PERIOD:
        #    self.get_speed(start_enc)
        # actual_speed = encoder.count() / time_interval
        # return actual_speed
        pass

    
