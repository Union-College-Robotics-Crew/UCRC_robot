import config
import micromouse



class robot(micromouse):
    def __init__(self):
        self.__l_motor = motor(config.l_motorKit, config.l_encoder)
        self.__r_motor = config.r_motor
        self.__lAng_ir = config.lAng_ir
        self.__rAng_ir = config.rAng_ir
        self.__l_ir = config.l_ir
        self.__r_ir = config.r_ir
        self.__lFwd_ir = config.lFwd_ir
        self.__rFwd_ir = config.rFwd_ir
        self.__target_wall_values = {"TARGET_VAL_L_IR": 0, "TARGET_VAL_R_IR": 0,
                              "TARGET_VAL_L_FWD_IR":0, "TARGET_VAL_R_FWD_IR": 0,
                              "TARGET_VAL_L_ANG_IR":0, "TARGET_VAL_R_ANG_IR": 0}

    def turnRight(self):




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
            return true
        else:
            return false

    def wallLeft(self):
        if self.__l_ir == TARGET_VAL_L_IR:
            return true
        else:
            return false





