from machine import Pin, PWM
from utime import sleep

FullStrokeTime = 8.02
FullStrokeDist = 50.0   

defaultHeight = 10.0
CarryHeight = 21.0
BottomFloorPickupHeight = 22.0
TopFloorPickupHeight = 4.0
"""
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
"""
def distToTime(dist):
    return FullStrokeTime * (dist / FullStrokeDist)

def timeToDist(time):
    return FullStrokeDist * (time / FullStrokeTime)

DirExtend  = 0   # towards full extension 
DirRetract = 1   # away from full extension


class Actuator:
    def __init__(self, dirPin, PWMPin):
        self.mDir = Pin(dirPin, Pin.OUT)
        self.pwm = PWM(Pin(PWMPin))
        self.pwm.freq(1000)
        self.stop()
        
        self.fullExtension()
        self.currentHeight = 0.0

    def run(self, direction, speed_percent):
        self.mDir.value(direction)
        duty = int(65535 * speed_percent / 100)
        self.pwm.duty_u16(duty)

    def stop(self):
        self.pwm.duty_u16(0)

    def fullExtension(self):
        self.run(DirExtend, 60)
        sleep(FullStrokeTime)
        self.stop()
        self.currentHeight = 0.0
        print("Fully Extended")
        
    def fullRetraction(self):
        self.run(DirRetract, 60)
        sleep(FullStrokeTime)
        self.stop()
        self.currentHeight = FullStrokeDist
        print("Fully Retracted")
    
    def moveUp(self, dist):
        time = distToTime(dist)
        self.run(DirRetract, 60)
        sleep(time)
        self.stop()
    
    def moveDown(self, dist):
        time = distToTime(dist)
        self.run(DirExtend, 60)
        sleep(time)
        self.stop()
    
    def setHeight(self, height):
        if height < 0:
            height = 0
        elif height > FullStrokeDist:
            height = FullStrokeDist
            
        dist = height - self.currentHeight
        if dist > 0:
            self.moveUp(dist)
        else:
            self.moveDown(dist)
        self.currentHeight = height


    def topFloorPickUp(self):
        self.setHeight(TopFloorPickupHeight)
        
    def bottomFloorPickUp(self):
        self.setHeight(BottomFloorPickupHeight)
    
    def defaultHeight(self):
        self.setHeight(defaultHeight)

    def pickUp(self):
        self.moveUp(4.0)
    
    def carry(self):
        if self.currentHeight != CarryHeight:
            self.setHeight(CarryHeight)

    def dropOff(self):
        self.fullExtension()


def main():
    actuator = Actuator(dirPin=0, PWMPin=1)

    # Home at startup
    actuator.fullExtension()


    actuator.topFloorPickUp()
    print("TOP")
    sleep(0.5)
    actuator.pickUp()
    print("PICK")
    sleep(1)
    
    actuator.dropOff()
    print("DROP")
    sleep(1)

    actuator.bottomFloorPickUp()
    print("BOT")
    sleep(0.5)
    actuator.pickUp()
    print("PICK")
    print("End")


if __name__ == "__main__":
    main()
