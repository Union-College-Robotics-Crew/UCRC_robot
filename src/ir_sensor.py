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
        return self.read()
      
    def median(self, lst = []):
        return np.median(lst)
        
    def read(self):
        adc_readings = []
        while True:
            adc_readings.append(self.port.value)
            time.sleep(.0018)
            if len(adc_readings) % 10 == 0:
                return_val= self.median(np.array(adc_readings))
                adc_readings=[]
                return return_val
