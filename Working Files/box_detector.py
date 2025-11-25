from machine import Pin, I2C
from libs.VL53L0X.VL53L0X import VL53L0X
from utime import sleep
from motor_control import Motor_controller
from line_sensor import line_sensor_motor_control
from route_planning import Route

# from map import nodes

def detection_trigger(motor_controller, route):
    # config I2C Bus
    i2c_bus = I2C(id=0, sda=Pin(8), scl=Pin(9)) # I2C0 on GP8 & GP9
    # print(i2c_bus.scan())  # Get the address (nb 41=0x29, 82=0x52)
    
    # Setup time of flight sensor
    vl53l0 = VL53L0X(i2c_bus)
    vl53l0.set_Vcsel_pulse_period(vl53l0.vcsel_period_type[0], 18)
    vl53l0.set_Vcsel_pulse_period(vl53l0.vcsel_period_type[1], 14)
    
    # trigger box detection when robot reaches a line potentially leading to a box
    checkNodes = ["ILL-1",  "ILL-2", "ILL-3", "ILL-4", "ILL-5", "ILL-6",
                  "ILR-1",  "ILR-2", "ILR-3", "ILR-4", "ILR-5", "ILR-6",
                  "IUL-1",  "IUL-2", "IUL-3", "IUL-4", "IUL-5", "IUL-6",
                  "IUR-1",  "IUR-2", "IUR-3", "IUR-4", "IUR-5", "IUR-6"]
    current_position = route.get_currentPosition()
                    
    if current_position in checkNodes:
        # Start TOF sensor
        vl53l0.start()

        distance = vl53l0.read()
        
        # continue if there is no box
        if distance > 350:
            vl53l0.stop()         # Stop TOF sensor
            motor_controller.move_straight(90)
            
        # turn to collect box
        else:
            vl53l0.stop()         # Stop TOF sensor
            motor_controller.rotate(90, "right")     # Rotate 90deg clockwise to face box
            
            # move forward until the line break
            motor_controller.move_straight(40)        
            
            while line_sensor.line_sensor_inner_left.value() == 1 or line_sensor.line_sensor_inner_right.value() == 1:
                line_sensor.line_sensor_motor_control(motor_controller, route)
            
            motor_controller.stop()
            
            return True # Return that we found a box, to tell the main code
        
    return False
            
            # pick up box using linear actuator code
            
            # call colour sensor to check that the block is on the forklift periodically during journey 