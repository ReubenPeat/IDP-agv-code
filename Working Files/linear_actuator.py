from machine import Pin, PWM
from utime import sleep

FULL_STROKE_TIME_S   = 8.02
TOTAL_FORK_TRAVEL_MM = 50.0   

# Lift amounts (mm)
# Top lift adjusted so top-floor carry height = bottom-floor carry height (21 mm)
LIFT_UP_TOP_MM    = 21.0      
LIFT_UP_BOTTOM_MM = 4.0       

# Bottom floor: from full extension to bottom pickup height
BOTTOM_PRE_PICK_RAISE_MM = 19.0

# Bottom floor: settle after pull-back
BOTTOM_LOWER_AFTER_PULL_MM = 2.0

# UNIVERSAL drop distance from carry to floor
DROP_FROM_CARRY_MM = 16.0     

def mm_to_time(mm):
    return FULL_STROKE_TIME_S * (mm / TOTAL_FORK_TRAVEL_MM)

# Convert mm → seconds
LIFT_UP_TOP_TIME_S        = mm_to_time(LIFT_UP_TOP_MM)
LIFT_UP_BOTTOM_TIME_S     = mm_to_time(LIFT_UP_BOTTOM_MM)
BOTTOM_PRE_PICK_RAISE_S   = mm_to_time(BOTTOM_PRE_PICK_RAISE_MM)
BOTTOM_LOWER_AFTER_PULL_S = mm_to_time(BOTTOM_LOWER_AFTER_PULL_MM)
DROP_FROM_CARRY_TIME_S    = mm_to_time(DROP_FROM_CARRY_MM)

MAX_TRAVEL_TIME_S = FULL_STROKE_TIME_S

DIR_EXTEND  = 0   # towards full extension 
DIR_RETRACT = 1   # away from full extension


class Actuator:
    def __init__(self, dirPin, PWMPin):
        self.mDir = Pin(dirPin, Pin.OUT)
        self.pwm = PWM(Pin(PWMPin))
        self.pwm.freq(1000)
        self.stop()

        # Time offset from reference (seconds)
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
        """Move fork UP (away from full extension) for t_s seconds."""
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
        """Move fork DOWN (towards full extension) for t_s seconds."""
        if t_s <= 0:
            return
        new_t = max(self.t_from_ref - t_s, 0.0)
        dt = self.t_from_ref - new_t
        if dt > 0:
            self.run(DIR_EXTEND, 100)
            sleep(dt)
            self.stop()
            self.t_from_ref = new_t

    def top_floor_pick_and_carry(self):
        """
        TOP FLOOR:
          - Start at full extension (~5 mm above ground).
          - Robot drives into block.     [external]
          - Raise actuator +21 mm to reach carry height.
          - Robot pulls back with block. [external]
        """
        self._nudge_up(LIFT_UP_TOP_TIME_S)

 
    def bottom_floor_pick_and_carry(self):
        """
        BOTTOM FLOOR:
          - Start at full extension.
          - Raise 19 mm to reach pickup height.
          - Robot drives forward into block.       [external]
          - Raise +4 mm to lift inside block.
          - Lower 2 mm to settle at carry height.
          - Robot pulls back with block.           [external]

        Net carry height = 19 + 4 - 2 = 21 mm above full extension.
        """
        self._nudge_up(BOTTOM_PRE_PICK_RAISE_S)
        # Robot drives forward externally
        self._nudge_up(LIFT_UP_BOTTOM_TIME_S)
        self._nudge_down(BOTTOM_LOWER_AFTER_PULL_S)


    def drop_off(self):
        """
        Drop-off for BOTH floors:
          - Start at unified carry height (~21 mm above full extension).
          - Robot drives to drop location.   [external]
          - Lower 16 mm so the block rests on the ground / surface.
          - Robot reverses to clear fork.    [external]
        """
        self._nudge_down(DROP_FROM_CARRY_TIME_S)

    def go_full_extension(self):
        self.home_full_extension()
        