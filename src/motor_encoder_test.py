import rotaryio
from adafruit_motorkit import MotorKit
import board
import time
from src.motor import Motor
import config

class MotorEncoderTest:

    def __init__(self) -> None:
        pass

    def motor_speed(iterations):
        test_motor = Motor(config.test_motorKit, config.pin_D5, config.pin_D6)
        speed = 0
        actual_speed = 0
        time_passed = 0
        readings = 0
        while readings < iterations:
            while speed < 1:
                test_motor.run(speed)
                time.sleep(1)
                time_passed += 1
                actual_speed = test_motor.get_speed(1)
                print((actual_speed,))
                speed += 0.1

            speed = 1
            while speed > 0:
                test_motor.run(speed)
                time.sleep(1)
                time_passed += 1
                actual_speed = test_motor.get_speed(1)
                print((actual_speed,))
                speed -= 0.1

            readings += 1

    # def encoder_position(iterations):
    #     test_motor = Motor(config.test_motorKit, config.pin_D5, config.pin_D6)
    #     test_encoder = Encoder(config.pin_D5, config.pin_D6)
    #     speed = 0
    #     time_passed = 0
    #     readings = 0
    #     while readings < iterations:
    #         while speed < 1:
    #             test_motor.run(speed)
    #             time.sleep(1)
    #             time_passed += 1
    #             print((actual_speed,))
    #             speed += 0.1

    #         speed = 1
    #         while speed > 0:
    #             test_motor.run(speed)
    #             time.sleep(1)
    #             time_passed += 1
    #             actual_speed = test_motor.get_speed(1)
    #             print((actual_speed,))
    #             speed -= 0.1

    #         readings += 1

