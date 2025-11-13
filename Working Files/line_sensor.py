from machine import Pin, PWM
from utime import sleep
from motor_control import Motor_controller

#Set the line sensor pins
line_sensor_front_left_pin = 14
line_sensor_front_right_pin = 15
line_sensor_back_left_pin = 16
line_sensor_back_right_pin = 17
line_sensor_front_left = Pin(line_sensor_front_left_pin, Pin.IN, Pin.PULL_DOWN)
line_sensor_front_right = Pin(line_sensor_front_right_pin, Pin.IN, Pin.PULL_DOWN)
line_sensor_back_left = Pin(line_sensor_back_left_pin, Pin.IN, Pin.PULL_DOWN)
line_sensor_back_right = Pin(line_sensor_back_right_pin, Pin.IN, Pin.PULL_DOWN) # 0=Black 1=White


def line_sensor_motor_control():
    leftMotor = Motor(dirPin=4, PWMPin=5)  # Motor 3 is controlled from Motor Driv2 #1, which is on GP4/5
    rightMotor = Motor(dirPin=7, PWMPin=6)
    
    motor_controller = Motor_controller(4, 5, 7, 6)

    #no upcoming corners/turns
    if line_sensor_front_left = False and line_sensor_front_right = False:
        
        #forward movement when both sensors are either side of white line
        if line_sensor_back_left = False and line_sensor_back_right = False:
            motor_controller.move_straight(100)
        
        #realign if either sensor is above the white line
        elif line_sensor_back_left = True:
            decrease_left_motor_speed(20)
        
        elif line_sensor_back_right = True:
            decrease_right_motor_speed(20)
         
        
    #approaching corner right turn
    elif line_sensor_front_right = True:
        decrease_right_motor_speed(100)
        sleep(1)
        
    #approaching corner left turn
    elif line_sensor_front_left = True:
        decrease_left_motor_speed(100)
        sleep(1)

