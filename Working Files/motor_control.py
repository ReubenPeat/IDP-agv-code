from machine import Pin, PWM
from utime import sleep

class Motor_controller:
    
    left_motor_speed = 0
    right_motor_speed = 0    
    
    def __init__(self, left_dirPin, left_PWPin, right_dirPin, right_PWPin):
        self.left_Motor = self.Motor(left_dirPin, left_PWPin)
        self.right_Motor = self.Motor(right_dirPin, right_PWPin)
        
    def set_speeds(self, left_speed, right_speed):
        if left_speed >= 0:
            self.left_Motor.Forward(left_speed)
        else:
            self.left_Motor.Reverse(left_speed)
            
        self.left_motor_speed = left_speed
        
        if right_speed >= 0:
            self.right_Motor.Forward(right_speed)
        else:
            self.right_Motor.Reverse(right_speed)
            
        self.right_motor_speed = right_speed
    
    def move_straight(self, speed=50):
        self.set_speeds(speed, speed)
        
    def set_left_motor_speed(self, left_speed=50):
        self.set_speeds(left_speed, self.right_motor_speed)
        
    def set_right_motor_speed(self, right_speed=50):
        self.set_speeds(self.left_motor_speed, right_speed)
        
    def rotate(self, angle=180, direction="left"):
        self.stop()
        sleep(0.5)
        if direction == "left":
            self.set_speeds(-50, 50)
        else:
            self.set_speeds(50, -50)
            
        sleep(0.017*angle)
        
        self.move_straight(50)
        
    def decrease_left_motor_speed(self, change_in_speed=20):
        new_left_speed = self.left_motor_speed - change_in_speed
        self.set_speeds(new_left_speed, self.right_motor_speed)
    
    def decrease_right_motor_speed(self, change_in_speed=20):
        new_right_speed = self.right_motor_speed - change_in_speed
        self.set_speeds(self.left_motor_speed, new_right_speed)
        
    def stop(self):
        self.set_speeds(0, 0)
        
    
    class Motor:
        def __init__(self, dirPin, PWMPin):
            self.mDir = Pin(dirPin, Pin.OUT)  # set motor direction pin
            self.pwm = PWM(Pin(PWMPin))  # set motor pwm pin
            self.pwm.freq(1000)  # set PWM frequency
            self.pwm.duty_u16(0)  # set duty cycle - 0=off
            
        def off(self):
            self.pwm.duty_u16(0)
            
        def Forward(self, speed=100):
            self.mDir.value(0)                     # forward = 0; reverse = 1; motor
            self.pwm.duty_u16(int(65535 * speed / 100))  # speed range 0-100 motor

        def Reverse(self, speed=30):
            self.mDir.value(1)
            self.pwm.duty_u16(int(65535 * speed / 100))
