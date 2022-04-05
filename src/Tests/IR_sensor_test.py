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
	

	def test_ir(self, amt_readings):
		for i in range(amt_readings):
			print((self.ir1.read(), self.ir2.read(), self.ir3.read(), self.ir4.read(), self.ir5.read(), self.ir6.read()),)
			time.sleep(1)
IR_tests = IR_sensor_tests()
print(IR_tests.test_ir(1000))
