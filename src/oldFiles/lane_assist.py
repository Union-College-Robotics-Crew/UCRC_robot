import base64
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
MAX_POSITION = 195.33
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
        self.__target_wall_values = {"TARGET_VAL_L_IR": 0, "TARGET_VAL_R_IR": 0,
                              "TARGET_VAL_L_FWD_IR":0, "TARGET_VAL_R_FWD_IR": 0,
                              "TARGET_VAL_L_ANG_IR":0, "TARGET_VAL_R_ANG_IR": 0}
                              
        # MAYBE SHOULD BE IN configure METHOD?:
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

        # start position of L/R motors (for encoder correction):
        # DESIGN DECISION: (1) could either keep start position as is OR (2) update it with each iteration
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
                # ALTERNATIVELY: could use "encoder correction", again
                use_PID = False
            elif (self.wallLeft() and self.wallRight):
                self.__error = self.__r_ir.ir_reading() - self.__l_ir.ir_reading() - self.__offset
            elif (self.wallLeft()):
                self.__error = 2 * (self.__target_left - self.__l_ir.ir_reading())
            elif (self.wallRight()):
                self.__error = 2 * (self.__r_ir.ir_reading() - self.__target_right)
            else:
                # Robot has no walls, so corrects direction with encoder readings
                self.__encCorrection(l_start_pos, r_start_pos)
                use_PID = False

            if (use_PID):
                # PID Function for total error calculation:
                total_error = KP * (self.__error) + KD * (self.__error - self.__prev_error) + KI * (self.__integral_error)
                # NOTE: Assumes that get_speed() returns speed in "throttle"
                # DESIGN DECISION: should I get the actual speed from the encoders, OR assume that the speed I input into the
                # motors is the current speed?
                l_speed = self.__l_motor.get_speed(TIME_INTERVAL) - total_error
                r_speed = self.__r_motor.get_speed(TIME_INTERVAL) + total_error
                # To avoid speeds out of motor's range / capability
                if ((l_speed <= MIN_SPEED) or (l_speed >= MAX_SPEED) or (r_speed <= MIN_SPEED) or (r_speed >= MAX_SPEED)):
                    anti_windup = True

                # DESIGN DECISION (in case of scaling adjusted speed): r_speed += (MAX_SPEED - l_speed)
                # if (l_speed >= MAX_SPEED):
                #     l_speed = MAX_SPEED
                #     anti_windup = True
                # elif (l_speed <= MIN_SPEED):
                #     # SCALING: r_speed += (MIN_SPEED - l_speed)
                #     l_speed = 0
                #     anti_windup = True
                # if (r_speed >= MAX_SPEED):
                #     # SCALING: ---
                #     r_speed = MAX_SPEED
                #     anti_windup = True
                # elif (r_speed <= MIN_SPEED):
                #     # SCALING: ---
                #     r_speed = MIN_SPEED
                #     anti_windup = True
                
                # Adjusting prev_error & integral_error for D and I components of PID
                # (includes "anti-windup" for the integrator)
                # Ideally, well-designed PID controller shouldn't saturate
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
                # ALTERNATE to possibility of "stale" errors: self.__error = 0, otherwise, keep error as is: 
                # (previous iteration's error)
            
            time.sleep(TIME_INTERVAL)

        # RESETTING THE POSSIBLE INSTANCE VARIABLE OF encoders' position at the start of cell:
        # self.__prev_l_pos = self.__l_motor.position()
        # self.__prev_r_pos = self.__r_motor.position()

    
    # Checks if robot moved one cell w/ encoders : returns boolean
    def __continueForward(self, l_pos, r_pos):
        l_counts = self.__l_motor.position() - l_pos
        r_counts = self.__r_motor.position() - r_pos
        average_counts = (l_counts + r_counts) / 2

        # Check w/ Encoders:
        if (average_counts > MAX_POSITION):
            return False

        # Check w/ Diagonal Sensors (Post Reading):
        if (self.wallFront() or ((self.__lAng_ir.ir_reading() - self.__l_ir.ir_reading() > 1.2) and (self.__rAng_ir.ir_reading() - self.__r_ir.ir_reading() > 1.2))):
            return False

        return True

        # TO UPDATE MAX_POSITION: Need to create methods like postDiagonalR & postDiagonalL and instance variables 
        #                         self.__prev_l_pos & self.__prev_r_pos
        # if (postDiagonalR and postDiagonalL):
        #   left_count = self.__l_motor.position() - self.__prev_l_pos
        #   right_count = self.__r_motor.position() - self.__prev_r_pos
        #   self.__prev_l_pos = self.__l_motor.position()
        #   self.__prev_r_pos = self.__r_motor.position()
        #   MAX_POSITION = (left_count + right_count) / 2 
        #   continue_forward = False

        return continue_forward

    # Corrects robot direction with left/right encoders
    def __encCorrection(self, l_pos, r_pos):
        l_counts = self.__l_motor.position() - l_pos
        r_counts = self.__r_motor.position() - r_pos
        if (l_counts > r_counts):
            # OPTION 1: Always set L/R motor to constant speed
            #           with R > L speed
            # l_speed = BASE_SPEED - 0.05
            # r_speed = BASE_SPEED + 0.05

            # OPTION 2: Use difference in L/R encoder readings
            #           to adjust motor speed
            # enc_error = K * (l_counts - r_counts)
            # NOTE: K - converts encoder counts to motor throttle
            # l_speed -= enc_error
            # r_speed += enc_error

            pass
        elif (r_counts > l_counts):
            # OPTION 1: Always set L/R motor to constant speed
            #           with L > R speed
            # l_speed = BASE_SPEED + 0.05
            # r_speed = BASE_SPEED - 0.05

            # OPTION 2: Use difference in L/R encoder readings
            #           to adjust motor speed
            # enc_error = K * (r_counts - l_counts)
            # NOTE: K - converts encoder counts to motor throttle
            # r_speed -= enc_error
            # l_speed += enc_error
            pass

    # TUNING Encoder Correction:
    def tuneEncCorrection(self, mode, base_speed, Kp, time_int):
        l_speed = base_speed
        r_speed = base_speed

        l_pos = self.__l_motor.position()
        r_pos = self.__r_motor.position()

        # MODE 1: Constant Encoder Correction
        while (mode == 1):
            l_counts = self.__l_motor.position() - l_pos
            r_counts = self.__r_motor.position() - r_pos
            if (l_counts > r_counts):
                l_speed = base_speed - 0.05
                r_speed = base_speed + 0.05

            elif (r_counts > l_counts):
                l_speed = base_speed + 0.05
                r_speed = base_speed - 0.05
            
            self.__l_motor.run(l_speed)
            self.__r_motor.run(r_speed)
            time.sleep(time_int)

        # MODE 2: Proportional Encoder Correction
        while (mode == 2):
            l_counts = self.__l_motor.position() - l_pos
            r_counts = self.__r_motor.position() - r_pos
            if (l_counts > r_counts):
                enc_error = Kp * (l_counts - r_counts)
                l_speed -= enc_error
                r_speed += enc_error

            elif (r_counts > l_counts):
                enc_error = Kp * (r_counts - l_counts)
                r_speed -= enc_error
                l_speed += enc_error
            
            self.__l_motor.run(l_speed)
            self.__r_motor.run(r_speed)
            time.sleep(time_int)



    def __angleCorrection(self):
        # OPTION 1: Akriti's method
        # OPTION 2: Using the accelerometer, if it works properly
        pass

            


    def configure(self):
        self.__target_wall_values["TARGET_VAL_L_IR"] = self.__l_ir.ir_reading()
        self.__target_wall_values["TARGET_VAL_R_IR"] = self.__r_ir.ir_reading()
        self.__target_wall_values["TARGET_VAL_L_ANG_IR"] = self.__lAng_ir.ir_reading()
        self.__target_wall_values["TARGET_VAL_R_ANG_IR"] = self.__rAng_ir.ir_reading()

        self.turnRight()
        self.__target_wall_values["TARGET_VAL_L_FWD_IR"] = 0
        self.__target_wall_values["TARGET_VAL_R_FWD_IR"] = 0
        self.turnLeft()

    def wallFront(self):
        if (self.__lFwd_ir == self.__target_wall_values["TARGET_VAL_L_FWD_IR"]) and (self.__rFwd_ir == self.__target_wall_values["TARGET_VAL_R_FWD_IR"]):
            return True
        else:
            return False

    def wallLeft(self):
        if (self.__l_ir == self.__target_wall_values["TARGET_VAL_L_IR"]) and (self.__lFwd_ir == self.__target_wall_values["TARGET_VAL_L_FWD_IR"]):
            return True
        else:
            return False

    def wallRight(self):
        if (self.__r_ir == self.__target_wall_values["TARGET_VAL_R_IR"]) and (self.__rFwd_ir == self.__target_wall_values["TARGET_VAL_R_FWD_IR"]):
            return True
        else:
            return False

    # Hard coded turn left and turn right methods:
    def turnLeft(self):
        start_l_enc = self.__l_motor.position()
        start_r_enc = self.__l_motor.position()
        max_turn = 0 # set experimentally
        turn_speed = 0 # set experimentally
        while ((self.__r_motor.position() - start_r_enc) < max_turn):
            self.__l_motor.run(- turn_speed)
            self.__r_motor.run(turn_speed)

    def turnRight(self):
        start_l_enc = self.__l_motor.position()
        start_r_enc = self.__l_motor.position()
        max_turn = 0 # set experimentally
        turn_speed = 0 # set experimentally
        while ((self.__l_motor.position() - start_l_enc) < max_turn):
            self.__l_motor.run(turn_speed)
            self.__r_motor.run(- turn_speed)
