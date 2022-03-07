# @author: Edwin Garcia-Flores
  
import board
import analogio
from ulab import numpy as np
import time
class IR_sensor:
    
    def __init__(self, ir_config):
        adc= ir_config
        self.port = adc
        
    def __str__(self):
        return (self.ir_reading(),)
    
    #adc = analogio.AnalogIn(port)
    def median(self, lst = []):
        return np.median(lst)
    def convert_ADC_to_CM(self, adc_val):
        a = 0.000005  # linear member
        b = 0.0609  # free member
        k = 2   # Corrective Constant
        
        d = (1 / a) / (adc_val + b / a) - k
        
        return d
        
    def ir_reading(self):
        adc_readings = []
        while True:
            cm_val = self.convert_ADC_to_CM(self.port.value)
            adc_readings.append(cm_val)
           # print("18ms have passed")
            time.sleep(.0018)
            if len(adc_readings) % 10 == 0:
                return_val= self.median(np.array(adc_readings))
                adc_readings=[]
                return return_val
