#====================================#
# EGB320
# Collection Script
# Group SLAVES: Group 13
# 2020 Semester 2
# Alan Yu
#====================================#


#---------------#
# Preamble
#---------------#
# Import Python Library for collection
import RPi.GPIO as GPIO
import time

#---------------#
# Variables
#---------------#
# Pin configurations
servoPin = 17


################################################################
# Define Class System
###############################################################
class Mobility:

    
    def __init__(self):
        """
        This initialises the mobility class. It will set relevant GPIO Pins on
        and also enables HBridge for forward/backward control.
        The function will end when we set the drive to 0.
        """
        # Set up GPIO Pins
        GPIO.setmode(GPIO.BCM)				
        GPIO.setup(servoPin, GPIO.OUT)			
        # Initialise PWM
        self.servoPWM = GPIO.PWM(servoPin, 50)

        self.
        # Initialise MotorDir
        self.motorDIR = [A1,A2,B1,B2]
        self.speedLeft  = MEDIUMSPEED
        self.speedRight = MEDIUMSPEED
        # Zero State
        self.drive(0, 0)


    def drive(self, v, w):
        # Threshold Velocity to max
        v = min(v, maxLin)
        w = min(w, maxAngBase)

        # Convert v and w to motor percentages
        self.speedLeft, self.speedRight = self.SetTargetVelocities(v, w)
        
        self.drivePower(self.speedLeft, self.speedRight)

    def SetTargetVelocities(self, v, w):

		# Calculate linear velocity for each wheel
        veloLeft = (v - 0.5 * w * WHEELBASE) 
        veloRight = (v + 0.5 * w * WHEELBASE)

		# Calculate angular velocity for each wheel
        angVeloLeft = veloLeft / WHEELRADIUS
        angVeloRight = veloRight / WHEELRADIUS
                
        # Convert to power value from 0 to 100
        powerLeft = angVeloLeft / maxAngWheel * 100
        powerRight = angVeloRight / maxAngWheel * 100 

        # Threshold for rounding and max power
        powerLeft = min(powerLeft, 100)
        powerRight = min(powerRight, 100)
        powerLeft = max(powerLeft, -100)
        powerRight = max(powerRight, -100)

        return powerLeft, powerRight

    def driveDir(self, powerLeft, powerRight):
        if powerLeft < 0:
            GPIO.output(self.motorDIR[0],GPIO.LOW) 	
            GPIO.output(self.motorDIR[1],GPIO.HIGH) 	
        else:
            GPIO.output(self.motorDIR[0],GPIO.HIGH) 	
            GPIO.output(self.motorDIR[1],GPIO.LOW) 	
            
        if powerRight < 0:
            GPIO.output(self.motorDIR[2],GPIO.LOW) 	
            GPIO.output(self.motorDIR[3],GPIO.HIGH) 	
        else:
            GPIO.output(self.motorDIR[2],GPIO.HIGH) 	
            GPIO.output(self.motorDIR[3],GPIO.LOW) 	

