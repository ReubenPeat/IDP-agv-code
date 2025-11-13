from machine import Pin
from utime import sleep
from line_sensor import line_sensor_motor_control
from motor_control import Motor_controller

"""
#Set the LED pin and configuration
led_pin = 28
led = Pin(led_pin, Pin.OUT)

#Set the button pin
button_pin = 12
button = Pin(button_pin, Pin.IN, Pin.PULL_DOWN)

#Continiously update the LED value and print said value
while True:
  led.value(button.value())
  sleep(0.1)
  print(button.value())
"""

motor_controller = Motor_controller(4, 5, 7, 6)
# Plug in left motor to slot 3, and right motor to slot 4
# Plug red on the left, and orange on the right
while True:
    line_sensor_motor_control(motor_controller)