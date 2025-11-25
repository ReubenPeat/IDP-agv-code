from machine import Pin, PWM
from utime import sleep

FULL_STROKE_TIME_S   = 8.02
TOTAL_FORK_TRAVEL_MM = 50.0   

# Lift amounts (mm)
LIFT_UP_TOP_MM    = 6.0    
LIFT_UP_BOTTOM_MM = 4.0   

# Bottom floor: from full extension up to bottom pickup height
BOTTOM_PRE_PICK_RAISE_MM = 19.0

# Bottom floor: after pull-back, lower slightly to carry height
BOTTOM_LOWER_AFTER_PULL_MM = 2.0

# Bottom floor drop: from carry, lower 16 mm to place box on floor
BOTTOM_DROP_EXTRA_MM = 16.0

# Top floor drop: undo the top lift
DROP_TOP_MM = LIFT_UP_TOP_MM


def mm_to_time(mm):
    return FULL_STROKE_TIME_S * (mm / TOTAL_FORK_TRAVEL_MM)

# Convert mm → seconds
LIFT_UP_TOP_TIME_S        = mm_to_time(LIFT_UP_TOP_MM)
LIFT_UP_BOTTOM_TIME_S     = mm_to_time(LIFT_UP_BOTTOM_MM)
BOTTOM_PRE_PICK_RAISE_S   = mm_to_time(BOTTOM_PRE_PICK_RAISE_MM)
BOTTOM_LOWER_AFTER_PULL_S = mm_to_time(BOTTOM_LOWER_AFTER_PULL_MM)
BOTTOM_DROP_EXTRA_TIME_S  = mm_to_time(BOTTOM_DROP_EXTRA_MM)
DROP_TOP_TIME_S           = mm_to_time(DROP_TOP_MM)

# Safety limit for homing
MAX_TRAVEL_TIME_S = 8.02

DIR_EXTEND  = 0   # towards full extension 
DIR_RETRACT = 1   # away from full extension


class Actuator:
    def __init__(self, dirPin, PWMPin):
        self.mDir = Pin(dirPin, Pin.OUT)
        self.pwm = PWM(Pin(PWMPin))
        self.pwm.freq(1000)
        self.stop()

        # t_from_ref = 0.0 means FULL EXTENSION
        self.t_from_ref = 0.0

    def run(self, direction, speed_percent):
        self.mDir.value(direction)
        duty = int(65535 * speed_percent / 100)
        self.pwm.duty_u16(duty)

    def stop(self):
        self.pwm.duty_u16(0)

    def home_full_extension(self):
        print("Homing to FULL EXTENSION...")
        self.run(DIR_EXTEND, 80)
        sleep(MAX_TRAVEL_TIME_S)
        self.stop()
        self.t_from_ref = 0.0
        print("Home complete. Reference = full extension.")

    def _nudge_up(self, t_s):
        """
        Move fork UP (away from full extension) for t_s seconds (time-based).
        """
        if t_s <= 0:
            return
        new_t = min(self.t_from_ref + t_s, MAX_TRAVEL_TIME_S)
        dt = new_t - self.t_from_ref
        if dt > 0:
            self.run(DIR_RETRACT, 100)
            sleep(dt)
            self.stop()
            self.t_from_ref = new_t

    def _nudge_down(self, t_s):
        """
        Move fork DOWN (towards full extension) for t_s seconds (time-based).
        """
        if t_s <= 0:
            return
        new_t = max(self.t_from_ref - t_s, 0.0)
        dt = self.t_from_ref - new_t
        if dt > 0:
            self.run(DIR_EXTEND, 100)
            sleep(dt)
            self.stop()
            self.t_from_ref = new_t

    # TOP FLOOR: PICK + CARRY + DROP

    def top_floor_pick_and_carry(self):
        """
        TOP FLOOR:
          - Start at full extension (pickup height 5 mm).
          - Robot drives forward into block. 
          - Raise +6 mm to carry height.
          - Robot pulls back with block.      
        """
        self._nudge_up(LIFT_UP_TOP_TIME_S)
    

    def top_floor_drop_off(self):
        """
        TOP FLOOR DROP:
          - Start at top carry height (+6 mm above pickup).
          - Robot drives forward to drop position. 
          - Lower 6 mm to place box on top-floor surface.
          - Robot reverses to clear fork.        
        """
        self._nudge_down(DROP_TOP_TIME_S)
        
    # BOTTOM FLOOR: PICK + CARRY + DROP
    def bottom_floor_pick_and_carry(self):
        """
        BOTTOM FLOOR:
          - Start at full extension (5 mm).
          - Raise 19 mm to bottom-floor pickup height.
          - Robot drives forward into block.      [external]
          - Raise +4 mm for clearance / lift.
          - Robot pulls back with block.          [external]
          - Lower 2 mm to final carry height.
        """
        # From full extension up to the bottom pickup height
        self._nudge_up(BOTTOM_PRE_PICK_RAISE_S)

        # (Robot drives forward here – done externally)

        # Lift inside the block
        self._nudge_up(LIFT_UP_BOTTOM_TIME_S)

        # Small drop to carry height
        self._nudge_down(BOTTOM_LOWER_AFTER_PULL_S)

    def bottom_floor_drop_off(self):
        """
        BOTTOM FLOOR DROP:
          - Start at bottom carry height.
          - Robot drives forward to drop position.    
          - Lower 16 mm so box rests on ground.
          - Robot reverses to clear fork.             
        """
        self._nudge_down(BOTTOM_DROP_EXTRA_TIME_S)

    def go_full_extension(self):
        self.home_full_extension()


def main():
    actuator = Actuator(dirPin=0, PWMPin=1)

    # Home once at startup
    actuator.home_full_extension()

    # TOP FLOOR sequence
    actuator.top_floor_pick_and_carry()
    # (your drive code moves robot to drop-off)
    actuator.top_floor_drop_off()

    # BOTTOM FLOOR sequence
    actuator.go_full_extension()        
    actuator.bottom_floor_pick_and_carry()
    # drive code moves robot to drop off
    actuator.bottom_floor_drop_off()


if __name__ == "__main__":
    main()

