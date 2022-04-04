import rotaryio
import time
import board
from adafruit_motorkit import MotorKit
import analogio
import config
from src.motor import Motor
from src.ir_sensor import IR_sensor
from src.magnetometer import Magnetometer

# Proportional, Derivative, and Integral Gains:
KP = 0.05
KD = 0.025
KI = 0.001

BASE_SPEED = 0.4

# Time Interval Between Iterations:
TIME_INTERVAL = 0

# Max & Min speeds for Motor:
MAX_SPEED = 1
MIN_SPEED = 0.2

# Has Side Walls Threshold (Temporarily Hard-Coded):
HAS_LEFT = 7.6
HAS_RIGHT = 7.6

class Robot:

    def __init__(self, l_enc, r_enc):
        config.pixel.fill(config.Color["green"])
        self.__l_motor = Motor(config.l_motorKit, l_enc)
        self.__r_motor = Motor(config.r_motorKit, r_enc)
        self.__lAng_ir = IR_sensor(config.lAng_ir)
        self.__rAng_ir = IR_sensor(config.rAng_ir)
        self.__l_ir = IR_sensor(config.l_ir)
        self.__r_ir = IR_sensor(config.r_ir)
        self.__lFwd_ir = IR_sensor(config.lFwd_ir)
        self.__rFwd_ir = IR_sensor(config.rFwd_ir)
        self.__magnetometer = Magnetometer()

        self.__target_left = self.__l_ir.read()
        self.__target_right = self.__r_ir.read()
        self.__offset = self.__target_right - self.__target_left

        self.__error = 0
        self.__prev_error = 0
        self.__integral_error = 0

    def forward(self):
        l_speed = BASE_SPEED
        r_speed = BASE_SPEED
        anti_windup = False
        
        l_start_pos = self.__l_motor.position()
        r_start_pos = self.__r_motor.position()

        while (self.__continueForward()):
            use_PID = True

            if (self.wallLeft() and self.wallRight()):
                config.pixel.fill(config.Color["white"])
                self.__error = self.__r_ir.read() - self.__l_ir.read() - self.__offset
            elif (self.wallLeft()):
                config.pixel.fill(config.Color["yellow"])
                self.__error = 2 * (self.__target_left - self.__l_ir.read())
            elif (self.wallRight()):
                config.pixel.fill(config.Color["purple"])
                self.__error = 2 * (self.__r_ir.read() - self.__target_right)
            else:
                self.__encCorrection(l_start_pos, r_start_pos)
                use_PID = False



            if (use_PID):
                # PID Function for Control Signal (Total Error) Calculation:
                total_error = KP * (self.__error) + KD * (self.__error - self.__prev_error) + KI * (self.__integral_error)
                
                l_speed = BASE_SPEED + total_error
                r_speed = BASE_SPEED - total_error

                # Anti-Windup for Integrator:
                if ((l_speed <= MIN_SPEED) or (l_speed >= MAX_SPEED) or (r_speed <= MIN_SPEED) or (r_speed >= MAX_SPEED)):
                    anti_windup = True

                # Adjusting prev_error & integral_error for D and I components of PID
                if (not anti_windup):
                    self.__integral_error += self.__error
                self.__prev_error = self.__error

                # Running motors at calculated speed for TIME_INTERVAL (Original):
                self.__r_motor.run(r_speed)
                self.__l_motor.run(l_speed)

            time.sleep(TIME_INTERVAL)

        config.pixel.fill(config.Color["red"])
        self.brake()


    def __continueForward(self):
        if (self.wallFront()):
            return False

        return True

    def wallLeft(self):
        if (self.__l_ir.read() <= HAS_LEFT):
            return True
        else:
            return False

    def wallRight(self):
        if (self.__r_ir.read() <= HAS_RIGHT):
            return True
        else:
            return False

    def wallFront(self):
        if ((self.__lFwd_ir.read() <= self.__target_left) and (self.__rFwd_ir.read() <= self.__target_right)):
            return True
        else:
            return False

    def brake(self):
        self.__l_motor.brake()
        self.__r_motor.brake()

    def turnRight(self):
        config.pixel.fill(config.Color["white"])
        target_heading = self.__magnetometer.heading() + 90
        if (target_heading > 360):
          target_heading -= 360
          special_case = True 

        if (special_case):
          while (self.__magnetometer.heading() <= 360 and self.__magnetometer.heading() >= 270):
              config.pixel.fill(config.Color["green"])

        while (self.__magnetometer.heading() <= target_heading):
          config.pixel.fill(config.Color["yellow"])

        self.brake()
        config.pixel.fill(config.Color["red"])

    def turnLeft(self):
        config.pixel.fill(config.Color["white"])
        target_heading = self.__magnetometer.heading() - 90
        if (target_heading < 0):
          target_heading += 360
          special_case = True 

        if (special_case):
          while (self.__magnetometer.heading() >= 0 and self.__magnetometer.heading() <= 90):
              config.pixel.fill(config.Color["green"])

        while (self.__magnetometer.heading() >= target_heading):
          config.pixel.fill(config.Color["yellow"])

        self.brake()
        config.pixel.fill(config.Color["red"])



    # Encoder Correction - corrects robot direction with left/right encoders:
    def __encCorrection(self, l_pos, r_pos):
        l_counts = self.__l_motor.position() - l_pos
        r_counts = self.__r_motor.position() - r_pos
        if (l_counts > r_counts):
            l_speed = BASE_SPEED - 0.05
            r_speed = BASE_SPEED + 0.05

        elif (r_counts > l_counts):
            l_speed = BASE_SPEED + 0.05
            r_speed = BASE_SPEED - 0.05
        else:
            l_speed = BASE_SPEED
            r_speed = BASE_SPEED

        self.__l_motor.run(l_speed)
        self.__r_motor.run(r_speed)

# TURNING ISSUE TO SOLVE:
# Whenever turning in the range where the "heading" changes from 0 --> 360 OR 360--> 0;
# What should the loop condition be then?

# Pseudocode of TURN RIGHT:

# target_heading = self.__magnetometer.heading() + 90
# if (target_heading > 360):
#   target_heading -= 360
#   special_case = True 

# if (special_case):
#   while (self.__magnetometer.heading() <= 360 and self.__magnetometer.heading() >= 270):
#       rotate right

# while (self.__magnetometer.heading() <= target_heading):
#   rotate right

# self.brake()


# Pseudocode of TURN LEFT:

# target_heading = self.__magnetometer.heading() - 90
# if (target_heading < 0):
#   target_heading += 360
#   special_case = True 

# if (special_case):
#   while (self.__magnetometer.heading() >= 0 and self.__magnetometer.heading() <= 90):
#       rotate left

# while (self.__magnetometer.heading() >= target_heading):
#   rotate left

# self.brake()