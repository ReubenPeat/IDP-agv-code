class Route:
    
    # The route for testing on Monday
    route = ['f', 'l', 'f', 'r', 'f', 'f', 'f', 'f', 'f', 'f', 'f', 'r', 'f', 'r', 'f', 'f', 'f', 'f', 'f', 'f', 'f', 'r', 'f', 'l', 'f']
    
    # No attributes to initialise - yet!
    def __init__(self):
        pass
    
    # Called when we reach an intersection (when front sensors detect something) to check what to do
    def intersection(self):
        instruction = self.route.pop() # Next instruction in the route
        if instruction == 'f':
            return "forward"      # forward
        elif instruction == 'b':
            return "backwards"    # reverse
        elif instruction == 't':
            return "turn"         # Turn 180 deg
        elif intstruction == 'l':
            if line_sensor_front_left.value() == 1:
                return "left"     # If the line goes to the left, follow it!
            else:
                self.route.insert(0, instruction)
                return "forward"  # Ignore
            
        elif intstruction == 'r':
            if line_sensor_front_right.value() == 1:
                return "right"    # If the line goes to the right, follow it!
            else:
                self.route.insert(0, instruction)
                return "forward"  # Ignore
    
    
    
    
    
    
    
line_sensor_front_left_pin = 14
line_sensor_front_right_pin = 15
line_sensor_front_left = Pin(line_sensor_front_left_pin, Pin.IN, Pin.PULL_DOWN)
line_sensor_front_right = Pin(line_sensor_front_right_pin, Pin.IN, Pin.PULL_DOWN)