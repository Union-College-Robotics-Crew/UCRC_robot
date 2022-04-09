
import rotaryio
import time
import board
from adafruit_motorkit import MotorKit
import analogio
import config
from src.motor import Motor
from src.ir_sensor import IR_sensor
# from src.magnetometer import Magnetometer

# Proportional, Derivative, and Integral Gains:
# KP = 0.05
# KD = 0.025
# KI = 0.001

KP = 0.045
KD = 0.025
KI = 0

BASE_SPEED = 0.4

# Time Interval Between Iterations:
TIME_INTERVAL = 0

# Max & Min speeds for Motor:
MAX_SPEED = 1
MIN_SPEED = 0.2

# Has Side Walls Threshold (Temporarily Hard-Coded):
HAS_LEFT = 7.6
HAS_RIGHT = 7.6


FRWD_UP_TIME = 1.153
FRWD_LOW_TIME = .7
NO_WALL_TIME = 1

INITIAL_FRWD_COUNT = 39
NORMAL_FRWRD_COUNT = 80
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
#         self.__magnetometer = Magnetometer()

        self.__target_left = self.__l_ir.read()
        self.__target_right = self.__r_ir.read()
        self.__offset = self.__target_right - self.__target_left

        self.skipBeam = False
        self.timeFound_BEAM = time.monotonic()

        self.calibrate()
        self.__error = 0
        self.__prev_error = 0
        self.__integral_error = 0

        self.__calibrateForward()



    def calibrate(self):
        self.__l_ir.calibrate()
        self.__r_ir.calibrate()
        self.__lAng_ir.calibrate()
        self.__rAng_ir.calibrate()
        self.__lFwd_ir.calibrate()
        self.__rFwd_ir.calibrate()



    def forward(self):
        self.timeStartedFwd = time.monotonic()
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

    def __calibrateForward(self):
        self.timeStartedFwd = time.monotonic()
        l_speed = BASE_SPEED
        r_speed = BASE_SPEED
        anti_windup = False

        l_start_pos = self.__l_motor.position()
        r_start_pos = self.__r_motor.position()

        while (self.__initContinue(l_start_pos)):
            print("calibrate frwd")
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

    def __initContinue(self, leftInitial):
#         leftCount = self.__l_motor.position()
        #rightCount = self.__r_motor.position()

        if (self.__l_motor.position() - leftInitial) < INITIAL_FRWD_COUNT:
            return True

        return False


    def isCornerBeam(self):
        l_ang=self.__lAng_ir.read()
        r_ang=self.__rAng_ir.read()

        l=self.__l_ir.read()
        r=self.__r_ir.read()

        if time.monotonic() - self.timeStartedFwd > FRWD_UP_TIME:
            return True

        if self.wallLeft() and self.wallRight() :
            #straight
            if (l_ang> self.__lAng_ir.initVal + .4) and (r_ang> self.__rAng_ir.initVal + .4):
                # if (l_ang> self.__lAng_ir.initVal + 2) or (r_ang> self.__rAng_ir.initVal + 2):
                #     return False
                self.skipBeam = False
                self.timeFound_BEAM = time.monotonic()
                if time.monotonic() - self.timeStartedFwd < FRWD_LOW_TIME:
                    return False
                return True

            if (l_ang> self.__lAng_ir.initVal + .4):
                # if (l > l_Init + .4):
                # if (l_ang> self.__lAng_ir.initVal + 2): #no wall on left
                #     return False
                if self.skipBeam:
                    self.skipBeam = False
                    self.timeFound_BEAM = time.monotonic()
                    return False
                else:
                    self.skipBeam = True
                    self.timeFound_BEAM = time.monotonic()
                    if time.monotonic() - self.timeStartedFwd < 1:
                        return False
                    return True



            if (r_ang> self.__rAng_ir.initVal + .4):
                if self.skipBeam:
                    self.skipBeam = False
                    self.timeFound_BEAM = time.monotonic()
                    return False
                else:
                    self.skipBeam = True
                    self.timeFound_BEAM = time.monotonic()
                    if time.monotonic() - self.timeStartedFwd < FRWD_LOW_TIME:
                        return False
                    return True

        else:
            if time.monotonic() - self.timeStartedFwd > NO_WALL_TIME:
                return True



        print("L + R:",l+r)
        print("Lang + Rang:", l_ang+r_ang)


        space = "*"*10 + "\n"
        print(space)

        print("DIFFERENCE R", r_ang - self.__rAng_ir.initVal )
        print("DIFFERENCE L", l_ang - self.__lAng_ir.initVal )
        print(space)

        return False


    def showAllIr(self):
        print("L Ang:",self.__lAng_ir.read())
        # print("R Ang:", self.__rAng_ir.read())
        print("L:",self.__l_ir.read())
        # print("R", self.__r_ir.read())
        # print("L fwd:",self.__lFwd_ir.read())
        # print("R fwd",self.__rFwd_ir.read())

    def __continueForward(self, leftPos, rightPos):
