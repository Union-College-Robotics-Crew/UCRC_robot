import rotaryio
import time
import board
from adafruit_motorkit import MotorKit
import analogio
import config
from motor import Motor
from ir_sensor import IR_sensor

KP_VAL = 0.1

class ControllerTest:

    def __init__(self):
        pass
        #self.motor = kit.motor4
        #self.encoder = rotaryio.IncrementalEncoder(board.D5, board.D6)
        #self.ir_sensor = analogio.AnalogIn(board.A5)
        #TARGET_IR = self.ir_sensor.value

    def count_to_throttle(counts):
        return counts / 465

    def ir_to_throttle(ir_readding):
        return ir_readding / 45000

    def initial_test(self):
        motor = Motor(config.test_motorKit, config.pin_D5, config.pin_D5)
        ir_sensor = IR_sensor(config.lAng_ir)
        target_ir = ir_sensor.ir_reading()

        desired_speed = 0.7
        motor.run(desired_speed)
        while True:
            print("Target IR Value: ")
            print(target_ir)
            print("Actual IR Value: ")
            print(ir_sensor)
            direction_error = self.ir_to_throttle(target_ir - ir_sensor.ir_reading())
            total_error = KP_VAL * direction_error
            print("Direction error: ")
            print(direction_error)

            print("Speed (without limits): ")
            print(desired_speed - total_error)
            
            if (desired_speed - total_error) > 1:
                desired_speed = 1
            elif (desired_speed - total_error) < 0:
                desired_speed = 0
            else:
                desired_speed -= total_error
            print("Input Speed: ")
            print(desired_speed)
            motor.run(desired_speed)

            time.sleep(1)



# IGNORE!

    # def continue_forward():
    #     pass

    # def left_wall():
    #     return True

    # def right_wall():
    #     pass

    # def forward(self):
    #     while (self.continue_forward()):
    #         if (self.left_wall()):
    #             direction_error = self.TARGET_LEFT - self.test_ir.value
    #         elif (self.right_wall()):
    #             #direction_error = self.test_ir.value - self.TARGET_LEFT
    #             pass
    #         else:
    #             pass

    #         total_error = KP_VAL * direction_error
            
            