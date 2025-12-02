from motor_control import Motor_controller
from utime import sleep
from linear_actuator import Actuator

motor_controller = Motor_controller(4, 5, 7, 6)


motor_controller.rotate180()