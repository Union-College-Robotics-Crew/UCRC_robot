import time
import board
import math
import adafruit_lis2mdl
from adafruit_ble import BLERadio
from adafruit_ble.advertising.standard import ProvideServicesAdvertisement
from adafruit_ble.services.nordic import UARTService

class Magnetometer:

    def __init__(self):
        i2c = board.I2C()  # uses board.SCL and board.SDA
        self.sensor = adafruit_lis2mdl.LIS2MDL(i2c)
        # "hardiron_calibration" MUST be calibrated and set:
        self.hardiron_calibration = [[1000, -1000], [1000, -1000], [1000, -1000]]

    def __actual_calibration(self):
        hardiron_calibration = [[1000, -1000], [1000, -1000], [1000, -1000]]
        start_time = time.monotonic()

        # Update the high and low extremes
        while time.monotonic() - start_time < 10.0:
            magval = self.sensor.magnetic
            print("Calibrating - X:{0:10.2f}, Y:{1:10.2f}, Z:{2:10.2f} uT".format(*magval))
            for i, axis in enumerate(magval):
                hardiron_calibration[i][0] = min(hardiron_calibration[i][0], axis)
                hardiron_calibration[i][1] = max(hardiron_calibration[i][1], axis)
        print("Calibration complete:")
        print("hardiron_calibration =", hardiron_calibration)

    def calibrate(self):
        print("Prepare to calibrate! Twist the magnetometer around in 3D in...")
        print("3...")
        time.sleep(1)
        print("2...")
        time.sleep(1)
        print("1...")
        time.sleep(1)

        self.__actual_calibration()

    def __normalize(self, magvals):
        ret = [0, 0, 0]
        for i, axis in enumerate(magvals):
            minv, maxv = self.hardiron_calibration[i]
            axis = min(max(minv, axis), maxv)  # keep within min/max calibration
            ret[i] = (axis - minv) * 200 / (maxv - minv) + -100
        return ret

    def heading(self):
        magvals = self.sensor.magnetic
        normvals = self.__normalize(magvals)
        print("magnetometer: %s -> %s" % (magvals, normvals))

        # we will only use X and Y for the compass calculations, so hold it level!
        compass_heading = int(math.atan2(normvals[1], normvals[0]) * 180.0 / math.pi)
        # compass_heading is between -180 and +180 since atan2 returns -pi to +pi
        # this translates it to be between 0 and 360
        compass_heading += 180

        print("Heading:", compass_heading)

        return compass_heading

