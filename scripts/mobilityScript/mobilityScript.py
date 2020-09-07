#====================================#
# EGB320
# Mobility Script
# Group SLAVES: Group 13
# 2020 Semester 2
# Alan Yu
#====================================#


#---------------#
# Preamble
#---------------#
# Import Python Library for mobility
import RPi.GPIO as GPIO
import numpy as np
import time


#---------------#
# Variables
#---------------#
# Pin configurations
PWMA = 27
PWMB = 6
A1 = 10
A2 = 22
B1 = 11
B2 = 5
STBY = 9

# Wheel Parameters
WHEELRADIUS = 0.03 # Metres
WHEELBASE = 0.13    # Metres

# Motor Parameters
maxLin = 0.2
maxAng = 6.66
maxRPM = 63.66

# Speed Constant
LOWSPEED = 35
MEDIUMSPEED = 50
FULLSPEED = 100

# Global Speed

################################################################
# Custom Functions
###############################################################

class _Getch:
    """Gets a single character from standard input.  Does not echo to the
screen."""
    def __init__(self):
        try:
            self.impl = _GetchWindows()
        except ImportError:
            self.impl = _GetchUnix()

    def __call__(self): return self.impl()

class _GetchUnix:
    def __init__(self):
        import tty, sys

    def __call__(self):
        import sys, tty, termios
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch

class _GetchWindows:
    def __init__(self):
        import msvcrt

    def __call__(self):
        import msvcrt
        return msvcrt.getch()

