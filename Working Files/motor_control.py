class Motor_controller:
    
    left_motor_speed = 0
    right_motor_speed = 0    
    
    def __init__(self, left_dirPin, left_PWPin, right_dirPin, right_PWPin):
        self.left_Motor = self.Motor(left_dirPin, left_PWPin)
        self.right_Motor = self.Motor(right_dirPin, right_PWPin)
        
    def set_speeds(self, left_speed, right_speed)
        if left_speed >= 0:
            left_Motor.Forward(speed)
        else:
            left_Motor.Reverse(speed)
            
        self.left_motor_speed = left_speed
        
        if right_speed >= 0:
            right_Motor.Forward(speed)
        else:
            right_Motor.Reverse(speed)
            
        self.right_motor_speed = right_speed
    
    def move_straight(self, speed=100):
        set_speeds(speed, speed)
        
    def decrease_left_motor_speed(self, change_in_speed=20):
        new_left_speed = self.left_motor_speed - change_in_speed
        set_speeds(new_left_speed, self.right_motor_speed)
    
    def decrease_right_motor_speed(self, change_in_speed=20):
        new_right_speed = self.right_motor_speed - change_in_speed
        set_speeds(self.left_motor_speed, new_right_speed)
        
    def stop(self):
        set_speeds(0, 0)
        
    
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


def motor_testing():
    leftMotor = Motor(dirPin=4, PWMPin=5)  # Motor 3 is controlled from Motor Driv2 #1, which is on GP4/5
    rightMotor = Motor(dirPin=7, PWMPin=6)
    