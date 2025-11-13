from machine import Pin, PWM
from utime import sleep

#Set the line sensor pins
line_sensor_front_left_pin = 14
line_sensor_front_right_pin = 15
line_sensor_back_left_pin = 16
line_sensor_back_right_pin = 17
line_sensor_front_left = Pin(line_sensor_front_left_pin, Pin.IN, Pin.PULL_DOWN)
line_sensor_front_right = Pin(line_sensor_front_right_pin, Pin.IN, Pin.PULL_DOWN)
line_sensor_back_left = Pin(line_sensor_back_left_pin, Pin.IN, Pin.PULL_DOWN)
line_sensor_back_right = Pin(line_sensor_back_right_pin, Pin.IN, Pin.PULL_DOWN) # 0=Black 1=White

class Motor:
    def __init__(self, dirPin, PWMPin):
        self.mDir = Pin(dirPin, Pin.OUT)  # set motor direction pin
        self.pwm = PWM(Pin(PWMPin))  # set motor pwm pin
        self.pwm.freq(1000)  # set PWM frequency
        self.pwm.duty_u16(0)  # set duty cycle - 0=off
        
    def off(self):
        self.pwm.duty_u16(0)
        
    def Forward(self, speed=100):
        self.mDir.value(0)                     # forward = 0 reverse = 1 motor
        self.pwm.duty_u16(int(65535 * speed / 100))  # speed range 0-100 motor

    def Reverse(self, speed=30):
        self.mDir.value(1)
        self.pwm.duty_u16(int(65535 * speed / 100))


def motor_control():
    leftMotor = Motor(dirPin=4, PWMPin=5)  # Motor 3 is controlled from Motor Driv2 #1, which is on GP4/5
    rightMotor = Motor(dirPin=7, PWMPin=6)

    #realign if either sensor is above the white line
    if line_sensor_back_left = True:
        
    elif line_sensor_back_right = True:

    #forward movement when both 
    elif line_sensor_back_left = False and line_sensor

    while True:
        if forward_button.value() == 1:
            leftMotor.Forward()
            rightMotor.Forward()
            sleep(1)
            leftMotor.off()
            rightMotor.off()
        elif left_button.value() == 0:
            leftMotor.Reverse()
            rightMotor.Forward()
            sleep(0.5)
            leftMotor.off()
            rightMotor.off()
        elif right_button.value() == 0:
            leftMotor.Forward()
            rightMotor.Reverse()
            sleep(0.5)
            leftMotor.off()
            rightMotor.off()
            


