from machine import Pin, PWM
from utime import sleep
from motor_control import Motor_controller
from route_planning import Route

#Set the line sensor pins
line_sensor_outer_left_pin = 14
line_sensor_outer_right_pin = 15
line_sensor_inner_left_pin = 16
line_sensor_inner_right_pin = 17
line_sensor_outer_left = Pin(line_sensor_outer_left_pin, Pin.IN, Pin.PULL_DOWN)
line_sensor_outer_right = Pin(line_sensor_outer_right_pin, Pin.IN, Pin.PULL_DOWN)
line_sensor_inner_left = Pin(line_sensor_inner_left_pin, Pin.IN, Pin.PULL_DOWN)
line_sensor_inner_right = Pin(line_sensor_inner_right_pin, Pin.IN, Pin.PULL_DOWN) # 0=Black 1=White


def line_sensor_motor_control(motor_controller, route):

    #no upcoming corners/turns
    if line_sensor_outer_left.value() == 0 and line_sensor_outer_right.value() == 0:
        
        #forward movement when both sensors are inside the white line
        if line_sensor_inner_left.value() == 1 and line_sensor_inner_right.value() == 1:
            motor_controller.move_straight(95) #55
            
        elif line_sensor_inner_left.value() == 0 and line_sensor_inner_right.value() == 0:
            motor_controller.stop()
        
        #realign if either sensor is outside the white line
        elif line_sensor_inner_right.value() == 0:
            motor_controller.set_right_motor_speed(65) #25
            motor_controller.set_left_motor_speed(95) #55
        
        elif line_sensor_inner_left.value() == 0:
            motor_controller.set_left_motor_speed(65) #25
            motor_controller.set_right_motor_speed(95) #55
        
    # Approaching intersection - either of the front sensors detect something
    else:
        instruction = route.intersection()
        print(instruction)
        if instruction == "forwards":
            motor_controller.move_straight(85)   #45  # Move forward over the line to prevent double detection
            sleep(0.8)
        elif instruction == "backwards":
            motor_controller.move_straight(-80) #-40
            sleep(1)
        elif instruction == "turn":
            motor_controller.rotate(180)
        elif instruction == "left":
            motor_controller.move_straight(88)   #48    # Move forward so bot turns at the corner exactly
            sleep(1.7)
            motor_controller.rotate(90, "left")      # Rotate 90deg anticlockwise
        elif instruction == "right":
            motor_controller.move_straight(88)   #48   # Move forward so bot turns at the corner exactly
            sleep(1.7)
            motor_controller.rotate(90, "right")     # Rotate 90deg clockwise
        elif instruction == "stop":  
            motor_controller.move_straight(90)   #50   # Get into position so the whole bot is inside the finish area
            sleep(2.5)
            motor_controller.stop()
            sleep(1000)


