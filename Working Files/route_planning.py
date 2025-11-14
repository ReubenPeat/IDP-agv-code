class Route:
    
    # The route for testing on Monday
    route = ['f', 'l', 'f', 'r', 'f', 'f', 'f', 'f', 'f', 'f', 'f', 'r', 'f', 'r', 'f', 'f', 'f', 'f', 'f', 'f', 'f', 'r', 'f', 'l', 's']
    # No attributes to initialise - yet!
    def __init__(self):
        pass
    
    # Called when we reach an intersection (when front sensors detect something) to check what to do
    def intersection(self):
        instruction = self.route.pop(0) # Next instruction in the route
        print(self.route)
        print(instruction)
        if instruction == 'f':
            return "forwards"     # forwards
        elif instruction == 'b':
            return "backwards"    # reverse
        elif instruction == 't':
            return "turn"         # Turn 180 deg
        elif instruction == 'l':
            return "left"     # If the line goes to the left, follow it!
        elif instruction == 'r':
            return "right"    # If the line goes to the right, follow it!
        elif instruction == 's':
            return "stop"
    
