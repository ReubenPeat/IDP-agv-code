from machine import Pin, PWM
from utime import sleep

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


def motor_testing():
    leftMotor = Motor(dirPin=4, PWMPin=5)  # Motor 3 is controlled from Motor Driv2 #1, which is on GP4/5
    rightMotor = Motor(dirPin=6, PWMPin=7)
    
    forward_button = Pin(12, Pin.IN, Pin.PULL_DOWN)
    left_button = Pin(13, Pin.IN, Pin.PULL_DOWN)
    right_button = Pin(14, Pin.IN, Pin.PULL_DOWN)

    while True:
        if forward_button.value() == 1:
            leftMotor.Forward()
            rightMotor.Forward()
            sleep(2)
            leftMotor.off()
            rightMotor.off()
            
            


if __name__ == "__main__":
    test_motor3()

