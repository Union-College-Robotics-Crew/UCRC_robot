import rotaryio
import time
import board
from adafruit_motorkit import MotorKit
import analogio
import config
from motor import Motor
from ir_sensor import IR_sensor
# VERSION 1: Simple anti integral windup; Not utilizing diagonal sensors;
#            Simple/partial implementation of continueForward() and
#            encCorrection() yet


# All of these constants need to be determined EXPERIMENTALLY!
KP = 0.01
KD = 0
KI = 0
BASE_SPEED = 0.5
# Ideally, PID controller doesn't need time interval; it is taken care of by Kp, Kd, Ki gains
TIME_INTERVAL = 0.5
# Encoder count threshold for moving forward one cell
MAX_POSITION = 0
# Max & Min speeds for motor throttle (max needs adjusting)
MAX_SPEED = 1
MIN_SPEED = 0

class LaneAssist:

    def __init__(self):
        self.__l_motor = Motor(config.l_motorKit, config.pin_D5, config.pin_D6)
        self.__r_motor = Motor(config.r_motor, config.pind_D9, config.pin_D10)
        self.__lAng_ir = IR_sensor(config.lAng_ir)
        self.__rAng_ir = IR_sensor(config.rAng_ir)
        self.__l_ir = IR_sensor(config.l_ir)
        self.__r_ir = IR_sensor(config.r_ir)
        self.__lFwd_ir = IR_sensor(config.lFwd_ir)
        self.__rFwd_ir = IR_sensor(config.rFwd_ir)

        self.__target_left = self.__l_ir.ir_reading()
        self.__target_right = self.__r_ir.ir_reading()
        self.__offset = self.__target_right - self.__target_left

        self.__error = 0
        self.__prev_error = 0
        self.__integral_error = 0
    
    def forward(self):
        # default speeds:
        l_speed = BASE_SPEED
        r_speed = BASE_SPEED

        # start position of L/R motors:
        l_start_pos = self.__l_motor.position()
        r_start_pos = self.__r_motor.position()

        # Starting the motors at BASE_SPEED (ideal PID shouldn't have this):
            # self.__l_motor.run(l_speed)
            # self.__r_motor.run(r_speed)
            # time.sleep(TIME_INTERVAL)

        while (self.__continueForward(l_start_pos, r_start_pos)):

            total_error = 0
            use_PID = True
            anti_windup = False

            # Could wallFront() be used for the condition described below? 
            # Or is the threshold of IR sensor value different when robot is facing
            # front wall diagonally?
            if (self.wallFront()):
                # Unusual Scenario: when robot is tilted, so has front senors reading wall, BUT
                # right and left sensors may also read equal values, even though not in center
                # SOLUTION: using Akriti's method of correcting angle of robot with front sensors(?)
                self.__angleCorrection()
                use_PID = False
            elif (self.wallLeft() and self.wallRight):
                self.__error = self.__r_ir.ir_reading() - self.__l_ir.ir_reading() - self.__offset
            elif (self.wallLeft()):
                self.__error = 2 * (self.__target_left - self.__l_ir.ir_reading())
            elif (self.wallRight()):
                self.__error = 2 * (self.__r_ir.ir_reading() - self.__target_right)
            else:
                # Robot has no walls, so corrects direction with encoder readings
                self.__encCorrection()
                use_PID = False

            if (use_PID):
                # PID Function for total error calculation:
                total_error = KP * (self.__error) + KD * (self.__error - self.__prev_error) + KI * (self.__integral_error)
                # NOTE: Assumes that get_speed() returns speed in "throttle"
                l_speed = self.__l_motor.get_speed(TIME_INTERVAL) - total_error
                r_speed = self.__r_motor.get_speed(TIME_INTERVAL) + total_error
                # To avoid speeds out of motor's range / capability
                if (l_speed >= 1):
                    l_speed = 1
                    anti_windup = True
                elif (l_speed <= 0):
                    l_speed = 0
                    anti_windup = True
                if (r_speed >= 1):
                    r_speed = 1
                    anti_windup = True
                elif (r_speed <= 0):
                    r_speed = 0
                    anti_windup = True
                
                # Adjusting prev_error & integral_error for D and I components of PID
                # (includes "anti-windup" for the integrator)
                if (not anti_windup):
                    self.__integral_error += self.__error
                self.__prev_error = self.__error

                # Running motors at calculated speed for TIME_INTERVAL
                self.__r_motor.run(r_speed)
                self.__l_motor.run(l_speed)
                # First try without TIME_INTERVAL; if it doesn't work, slowly increment
            else:
                # To avoid getting a speed of robot over multiple iterations
                # Due to current implementation of Motor's get_speed()
                self.__l_motor.get_speed(TIME_INTERVAL)
                self.__r_motor.get_speed(TIME_INTERVAL)
            
            time.sleep(TIME_INTERVAL)

            


    def wallFront(self):
        pass

    def wallLeft(self):
        pass

    def wallRight(self):
        pass

    # Checks if robot moved one cell w/ encoders : returns boolean
    def __continueForward(self, l_pos, r_pos):
        #continue_forward = False
        l_counts = self.__l_motor.position() - l_pos
        r_counts = self.__r_motor.position() - r_pos
        average_counts = (l_counts + r_counts) / 2 

        if (average_counts > MAX_POSITION):
            return False

        return True

    # Corrects robot direction with left/right encoders
    def __encCorrection(self, l_pos, r_pos):
        l_counts = self.__l_motor.position() - l_pos
        r_counts = self.__r_motor.position() - r_pos
        if (l_counts > r_counts):
            # OPTION 1: Always set L/R motor to constant speed
            #           with R > L speed

            # OPTION 2: Use difference in L/R encoder readings
            #           to adjust motor speed
            pass
        elif (r_counts > l_counts):
            # OPTION 1: Always set L/R motor to constant speed
            #           with L > R speed

            # OPTION 2: Use difference in L/R encoder readings
            #           to adjust motor speed
            pass
        pass

    def __angleCorrection(self):
        # OPTION 1: Akriti's method
        # OPTION 2: Using the accelerometer, if it works properly
        pass
