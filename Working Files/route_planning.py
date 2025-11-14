class Route:
    
    # The route for testing on Monday
    route = ['f', 'l', 'f', 'r', 'f', 'f', 'f', 'f', 'f', 'f', 'f', 'r', 'f', 'r', 'f', 'f', 'f', 'f', 'f', 'f', 'f', 'r', 'f', 'l', 'f']
    
    
    # No attributes to initialise - yet!
    def __init__(self):
        pass
    
    # Called when we reach an intersection (when front sensors detect something) to check what to do
    def intersection(self):
        try:
            instruction = self.route.pop() # Next instruction in the route
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
        except:
            return "stop" # Stop if list is empty - route finished!
    
