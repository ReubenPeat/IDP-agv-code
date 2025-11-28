from machine import Pin
from utime import sleep
from line_sensor import line_sensor_motor_control
from motor_control import Motor_controller
from route_planning import Route
from route_planning import Graph
from colour_sensor import block_identification
from box_detector import detection_trigger
from linear_actuator import Actuator

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

# Initialise actuator pins
actuator = Actuator(dirPin=0, PWMPin=1)

# Actuator default
#actuator.home_full_extension()

# Plug in left motor to slot 3, and right motor to slot 4
# Plug red on the left, and orange on the right
motor_controller = Motor_controller(4, 5, 7, 6)
graph = Graph()

verticesToCheck = ["IR",    "ILL-1", "ILL-2", "ILL-3", "ILL-4", "ILL-5", "ILL-6",
                   "PUR-1", "IUR-1", "IUR-2", "IUR-3", "IUR-4", "IUR-5", "IUR-6",
                   "PUL-2", "IUL-6", "IUL-5", "IUL-4", "IUL-3", "IUL-2", "IUL-1",
                   "PLR-1", "ILR-6", "ILR-5", "ILR-4", "ILR-3", "ILR-2", "ILR-1"]    # We must visit all of these in order to check for blocks

route = Route(graph, ["Start", verticesToCheck.pop(0)]) # initialise the first route
hasBox = False


led.value(0)

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
        
        if hasBox==False:
            boxFound = detection_trigger(motor_controller, route)
            if boxFound:
                
                # Pick up box
                if route.isOnUpperFloor() == True:
                    # TOP FLOOR sequence
                    actuator.top_floor_pick_and_carry()
                    
                else:
                    # BOTTOM FLOOR sequence       
                    actuator.bottom_floor_pick_and_carry()
                    
                colour = block_identification()         # Identify the colour of the block picked up
                hasBox = True
                
                while colour == " ":                    # Repeat until a colour is found
                    colour = block_identification()
                    sleep(0.1)
                
                intersectionPosition = route.get_currentPosition()
                actualCurrentPosition = "B" + intersectionPosition[1:]  # Update the current position to the bay, since we moved there without telling the route object
                
                route = Route(graph, [actualCurrentPosition, colour])   # create a new route leading back to the start
                instruction = route.intersection()                      # Call intersection to tell the route object we will now turn around
                
                motor_controller.move_straight(-80)
                sleep(1)
                motor_controller.rotate(180)
                motor_controller.stop()                           # Reverse out and turn around ready to path back to the start
            
        else:
            if instruction == "forwards":
                motor_controller.move_straight(90)       # Move forward until over the line
                while line_sensor_outer_left.value() == 1 or line_sensor_outer_right.value() == 1:
                    pass
            elif instruction == "backwards":
                motor_controller.move_straight(-80)
                sleep(1)
            elif instruction == "turn":
                motor_controller.rotate(180)
            elif instruction == "left":
                motor_controller.rotate(90, "left")      # Rotate 90deg anticlockwise
            elif instruction == "right":
                motor_controller.rotate(90, "right")     # Rotate 90deg clockwise
            elif instruction == "stop":  
                motor_controller.stop()
                break
        
        if route.isAtEndOfRoute():
            if hasBox:                  # If we have a box then drop it off!
                motor_controller.move_straight(80)
                sleep(1)
                
                # Drop off box
                actuator.drop_off()
                actuator.home_full_extension()
                hasBox = False
                instruction = route.intersection()                # Call intersection to tell the route object we will now turn around
                motor_controller.move_straight(-80)
                sleep(1)
                motor_controller.rotate(180)
                
            if len(verticesToCheck) > 0:
                route = Route(graph, [route.get_currentPosition(), verticesToCheck.pop(0)])
            else:
                route = Route(graph, [route.get_currentPosition(), "Start"])

led.value(0)
# Stop the motors when exiting
motor_controller.stop()