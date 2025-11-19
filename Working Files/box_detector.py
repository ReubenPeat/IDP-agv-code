from machine import Pin, I2C
from libs.VL53L0X.VL53L0X import VL53L0X
from utime import sleep
from motor_control import Motor_controller
from line_sensor import line_sensor_motor_control

#from map import nodes

def detection_trigger():
    # config I2C Bus
    i2c_bus = I2C(id=0, sda=Pin(8), scl=Pin(9)) # I2C0 on GP8 & GP9
    # print(i2c_bus.scan())  # Get the address (nb 41=0x29, 82=0x52)
    
    # Setup vl53l0 object
    vl53l0 = VL53L0X(i2c_bus)
    vl53l0.set_Vcsel_pulse_period(vl53l0.vcsel_period_type[0], 18)
    vl53l0.set_Vcsel_pulse_period(vl53l0.vcsel_period_type[1], 14)


    while at white line/required node position:
        # Start device
        vl53l0.start()

        distance = vl53l0.read()
        
        # continue if there is no box
        if distance > 350:
            vl53l0.stop()         # Stop device
            line_sensor.line_sensor_motor_control(motor_controller, f)
        
        # turn to collect box
        else:
            vl53l0.stop()         # Stop device
            line_sensor.line_sensor_motor_control(motor_controller, r) # Rotate 90deg clockwise to face box
            
            # move forward until the line break
            line_sensor.line_sensor_motor_control(motor_controller, f)
            
            if line_sensor.line_sensor_inner_left.value() == 0 and line_sensor.line_sensor_inner_right.value() == 0:
                motor_controller.stop()
            
            #pick up box using linear actuator code
            