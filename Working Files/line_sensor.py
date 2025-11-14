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
        
        #forward movement when both sensors are either side of white line
        if line_sensor_inner_left.value() == 0 and line_sensor_inner_right.value() == 0:
            motor_controller.move_straight(55)
            
        elif line_sensor_inner_left.value() == 1 and line_sensor_inner_right.value() == 1:
            motor_controller.stop()
        
        #realign if either sensor is above the white line
        elif line_sensor_inner_right.value() == 1:
            motor_controller.set_right_motor_speed(25)
            motor_controller.set_left_motor_speed(55)
        
        elif line_sensor_inner_left.value() == 1:
            motor_controller.set_left_motor_speed(25)
            motor_controller.set_right_motor_speed(55)
        
    # Approaching intersection - either of the front sensors detect something
    else:
        instruction = route.intersection()
        print(instruction)
        if instruction == "forwards":
            motor_controller.move_straight(55)
            sleep(0.8)
        elif instruction == "backwards":
            motor_controller.move_straight(-40)
            sleep(1)
        elif instruction == "turn":
            motor_controller.rotate(180)
        elif instruction == "left":
            motor_controller.move_straight(50)
            sleep(1.7)
            motor_controller.rotate(90, "left")
        elif instruction == "right":
            motor_controller.move_straight(50)
            sleep(1.7)
            motor_controller.rotate(90, "right")
        elif instruction == "stop":
            motor_controller.stop()
            sleep(10)


