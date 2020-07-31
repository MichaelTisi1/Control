""" Main class for top level control.  
"""
# Dependency
## Modules: ultrasonic, PIR, timer classes

# Status:   in progress.
# Last edit: Jordan Hong, 22:30 July 30, 2020 

class smartUV:
    # Declare constants 

    # State constants
    IDLE    = 0
    INITIAL = 1
    ACTIVE  = 2

    # GPIO (subject to change)
    ## Output
    GPIO_warning    = 31
    GPIO_lamp       = 37
    ## Input
    GPIO_PIR0       = 21
    GPIO_PIR1       = 23
    GPIO_PIR2       = 29

    GPIO_DIST0      = 33
    GPIO_DIST1      = 35
    GPIO_DIST2      = 32


    def __init__(self):

        # Initialize utility classes with respective GPIO pins
        self.distanceSensor = Ultrasonic(GPIO_DIST0, GPIO_DIST1, GPIO_DIST2)
        self.motionSensor   = PIR(GPIO_PIR0, GPIO_PIR1, GPIO_PIR2)
        self.timer          = Timer()

        # Declare parameters
        self.state = INITIAL    ## state variable
        self.dist = 0           ## distance in cm, measured from self.distanceSensor
        self.timeTheta = [320.25, -76.859, 444.6, -72.298]
        self.seeHuman = False   ## boolean to indicate whether human is detected

        # Timing parameters
        self.start_time = 0
        self.current_time = 0

    def main(self):
        """ Main function to loop through when system is not in IDLE state.
        """
        while (self.state != IDLE):

            ## Scans for moving object/human
            self.seeHuman = self.motionSensor.getReadings()
            if (self.seeHuman):
                self.state = IDLE
                break

            ## Case statements
            if (self.state==INITIAL):
                ## Initial state, get distance readings and use it calculate UV time parameter
                self.dist   = self.distanceSensor.getReadings()
                self.onTime = self.distance_to_On_time(self.dist, self.timeTheta)

            elif (self.state == ACTIVE):
                ## Checks timer
                ## Write to pin if needed (toggle lamp ON/OFF)
            else:
                ## Wrong state: outputs error (should not occur)
                pass
        return True

