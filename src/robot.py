
from ulab import numpy as np

import rotaryio
import time
import board
from adafruit_motorkit import MotorKit
import analogio
import config
from src.motor import Motor
from src.ir_sensor import IR_sensor

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

        self.__target_left = self.__l_ir.read()
        self.__target_right = self.__r_ir.read()
        self.__offset = self.__target_right - self.__target_left
        self.skipBeam = False

        self.timeFound_BEAM = time.monotonic()
        self.calibrate()
        self.__error = 0
        self.__prev_error = 0
        self.__integral_error = 0

    def calibrate(self):
        self.__l_ir.calibrate()
        self.__r_ir.calibrate()
        self.__lAng_ir.calibrate()
        self.__rAng_ir.calibrate()
        self.__lFwd_ir.calibrate()
        self.__rFwd_ir.calibrate()



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

    def isCornerBeam(self):
        l_ang=self.__lAng_ir.read()
        r_ang=self.__rAng_ir.read()

        l=self.__l_ir.read()
        r=self.__r_ir.read()

        l_frwd = self.__lFwd_ir.read()
        r_frwd = self.__rFwd_ir.read()

        lrAng_sum = l_ang + r_ang
        lr_sum = l + r

        

        l_angInit= self.__lAng_ir.initVal
        r_angInit= self.__rAng_ir.initVal

        l_Init = self.__l_ir.initVal
        r_Init = self.__r_ir.initVal

        #straight
        if (l_ang> self.__lAng_ir.initVal + .4) and (r_ang> self.__rAng_ir.initVal + .4):
            # if (l_ang> self.__lAng_ir.initVal + 2) or (r_ang> self.__rAng_ir.initVal + 2):
            #     return False
            self.skipBeam = False
            self.timeFound_BEAM = time.monotonic()
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
                return True

        #left oriented
        # if (r > r_Init + .4):
        #     print("LEFT"*10)
        if (r_ang> self.__rAng_ir.initVal + .4):
            # if (r_ang> self.__rAng_ir.initVal + 2): #no wall on right
            #     return False

            if self.skipBeam:
                self.skipBeam = False
                self.timeFound_BEAM = time.monotonic()
                return False
            else:
                self.skipBeam = True
                self.timeFound_BEAM = time.monotonic()
                return True
                
        

        #right oriented
        # if (l > l_Init + .4):
        #     print("RIGHT"*10)
        #     if (l_ang> self.__lAng_ir.initVal + .3):
        #         # if (l_ang> self.__lAng_ir.initVal + 2): #no wall on left
        #         #     return False

        #         if self.skipBeam:
        #             self.skipBeam = False
        #             return False
        #         else:
        #             self.skipBeam = True
        #             return True

        # #left oriented
        # if (r > r_Init + .4):
        #     print("LEFT"*10)
        #     if (r_ang> self.__rAng_ir.initVal + .3):
        #         # if (r_ang> self.__rAng_ir.initVal + 2): #no wall on right
        #         #     return False

        #         if self.skipBeam:
        #             self.skipBeam = False
        #             return False
        #         else:
        #             self.skipBeam = True
        #             return True
                    
        # #straight
        # if (l_ang> self.__lAng_ir.initVal + .3) and (r_ang> self.__rAng_ir.initVal + .3):
        #     # if (l_ang> self.__lAng_ir.initVal + 2) or (r_ang> self.__rAng_ir.initVal + 2):
        #     #     return False
        #     self.skipBeam = False
        #     return True
    

        print("L + R:",l+r)
        print("Lang + Rang:", l_ang+r_ang)
        # print("LRANG_InitSum:", lR_AngInit_sum)
        

        space = "*"*10 + "\n"
        print(space)

        print("DIFFERENCE R", r_ang - self.__rAng_ir.initVal )
        print("DIFFERENCE L", l_ang - self.__lAng_ir.initVal )
        print(space)



        # if not(self.FOUND_BEAM):
        #     if (l_ang> self.__lAng_ir.initVal + .3) or (r_ang> self.__rAng_ir.initVal + .3):
        #         if not(lr_sum > lR_Init_sum + .4):
        #             self.FOUND_BEAM = True
        #             self.timeFound_BEAM= time.monotonic()
        #             print("here"*20)
        #             return True

        # if self.FOUND_BEAM:
        #     return True
            # if time.monotonic() - self.timeFound_BEAM > .5:
            #     self.timeFound_BEAM = time.monotonic()
            #     self.FOUND_BEAM = False
            #     return False
        


        return False

    #hard coded
    # def isCornerBeam(self):
    #     if time.monotonic() - self.timeFound_BEAM > 1.31:
    #         self.timeFound_BEAM = time.monotonic()
    #         return True
    
    def showAllIr(self):
        print("L Ang:",self.__lAng_ir.read())
        # print("R Ang:", self.__rAng_ir.read())
        print("L:",self.__l_ir.read())
        # print("R", self.__r_ir.read())
        # print("L fwd:",self.__lFwd_ir.read())
        # print("R fwd",self.__rFwd_ir.read())


    def __continueForward(self):
        if time.monotonic()-self.timeFound_BEAM > .5:
            if self.isCornerBeam():
                return False
        if self.wallFront():
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
        time.sleep(.5)


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