getch = _Getch()


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
        GPIO.setmode(GPIO.BCM)				# Set the GPIO pin naming convention
        GPIO.setup(PWMB, GPIO.OUT)			# Set our GPIO pin to output
        GPIO.setup(PWMA, GPIO.OUT)			# Set our GPIO pin to output
        GPIO.setup(STBY, GPIO.OUT)			# Set our GPIO pin to output
        GPIO.setup(A1 , GPIO.OUT)			# Set our GPIO pin to output
        GPIO.setup(A2 , GPIO.OUT)			# Set our GPIO pin to output
        GPIO.setup(B1 , GPIO.OUT)			# Set our GPIO pin to output
        GPIO.setup(B2 , GPIO.OUT)			# Set our GPIO pin to output
        # Set up GPIO Output 
        GPIO.output(STBY,GPIO.HIGH)
        GPIO.output(A1,GPIO.HIGH)
        GPIO.output(A2,GPIO.LOW)
        GPIO.output(B1,GPIO.HIGH)
        GPIO.output(B2,GPIO.LOW) 		
        # Initialise PWM
        self.motorPWM = [GPIO.PWM(PWMA, 100),GPIO.PWM(PWMB, 100)]
        # Initialise MotorDir
        self.motorDIR = [A1,A2,B1,B2]
        self.speedLeft  = MEDIUMSPEED
        self.speedRight = MEDIUMSPEED
        # Zero State
        self.drive(0, 0)


    def drive(self, v, w):
        # Threshold Velocity to max
        v = min(v, maxLin)
        w = min(w, maxAng)

        # Convert v and w to motor percentages
        self.speedLeft, self.speedRight = self.veloCalcWheels(v, w)
        
        self.drivePower(self.speedLeft, self.speedRight)

    def veloCalcWheels(self, v, w):

		# Calculate linear velocity for each wheel
        veloLeft = (v - 0.5 * w * WHEELBASE) 
        veloRight = (v + 0.5 * w * WHEELBASE)

		# Calculate angular velocity for each wheel
        angVeloLeft = veloLeft / WHEELRADIUS
        angVeloRight = veloRight / WHEELRADIUS
                
        # Convert to power value from 0 to 100
        powerLeft = angVeloLeft / maxAng * 100
        powerRight = angVeloRight / maxAng * 100 

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


    def drivePower(self, powerLeft, powerRight):
        """  Set PWM to drive the motors """
        # Set Drive Direction
        self.driveDir(powerLeft, powerRight)
        # Print
        print(powerLeft)
        print(powerRight)
        # Turn motors
        self.motorPWM[0].start(abs(powerLeft))
        self.motorPWM[1].start(abs(powerRight))


    def manualControl(self):
        print("""
        Manual Control Mode:
        This control mode allows the user to press a button and enter it whilst the action will run indefintely.
        w     Move Forward
        s     Move Backward
        a     Turn Left
        d     Turn Right
        r     Rotate on spot
        c     Stop motors
        i     Custom Speed Setting (v,w)
        j     Custom Speed Setting (l,r)
        1     Low Speed Setting (35% PWM)
        2     Medium Speed Setting (50% PWM)
        3     Full Speed Setting (100% PWM)
        q     Exit Mode\n""")
        while (True):            
            key = input(">> ") 
            if key == 'w':
                print("Moving Forwards")
                self.drivePower(self.speedLeft, self.speedRight)
            elif key == 's':
                print("Moving Backwards")
                self.drivePower(-self.speedLeft, -self.speedRight)
            elif key == 'a':
                print("Turning Left")
                self.drivePower(0, self.speedRight)
            elif key == 'd':
                print("Turning Right")
                self.drivePower(self.speedLeft, 0)
            elif key == 'r':
                print("Rotating")
                self.drivePower(-self.speedLeft, self.speedRight)
            elif key == 'c':
                print("Stopping Motors")
                self.drivePower(0, 0)
            elif key == 'i':
                self.drivePower(0, 0)
                print("Input speed in format 'velocity,angularVelocity': ", end='')
                speedInput = input()
                # Split commas
                speedInput = speedInput.split(',')
                if len(speedInput) != 2:
                    print("Error: Incorrect Input")
                    continue            
                # Parse numbers
                try:
                    self.speedLeft, self.speedRight = self.veloCalcWheels(float(speedInput[0]), float(speedInput[1]))
                    print("--------\n")
                    print(self.speedLeft)
                    print(self.speedRight)
                    print("--------\n")
                except ValueError:
                    print("Error: Incorrect Input")
                    continue
            elif key == 'j':
                self.drivePower(0, 0)
                print("Input speed in format 'leftPower,rightPower': ", end='')
                speedInput = input()
                # Split commas
                speedInput = speedInput.split(',')
                if len(speedInput) != 2:
                    print("Error: Incorrect Input")
                    continue            
                # Parse numbers
                try:
                    self.speedLeft = int(speedInput[0])
                    self.speedRight = int(speedInput[1])
                except ValueError:
                    print("Error: Incorrect Input")
                    continue
            elif key == '1':
                print("Setting LowSpeed")
                print(LOWSPEED)
                self.speedLeft = LOWSPEED
                self.speedRight = LOWSPEED
            elif key == '2':
                print("Setting MediumSpeed")
                print(MEDIUMSPEED)
                self.speedLeft = MEDIUMSPEED
                self.speedRight = MEDIUMSPEED
            elif key == '3':
                print("Setting FullSpeed")
                print(FULLSPEED)
                self.speedLeft = FULLSPEED
                self.speedRight = FULLSPEED
            elif key == 'q':
                print("Quitting ...")
                GPIO.cleanup()
                break
            else:
                print("Unknown Command")


    def continuousControl(self):
        print("""
        Continuous Control Mode:
        This control system allows user to press and hold to fine tune control.
        w     Move Forward
        s     Move Backward
        a     Turn Left
        d     Turn Right
        r     Rotate on spot
        c     Stop motors
        i     Custom Speed Setting (v,w)
        j     Custom Speed Setting (l,r)
        1     Low Speed Setting (35% PWM)
        2     Medium Speed Setting (50% PWM)
        3     Full Speed Setting (100% PWM)
        q     Exit Mode\n""")
        while (True):            
            key = getch() 
            if key == 'w':
                self.drivePower(self.speedLeft, self.speedRight)
                time.sleep(0.2)
            elif key == 's':
                self.drivePower(-self.speedLeft, -self.speedRight)
                time.sleep(0.2)
            elif key == 'a':
                self.drivePower(0, self.speedRight)
                time.sleep(0.2)
            elif key == 'd':
                self.drivePower(self.speedLeft, 0)
                time.sleep(0.2)
            elif key == 'r':
                self.drivePower(-self.speedLeft, self.speedRight)
                time.sleep(0.2)
            elif key == 'c':
                self.drivePower(0, 0)
                time.sleep(0.2)
            elif key == 'i':
                self.drivePower(0, 0)
                print("Input speed in format 'velocity,angularVelocity': ", end='')
                speedInput = input()
                # Split commas
                speedInput = speedInput.split(',')
                if len(speedInput) != 2:
                    print("Error: Incorrect Input")
                    continue            
                # Parse numbers
                try:
                    self.speedLeft, self.speedRight = self.veloCalcWheels(float(speedInput[0]), float(speedInput[1]))
                except ValueError:
                    print("Error: Incorrect Input")
                    continue
            elif key == 'j':
                self.drivePower(0, 0)
                print("Input speed in format 'leftPower,rightPower': ", end='')
                speedInput = input()
                # Split commas
                speedInput = speedInput.split(',')
                if len(speedInput) != 2:
                    print("Error: Incorrect Input")
                    continue            
                # Parse numbers
                try:
                    self.speedLeft = int(speedInput[0])
                    self.speedRight = int(speedInput[1])
                except ValueError:
                    print("Error: Incorrect Input")
                    continue
            elif key == '1':
                print("Setting LowSpeed")
                print(LOWSPEED)
                self.speedLeft = LOWSPEED
                self.speedRight = LOWSPEED
                time.sleep(0.2)
            elif key == '2':
                print("Setting MediumSpeed")
                print(MEDIUMSPEED)
                self.speedLeft = MEDIUMSPEED
                self.speedRight = MEDIUMSPEED
                time.sleep(0.2)
            elif key == '3':
                print("Setting FullSpeed")
                print(FULLSPEED)
                self.speedLeft = FULLSPEED
                self.speedRight = FULLSPEED
                time.sleep(0.2)
            elif key == 'q':
                print("Quitting ...")
                GPIO.cleanup()
                break
            else:
                self.drivePower(0, 0)



    def commandCentreTest(self,command):
        if (len(command.split(','))>2):
            controlVar1 = command.split(',')[1]
            controlVar2 = command.split(',')[2]
            command = command.split(',')[0]

        if command == 'w':
            print("Im HERE")
            print(self.speedLeft)
            print(self.speedRight)
            print("Im HERE")
            self.drivePower(self.speedLeft, self.speedRight)
        elif command == 's':
            self.drivePower(-self.speedLeft, -self.speedRight)
        elif command == 'a':
            self.drivePower(0, self.speedRight)
        elif command == 'd':
            self.drivePower(self.speedLeft, 0)
        elif command == 'r':
            self.drivePower(-self.speedLeft, self.speedRight)
        elif command == 'c':
            self.drivePower(0, 0)
        elif command == 'i':
            self.drivePower(0, 0)
            self.speedLeft, self.speedRight = self.veloCalcWheels(float(controlVar1), float(controlVar2))
        elif command == 'j':
            self.drivePower(0, 0)
            self.speedLeft = int(controlVar1)
            self.speedRight = int(controlVar2)
        elif command == '1':
            print("Setting LowSpeed")
            print(LOWSPEED)
            self.speedLeft = LOWSPEED
            self.speedRight = LOWSPEED
        elif command == '2':
            print("Setting MediumSpeed")
            print(MEDIUMSPEED)
            self.speedLeft = MEDIUMSPEED
            self.speedRight = MEDIUMSPEED
        elif command == '3':
            print("Setting FullSpeed")
            print(FULLSPEED)
            self.speedLeft = FULLSPEED
            self.speedRight = FULLSPEED
        elif command == 'q':
            print("Quitting ...")
            GPIO.cleanup()
        else:
            self.drivePower(0, 0)



    def gpioClean(self):
        self.drive(0, 0)
        GPIO.cleanup()
