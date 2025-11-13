from machine import Pin
from utime import sleep

#Set the LED pin and configuration
led_pin = 0
led = Pin(led_pin, Pin.OUT)


#Continiously update the LED value and print said value
while True:
  led.value(0)
  sleep(5)
  led.value(1)
  sleep(5)
