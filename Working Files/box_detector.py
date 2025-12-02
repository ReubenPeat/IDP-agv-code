from machine import Pin, I2C
from libs.VL53L0X.VL53L0X import VL53L0X
from utime import sleep
from motor_control import Motor_controller
from line_sensor import line_sensor_motor_control
from route_planning import Route, Graph

line_sensor_inner_left_pin = 2
line_sensor_inner_right_pin = 8

line_sensor_inner_left = Pin(line_sensor_inner_left_pin, Pin.IN, Pin.PULL_DOWN)
line_sensor_inner_right = Pin(line_sensor_inner_right_pin, Pin.IN, Pin.PULL_DOWN)

def detection_trigger(motor_controller, route, vl53l0):
        
    # trigger box detection when robot reaches a line potentially leading to a box
    checkNodes = ["ILL-1",  "ILL-2", "ILL-3", "ILL-4", "ILL-5", "ILL-6",
                  "ILR-1",  "ILR-2", "ILR-3", "ILR-4", "ILR-5", "ILR-6",
                  "IUL-1",  "IUL-2", "IUL-3", "IUL-4", "IUL-5", "IUL-6",
                  "IUR-1",  "IUR-2", "IUR-3", "IUR-4", "IUR-5", "IUR-6"]
    current_position = route.get_currentPosition()
                 
    if current_position in checkNodes:
        # Start TOF sensor
        vl53l0.start()
        
        distanceReadings = 0
        for i in range(0,10):
            distanceReadings += vl53l0.read()
            sleep(0.1)
        distance = distanceReadings / 10
        # continue if there is no box
        if distance > 300:
            vl53l0.stop()         # Stop TOF sensor
            motor_controller.move_straight(90)
            
        # turn to collect box
        else:
            vl53l0.stop()         # Stop TOF sensor
            motor_controller.stop()
            sleep(0.1)
            motor_controller.move_straight(-50)
            sleep(1.2)
            motor_controller.stop()
            sleep(0.1)
            motor_controller.turn(90, "right")     # Rotate 90deg clockwise to face box
            
            # move forward until the line break
            motor_controller.move_straight(40)        
            
            while line_sensor_inner_left.value() == 1 or line_sensor_inner_right.value() == 1:
                #forward movement when both sensors are inside the white line
                if line_sensor_inner_left.value() == 1 and line_sensor_inner_right.value() == 1:
                    motor_controller.move_straight(55) #55
            
                elif line_sensor_inner_left.value() == 0 and line_sensor_inner_right.value() == 0:
                    break
        
                #realign if either sensor is outside the white line
                elif line_sensor_inner_right.value() == 0:
                    motor_controller.set_right_motor_speed(55) 
                    motor_controller.set_left_motor_speed(25) 
                
                elif line_sensor_inner_left.value() == 0:
                    motor_controller.set_left_motor_speed(55) 
                    motor_controller.set_right_motor_speed(25) 
           
            motor_controller.move_straight(40)
            sleep(0.2)
            motor_controller.stop()
            sleep(1)
    
            return True # Return that we found a box, to tell the main code
        
    return False

"""
# configure I2C Bus for distance sensor
i2c_bus = I2C(id=0, sda=Pin(16), scl=Pin(17)) # I2C0 on GP8 & GP9
print(i2c_bus.scan())  # Get the address (nb 41=0x29, 82=0x52)

vl53l0 = VL53L0X(i2c_bus)
vl53l0.set_Vcsel_pulse_period(vl53l0.vcsel_period_type[0], 18)
vl53l0.set_Vcsel_pulse_period(vl53l0.vcsel_period_type[1], 14)
motor_controller = Motor_controller(4, 5, 7, 6)
graph = Graph()
route = Route(graph, ["ILL-1", "ILL-2"])
while True:
    print(detection_trigger(motor_controller, route, vl53l0))
    sleep(0.5)
"""