#         if time.monotonic()-self.timeFound_BEAM > .5:
#             if self.isCornerBeam():
#                 return False
        if (self.wallFront()):
            return False

        curLeft = self.__l_motor.position() - leftPos
        curRight = self.__r_motor.position() - rightPos
        if ((curLeft + curRight) / 2 > 80):
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
        time.sleep(0.5)

    def turnLeft(self):
#         special_case = False
#         config.pixel.fill(config.Color["white"])
#         target_heading = self.__magnetometer.heading() + 90
#         if (target_heading > 360):
#           target_heading -= 360
#           special_case = True

#         if (special_case):
#           while (self.__magnetometer.heading() <= 360 and self.__magnetometer.heading() >= 270):
#               config.pixel.fill(config.Color["green"])
#               self.__rotateRight()

#         while (self.__magnetometer.heading() <= target_heading):
#           config.pixel.fill(config.Color["yellow"])
#           self.__rotateRight()
        initialRight = self.__r_motor.position()
        while (self.__r_motor.position() - initialRight < 69):
            self.__l_motor.runNegative(-0.5)
            self.__r_motor.run(0.5)
            config.pixel.fill(config.Color["green"])

        self.brake()
        config.pixel.fill(config.Color["red"])

    def turnRight(self):
#         special_case = False
#         config.pixel.fill(config.Color["white"])
#         target_heading = self.__magnetometer.heading() - 90
#         if (target_heading < 0):
#           target_heading += 360
#           special_case = True

#         if (special_case):
#           while (self.__magnetometer.heading() >= 0 and self.__magnetometer.heading() <= 90):
#               config.pixel.fill(config.Color["green"])
#               self.__rotateLeft()

#         while (self.__magnetometer.heading() >= target_heading):
#           config.pixel.fill(config.Color["yellow"])
#           self.__rotateLeft()
        initialLeft = self.__l_motor.position()
        while (self.__l_motor.position() - initialLeft < 73):
            #self.__rotateRight()
            self.__r_motor.runNegative(-0.5)
            self.__l_motor.run(0.5)
            config.pixel.fill(config.Color["green"])

        self.brake()
        config.pixel.fill(config.Color["red"])


    def __rotateLeft(self):
        prev_lEnc = self.__l_motor.position()
        prev_rEnc = self.__r_motor.position()
        self.__r_motor.run(0.5)
        self.__l_motor.runNegative(-0.5)

        while ((self.__l_motor.position() - prev_lEnc > 5) and (self.__r_motor.position() - prev_rEnc < -5)):
            if (self.__l_motor.position() - prev_lEnc >= 5):
                self.__l_motor.brake()
            if (self.__r_motor.position() - prev_rEnc <= 5):
                self.__r_motor.brake()

        # In case one of the motor doesn't brake:
        self.brake()

    def __rotateRight(self):
        prev_lEnc = self.__l_motor.position()
        prev_rEnc = self.__r_motor.position()
        self.__r_motor.runNegative(-0.5)
        self.__l_motor.run(0.5)
        # while (self.__l_motor.position() - prev_lEnc < 20):
        #     config.pixel.fill(config.Color["blue"])
        #     print(self.__l_motor.position() - prev_lEnc)

        while ((self.__l_motor.position() - prev_lEnc < 2) and (self.__r_motor.position() - prev_rEnc > -2)):
            if (self.__l_motor.position() - prev_lEnc >= 2):
                self.__l_motor.brake()
            if (self.__r_motor.position() - prev_rEnc <= -2):
                self.__r_motor.brake()

        # In case one of the motor doesn't brake:
        self.brake()


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
