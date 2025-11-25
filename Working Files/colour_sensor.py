from machine import Pin, SoftI2C, I2C
from libs.tcs3472_micropython.tcs3472 import tcs3472
from utime import sleep
import time
import math

# TCS34725 I2C address
TCS34725_ADDR = 0x29
COMMAND_BIT = 0x80

# Register addresses
REG_ENABLE = 0x00
REG_ATIME = 0x01
REG_CONTROL = 0x0F
REG_ID = 0x12
REG_CDATAL = 0x14  # Clear channel data low byte
REG_RDATAL = 0x16
REG_GDATAL = 0x18
REG_BDATAL = 0x1A

# Enable register bits
ENABLE_AEN = 0x02  # RGBC enable
ENABLE_PON = 0x01  # Power ON

class TCS34725:
    def __init__(self, i2c, integration_time=0xEB, gain=0x01):
        self.i2c = i2c
        self.integration_time = integration_time
        self.gain = gain

        # Check sensor ID
        sensor_id = self._read8(REG_ID)
        if sensor_id not in (0x44, 0x10):
            raise RuntimeError("TCS34725 not found or wrong ID: 0x{:02X}".format(sensor_id))

        # Set integration time and gain
        self._write8(REG_ATIME, self.integration_time)
        self._write8(REG_CONTROL, self.gain)

        # Enable the device
        self.enable()

    def enable(self):
        self._write8(REG_ENABLE, ENABLE_PON)
        time.sleep_ms(3)
        self._write8(REG_ENABLE, ENABLE_PON | ENABLE_AEN)

    def disable(self):
        reg = self._read8(REG_ENABLE)
        self._write8(REG_ENABLE, reg & ~(ENABLE_PON | ENABLE_AEN))

    def _read8(self, reg):
        return self.i2c.readfrom_mem(TCS34725_ADDR, COMMAND_BIT | reg, 1)[0]

    def _read16(self, reg):
        data = self.i2c.readfrom_mem(TCS34725_ADDR, COMMAND_BIT | reg, 2)
        return data[1] << 8 | data[0]

    def _write8(self, reg, value):
        self.i2c.writeto_mem(TCS34725_ADDR, COMMAND_BIT | reg, bytes([value]))

    def read_raw(self):
        """Returns raw (clear, red, green, blue) values."""
        clear = self._read16(REG_CDATAL)
        red = self._read16(REG_RDATAL)
        green = self._read16(REG_GDATAL)
        blue = self._read16(REG_BDATAL)
        return clear, red, green, blue

    def calculate_color_temperature(self, r, g, b):
        """Approximate color temperature in Kelvin."""
        if r == 0 or g == 0 or b == 0:
            return 0
        X = (-0.14282 * r) + (1.54924 * g) + (-0.95641 * b)
        Y = (-0.32466 * r) + (1.57837 * g) + (-0.73191 * b)
        Z = (-0.68202 * r) + (0.77073 * g) + (0.56332 * b)
        if X + Y + Z == 0:
            return 0
        xc = X / (X + Y + Z)
        yc = Y / (X + Y + Z)
        n = (xc - 0.3320) / (0.1858 - yc)
        return int((449 * (n ** 3)) + (3525 * (n ** 2)) + (6823.3 * n) + 5520.33)

    def calculate_lux(self, r, g, b):
        """Approximate lux value."""
        return int((-0.32466 * r) + (1.57837 * g) + (-0.73191 * b))
    
    def calculate_ratios(self, r, g, b, clear):
        return [r / clear, g / clear, b / clear] 

# -------------------------
# Main program
# -------------------------


        #print("Clear: {}, Red: {}, Green: {}, Blue: {}".format(clear, red, green, blue))
        #print("Ratios: Red: {}, Green: {}, Blue: {}".format(red_ratio, green_ratio, blue_ratio))
        #print("Color Temp: {} K, Lux: {}".format(temp, lux))
        #print("-" * 40)
        #time.sleep(1)
        
        # Typical Values of ratios for the blocks, from 0-5cm away from the block
        # Red block:    r:0.35-0.46, g:0.21-0.29 b:0.26-0.36
        # Yellow block: r:0.30-0.41, g:0.35-0.44 b:0.22-0.26
        # Green block:  r:0.15-0.40, g:0.34-0.39 b:0.31-0.45
        # Blue block:   r:0.07-0.36, g:0.30-0.35 b:0.34-0.61     

except Exception as e:
    print("Error:", e)
    
def block_identification():
    try:
        # Initialize I2C (adjust pins for your board)
        i2c = I2C(1, scl=Pin(2), sda=Pin(3), freq=400000)
        print(i2c.scan())
        sensor = TCS34725(i2c)
        clear, red, green, blue = sensor.read_raw()
        temp = sensor.calculate_color_temperature(red, green, blue)
        lux = sensor.calculate_lux(red, green, blue)
        red_ratio, green_ratio, blue_ratio = sensor.calculate_ratios(red, green, blue, clear)
        if red_ratio > 0.35 and red_ratio < 0.46 and green_ratio > 0.21 and green_ratio < 0.29 and blue_ratio > 0.26 and blue_ratio < 0.36:
            return 'Red'
        elif red_ratio > 0.3 and red_ratio < 0.41 and green_ratio > 0.35 and green_ratio < 0.44 and blue_ratio > 0.22 and blue_ratio < 0.26:
            return 'Yellow'
        elif red_ratio > 0.15 and red_ratio < 0.6 and green_ratio > 0.34 and green_ratio < 0.39 and blue_ratio > 0.31 and blue_ratio < 0.45:
            return 'Green'
        elif red_ratio > 0.07 and red_ratio < 0.36 and green_ratio > 0.3 and green_ratio < 0.35 and blue_ratio > 0.34 and blue_ratio < 0.61:
            return 'Blue'
