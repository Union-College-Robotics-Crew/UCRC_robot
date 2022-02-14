from src import config
from src import ir_sensor

import time

class IR_sensor_tests:
	def __init__(self):
		self.ir1 = ir_sensor.IR_sensor(config.lAng_ir)
		self.ir2 = ir_sensor.IR_sensor(config.rAng_ir)
		self.ir3 = ir_sensor.IR_sensor(config.l_ir)
		self.ir4 = ir_sensor.IR_sensor(config.r_ir)
		self.ir5 = ir_sensor.IR_sensor(config.lFwd_ir)
		self.ir6 = ir_sensor.IR_sensor(config.rFwd_ir)
	

	def test_ir(amt_readings):
		for i in range(amt_readings):
#       			print("ir1: ", self.ir1)
# 			print("ir2: ", self.ir2)
# 			print("ir3: ", self.ir3)
# 			print("ir4: ", self.ir4)
# 			print("ir5: ", self.ir5)
# 			print("ir6: ", self.ir6)
			print(self.ir1, self.ir2, self.ir3, self.ir4, self.ir5, self.ir6)
			time.sleep(1)
IR_tests = IR_sensor_tests()
print(IR_tests.test_ir(1000))
