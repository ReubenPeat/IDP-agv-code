from machine import Pin
from utime import sleep
from line_sensor import line_sensor_motor_control
from motor_control import Motor_controller
from route_planning import Route
# from colour_sensor import block_identification
from box_detector import detection_trigger

#Set the button pin
button_pin = 12
button = Pin(button_pin, Pin.IN, Pin.PULL_DOWN)
  
line_sensor_outer_left_pin = 14
line_sensor_outer_right_pin = 15
line_sensor_inner_left_pin = 16
line_sensor_inner_right_pin = 17
line_sensor_outer_left = Pin(line_sensor_outer_left_pin, Pin.IN, Pin.PULL_DOWN)
line_sensor_outer_right = Pin(line_sensor_outer_right_pin, Pin.IN, Pin.PULL_DOWN)
line_sensor_inner_left = Pin(line_sensor_inner_left_pin, Pin.IN, Pin.PULL_DOWN)
line_sensor_inner_right = Pin(line_sensor_inner_right_pin, Pin.IN, Pin.PULL_DOWN)

#Set the LED pin and configuration
led_pin = 22
led = Pin(led_pin, Pin.OUT)

# Plug in left motor to slot 3, and right motor to slot 4
# Plug red on the left, and orange on the right
motor_controller = Motor_controller(4, 5, 7, 6)

route = Route(["Start", "IR", "PLL-1", "PUR-1", "PUR-2", "PUL-2", "PUL-1", "PLR-1", "IB", "Start"]) # initialise the first route

led.value(0)

while button.value() == 0:
    pass
while button.value() == 1:
    sleep(0.1)

led.value(1)

# Main loop: run until button pressed again
while True:
    # If button pressed again, exit
    if button.value() == 1:
        break

    # Line following control
    instruction = line_sensor_motor_control(motor_controller, route)

    if instruction == "No Instruction":
        pass
    else:
        boxFound = detectionTrigger(motor_controller, route)
        if boxFound:
            # Pick Up box
        else:
            if instruction == "forwards":
                motor_controller.move_straight(90)       # Move forward until over the line
                while line_sensor_outer_left.value() == 1 or line_sensor_outer_right.value() == 1:
                    pass
            elif instruction == "backwards":
                motor_controller.move_straight(-80)
                sleep(1)
            elif instruction == "turn":
                motor_controller.rotate(180)
            elif instruction == "left":
                motor_controller.rotate(90, "left")      # Rotate 90deg anticlockwise
            elif instruction == "right":
                motor_controller.rotate(90, "right")     # Rotate 90deg clockwise
            elif instruction == "stop":  
                motor_controller.stop()
                break

led.value(0)
# Stop the motors when exiting
motor_controller.stop()