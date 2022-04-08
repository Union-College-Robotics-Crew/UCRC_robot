from adafruit_ble import BLERadio
from adafruit_ble.advertising.standard import ProvideServicesAdvertisement
from adafruit_ble.services.nordic import UARTService
class BLE_Comm:
    def __init__(self):
        self.ble = BLERadio()
        self.uart = UARTService()
        self.advertisement = ProvideServicesAdvertisement(self.uart)

    def send(self, val):
        if self.ble.connected:
            val_str= str(val)
            self.uart.write(val_str)

    # def get_val(self):
    #     if ble.connected:
    #         s = uart.readline()
    #         if s:
    #             try:
    #                 result = str(eval(s))
    #             except Exception as e:
    #                 result = repr(e)
    #             uart.write(result.encode("utf-8"))
