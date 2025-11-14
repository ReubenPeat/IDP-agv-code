from machine import Pin
from utime import sleep
from line_sensor import line_sensor_motor_control
from motor_control import Motor_controller
from route_planning import Route

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

route = Route() # initialise default route

led.value(0)

while button.value() == 0:
    sleep(0.1)
while button.value() == 1:
    pass

led.value(1)

# Main loop: run until button pressed again
while True:
    # If button pressed again → exit
    if button.value() == 1:
        break

    # Line following control
    line_sensor_motor_control(motor_controller, route)

led.value(0)
# Stop the motors when exiting
motor_controller.stop()