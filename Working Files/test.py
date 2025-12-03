from motor_control import Motor_controller
from utime import sleep
from linear_actuator_Luke import Actuator

motor_controller = Motor_controller(4, 5, 7, 6)


actuator = Actuator(0, 1)
sleep(0.5)
actuator.bottomFloorPickUp()
sleep(0.5)
actuator.pickUp()
sleep(0.5)
actuator.carry()