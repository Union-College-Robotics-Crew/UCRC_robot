class IR_sensor_tests:

	ir1 = IR_sensor(lAng_ir)
	ir2 = IR_sensor(rAng_ir)
	ir3 = IR_sensor(l_ir)
	ir4 = IR_sensor(r_ir)
	ir5 = IR_sensor(lFwd_ir)
	ir6 = IR_sensor(rFwd_ir)
	

	def test_ir(amt_readings):
		for i in range(amt_readings):
      print("ir1: ", ir1)
			print("ir2: ", ir2)
			print("ir3: ", ir3)
			print("ir4: ", ir4)
			print("ir5: ", ir5)
			print("ir6: ", ir6)
      
  test_ir(1000)
