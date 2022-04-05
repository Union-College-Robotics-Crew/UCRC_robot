# @author: Edwin Garcia-Flores
  
import board
import analogio
from ulab import numpy as np
import time

VALIDATION_NUM = 20

class IR_sensor:
    
    def __init__(self, ir_config):
        adc = ir_config
        self.port = adc
        
    def __str__(self):
        return self.read()

    def median(self, lst = []):
        return np.median(lst)

    def convert_ADC_to_CM(self, adc_val):
        a = 0.000005  # linear member
        b = 0.0609  # free member
        k = 2   # Corrective Constant
        
        d = (1 / a) / (adc_val + b / a) - k

        return d
  
    def read(self):
        adc_readings = []
        for i in range(0,VALIDATION_NUM):
            cm_val = self.convert_ADC_to_CM(self.port.value)
            adc_readings.append(cm_val)
            time.sleep(.0001)
        return_val= self.median(np.array(adc_readings))
        return return_val
        

    def calibrate(self):
        readings = []
        for i in range(0,10):
            readings.append(self.read())
        self.initVal = np.median(np.array(readings))