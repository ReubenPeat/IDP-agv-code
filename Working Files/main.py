from machine import Pin, I2C
from libs.VL53L0X.VL53L0X import VL53L0X
from utime import sleep
from line_sensor import line_sensor_motor_control
from motor_control import Motor_controller
from route_planning import Route
from route_planning import Graph
from colour_sensor import block_identification
from box_detector import detection_trigger
from linear_actuator_Luke import Actuator

#Set the button pin
button_pin = 18
button = Pin(button_pin, Pin.IN, Pin.PULL_DOWN)

#Set line sensor pins
line_sensor_outer_left_pin = 3
line_sensor_outer_right_pin = 9
line_sensor_inner_left_pin = 2
line_sensor_inner_right_pin = 8
line_sensor_outer_left = Pin(line_sensor_outer_left_pin, Pin.IN, Pin.PULL_DOWN)
line_sensor_outer_right = Pin(line_sensor_outer_right_pin, Pin.IN, Pin.PULL_DOWN)
line_sensor_inner_left = Pin(line_sensor_inner_left_pin, Pin.IN, Pin.PULL_DOWN)
line_sensor_inner_right = Pin(line_sensor_inner_right_pin, Pin.IN, Pin.PULL_DOWN)

#Set the LED pin and configuration
led_pin = 26
led = Pin(led_pin, Pin.OUT)

led.value(0)

# configure I2C Bus for distance sensor
i2c_ToF = I2C(id=0, sda=Pin(16), scl=Pin(17)) # I2C0 on GP8 & GP9
#print(i2c_ToF.scan())  # Get the address (nb 41=0x29, 82=0x52)
    
# Setup time of flight sensor
vl53l0 = VL53L0X(i2c_ToF)
vl53l0.set_Vcsel_pulse_period(vl53l0.vcsel_period_type[0], 18)
vl53l0.set_Vcsel_pulse_period(vl53l0.vcsel_period_type[1], 14)

vl53l0.start()
print(vl53l0.read())
vl53l0.stop()        # Take a reading to check for errors

# Setup colour sensor enable pin - but don't turn it on
enable_CS_pin = 11
enable_CS = Pin(enable_CS_pin, Pin.OUT)
enable_CS.value(0)

# Initialise actuator pins
actuator = Actuator(dirPin=0, PWMPin=1)
actuator.bottomFloorPickUp()


# Plug in left motor to slot 3, and right motor to slot 4
# Plug red on the left, and orange on the right
motor_controller = Motor_controller(4, 5, 7, 6)
graph = Graph()

verticesToCheck = ["ILL-1", "ILL-2", "ILL-3", "ILL-4", "ILL-5", "ILL-6",
                   "IUR-1", "IUR-2", "IUR-3", "IUR-4", "IUR-5", "IUR-6",
                   "IUL-6", "IUL-5", "IUL-4", "IUL-3", "IUL-2", "IUL-1",
                   "ILR-6", "ILR-5", "ILR-4", "ILR-3", "ILR-2", "ILR-1"]    # We must visit all of these in order to check for blocks

defaultRoute = Route(graph, ["Start", "IR", "PLL-1", "PLR-1", "IB", "Start"]) # initialise the first route
# Full route: ["Start", "IR", "PLL-1", "PUR-1", "PUR-2", "PUL-2", "PUL-1", "PLR-1", "IB", "Start"]
route = defaultRoute
hasBox = False

def pick_up_box(route, graph, actuator):
    actuator.pickUp()
        
    colour = block_identification(enable_CS)         # Identify the colour of the block picked up
    hasBox = True
    
    for i in range(0, 10):
        if colour != " ":
            colour = block_identification(enable_CS)
            sleep(0.2)
            if colour != " " and i == 9:
                colour = "Red"
            print(colour)
        else:
            break
        
        
    
    intersectionPosition = route.previousPosition
    actualCurrentPosition = "B" + intersectionPosition[1:]  # Update the current position to the bay, since we moved there without telling the route object
    print(actualCurrentPosition)
    route = Route(graph, [actualCurrentPosition, colour])   # create a new route leading back to the start
    instruction = route.intersection()                      # Call intersection to tell the route object we will now turn around
    
    motor_controller.move_straight(-80)
    sleep(4)
    motor_controller.stop()
    motor_controller.rotate180()
    motor_controller.stop()                           # Reverse out and turn around ready to path back to the start

def drop_off_box(route, graph, actuator):
    motor_controller.move_straight(80)
    sleep(1)
    
    # Drop off box
    actuator.dropOff()
    hasBox = False
    instruction = route.intersection()                # Call intersection to tell the route object we will now turn around
    motor_controller.move_straight(-80)
    sleep(1)
    motor_controller.rotate180()

print("Ready")
while button.value() == 0:
    pass
while button.value() == 1:
    sleep(0.1)



while line_sensor_inner_right.value() == 0 or line_sensor_inner_left.value() == 0:
    motor_controller.move_straight()        # Initially, we will be in the start box - no line to follow, so go forward until you find it
    

led.value(0)

# Main loop: run until button pressed again
while True:
    # If button pressed again, exit
    if button.value() == 1:
        break
    if route.get_currentPosition() == "Start":
        led.value(0)
    else:
        led.value(1)

    # Line following control
    instruction = line_sensor_motor_control(motor_controller, route)
    
    if instruction == "No Instruction":
        pass
    else:
        boxFound = False
        if hasBox==False:
            if route.get_currentPosition() == verticesToCheck[0]:
                motor_controller.stop()
                sleep(0.5)
                if route.isOnUpperFloor() == True:
                    # TOP FLOOR sequence
                    actuator.topFloorPickUp()
                    pass
                else:
                    # BOTTOM FLOOR sequence       
                    actuator.bottomFloorPickUp()
                    pass
                print("Checking for box")
                boxFound = detection_trigger(motor_controller, route, vl53l0)
                verticesToCheck.pop(0)
                print(boxFound)
        if boxFound == True:
            pick_up_box(route, graph, actuator) 
        else:
            if instruction == "forwards":
                motor_controller.move_straight(90)       # Move forward until over the line
                while line_sensor_outer_left.value() == 1 or line_sensor_outer_right.value() == 1:
                    pass
                sleep(0.1)
            elif instruction == "backwards":
                motor_controller.move_straight(-80)
                sleep(1)
            elif instruction == "turn":
                motor_controller.rotate180()
            elif instruction == "left":
                motor_controller.turn(90, "left")      # Rotate 90deg anticlockwise
            elif instruction == "right":
                motor_controller.turn(90, "right")     # Rotate 90deg clockwise
            elif instruction == "stop":  
                motor_controller.stop()
                break
        
        if route.isAtEndOfRoute():
            if hasBox:                  # If we have a box then drop it off!
                drop_off_box(route, graph, actuator)
            if len(verticesToCheck) > 0:
                route = defaultRoute

led.value(0)
# Stop the motors when exiting
motor_controller.stop()