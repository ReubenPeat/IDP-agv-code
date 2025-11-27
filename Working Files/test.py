from motor_control import Motor_controller
from utime import sleep
from linear_actuator import Actuator

motor_controller = Motor_controller(4, 5, 7, 6)
"""
motor_controller.stop()

motor_controller.set_left_motor_speed(100)

sleep(2)

motor_controller.stop()

motor_controller.set_right_motor_speed(100)

sleep(2)

motor_controller.move_straight(70)

sleep(2)

motor_controller.stop()
"""
actuator = Actuator(0, 1)

actuator.go_full_extension()
actuator.top_floor_pick_and_carry()