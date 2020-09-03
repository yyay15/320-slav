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

#---------------#
# Definition
#---------------#
# # Custom Functions
# class _Getch:
#     """Gets a single character from standard input.  Does not echo to the
# screen."""
#     def __init__(self):
#         try:
#             self.impl = _GetchWindows()
#         except ImportError:
#             self.impl = _GetchUnix()

#     def __call__(self): return self.impl()

# class _GetchUnix:
#     def __init__(self):
#         import tty, sys

#     def __call__(self):
#         import sys, tty, termios
#         fd = sys.stdin.fileno()
#         old_settings = termios.tcgetattr(fd)
#         try:
#             tty.setraw(sys.stdin.fileno())
#             ch = sys.stdin.read(1)
#         finally:
#             termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
#         return ch

# class _GetchWindows:
#     def __init__(self):
#         import msvcrt

#     def __call__(self):
#         import msvcrt
#         return msvcrt.getch()

# getch = _Getch()




# GPIO.setmode(GPIO.BCM)				# Set the GPIO pin naming convention
# GPIO.setup(PWMB, GPIO.OUT)			# Set our GPIO pin to output
# GPIO.setup(PWMA, GPIO.OUT)			# Set our GPIO pin to output
# GPIO.setup(STBY, GPIO.OUT)			# Set our GPIO pin to output
# GPIO.setup(A1 , GPIO.OUT)			# Set our GPIO pin to output
# GPIO.setup(A2 , GPIO.OUT)			# Set our GPIO pin to output
# GPIO.setup(B1 , GPIO.OUT)			# Set our GPIO pin to output
# GPIO.setup(B2 , GPIO.OUT)			# Set our GPIO pin to output


# while(1):

#     key = getch() 

#     if key == 'w':
#         GPIO.output(A1,GPIO.HIGH) 		# Set GPIO pin 21 to digital high (on)
#         GPIO.output(B1,GPIO.HIGH) 		# Set GPIO pin 21 to digital high (on)
#         GPIO.output(A2,GPIO.LOW) 		# Set GPIO pin 21 to digital high (on)
#         GPIO.output(B2,GPIO.LOW) 		# Set GPIO pin 21 to digital high (on)
#         pwmA.ChangeDutyCycle(100)
#         pwmB.ChangeDutyCycle(100)
#         time.sleep(0.2)

#     elif key == 's':
#         GPIO.output(A1,GPIO.LOW) 		# Set GPIO pin 21 to digital high (on)
#         GPIO.output(B1,GPIO.LOW) 		# Set GPIO pin 21 to digital high (on)
#         GPIO.output(A2,GPIO.HIGH) 		# Set GPIO pin 21 to digital high (on)
#         GPIO.output(B2,GPIO.HIGH) 		# Set GPIO pin 21 to digital high (on)
#         pwmA.ChangeDutyCycle(100)
#         pwmB.ChangeDutyCycle(100)
#         time.sleep(0.2)


#     elif key == 'a':
#         GPIO.output(A1,GPIO.HIGH) 		# Set GPIO pin 21 to digital high (on)
#         GPIO.output(B1,GPIO.HIGH) 		# Set GPIO pin 21 to digital high (on)
#         GPIO.output(A2,GPIO.LOW) 		# Set GPIO pin 21 to digital high (on)
#         GPIO.output(B2,GPIO.LOW) 		# Set GPIO pin 21 to digital high (on)
#         pwmA.ChangeDutyCycle(0)
#         pwmB.ChangeDutyCycle(100)
#         time.sleep(0.2)

#     elif key == 'd':
#         GPIO.output(A1,GPIO.HIGH) 		# Set GPIO pin 21 to digital high (on)
#         GPIO.output(B1,GPIO.HIGH) 		# Set GPIO pin 21 to digital high (on)
#         GPIO.output(A2,GPIO.LOW) 		# Set GPIO pin 21 to digital high (on)
#         GPIO.output(B2,GPIO.LOW) 		# Set GPIO pin 21 to digital high (on)
#         pwmA.ChangeDutyCycle(100)
#         pwmB.ChangeDutyCycle(0)
#         time.sleep(0.2)


#     elif key == 'r':
#         GPIO.output(A1,GPIO.HIGH) 		# Set GPIO pin 21 to digital high (on)
#         GPIO.output(B1,GPIO.LOW) 		# Set GPIO pin 21 to digital high (on)
#         GPIO.output(A2,GPIO.LOW) 		# Set GPIO pin 21 to digital high (on)
#         GPIO.output(B2,GPIO.HIGH) 		# Set GPIO pin 21 to digital high (on)
#         pwmA.ChangeDutyCycle(100)
#         pwmB.ChangeDutyCycle(100)
#         time.sleep(1)


#     elif key == 'q':
#         print("quitting")
#         pwmA.stop()					# Stop the PWM signal
#         pwmB.stop()					# Stop the PWM signal
#         GPIO.output(A1,GPIO.LOW) 		# Set GPIO pin 21 to digital high (on)
#         GPIO.output(B1,GPIO.LOW) 		# Set GPIO pin 21 to digital high (on)
#         GPIO.output(A2,GPIO.LOW) 		# Set GPIO pin 21 to digital high (on)
#         GPIO.output(B2,GPIO.LOW) 		# Set GPIO pin 21 to digital high (on)
#         GPIO.cleanup()
#         break

#     else:
#         pwmA.ChangeDutyCycle(0)
#         pwmB.ChangeDutyCycle(0)

#     # Clean
#     char = ""
#     pwmA.ChangeDutyCycle(0)
#     pwmB.ChangeDutyCycle(0)




################################################################
# Custom Functions
###############################################################

# wip : OOP for mobility

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
        GPIO.output(B1,GPIO.HIGH) 		
        GPIO.output(A2,GPIO.LOW) 		
        GPIO.output(B2,GPIO.LOW) 		

        # Initialise PWM
        pwmA = GPIO.PWM(PWMA, 100)			# Initiate the PWM signal
        pwmA.start(0)					# Start a PWM signal with duty cycle at 50%
        pwmB = GPIO.PWM(PWMB, 100)			# Initiate the PWM signal
        pwmB.start(0)					# Start a PWM signal with duty cycle at 50%

        # Zero State
        self.drive(0, 0)


    def drive(self, velocity, angVelocity):

        # Convert v and w to motor percentages
        speedLeft, speedRight = self.veloCalcWheels(v, w)
        
        self.drivePower(speedLeft, speedRight)

    def veloCalcWheels(self, velocity, angVelocity):
                
		# Calculate linear velocity for each wheel
        veloLeft = velocity - angVelocity * WHEELBASE
        veloRight = 2 * velocity - veloLeft

		# Calculate angular velocity for each wheel
        angVeloLeft = veloLeft / WHEELRADIUS
        angVeloRight = veloRight / WHEELRADIUS

        # Convert to power value from 0 to 100
        powerLeft = angVeloLeft * POWER_TO_RADS
        powerRight = angVeloRight * POWER_TO_RADS

        return powerLeft, powerRight


    def manualControl(self):
        print("""
        Manual Control Mode:
        w     Move Forward
        s     Move Backward
        a     Turn Left
        d     Turn Right
        r     Rotate on spot
        c     Stop motors
        1,2,3 Preset speed 
        i     Custom Speed Setting
        q     Exit Mode\n""")
        while (True):            
            key = input() 
            if key == 'w':
                GPIO.output(A1,GPIO.HIGH) 		# Set GPIO pin 21 to digital high (on)
                GPIO.output(B1,GPIO.HIGH) 		# Set GPIO pin 21 to digital high (on)
                GPIO.output(A2,GPIO.LOW) 		# Set GPIO pin 21 to digital high (on)
                GPIO.output(B2,GPIO.LOW) 		# Set GPIO pin 21 to digital high (on)
                pwmA.ChangeDutyCycle(100)
                pwmB.ChangeDutyCycle(100)
            elif key == 's':
                GPIO.output(A1,GPIO.LOW) 		# Set GPIO pin 21 to digital high (on)
                GPIO.output(B1,GPIO.LOW) 		# Set GPIO pin 21 to digital high (on)
                GPIO.output(A2,GPIO.HIGH) 		# Set GPIO pin 21 to digital high (on)
                GPIO.output(B2,GPIO.HIGH) 		# Set GPIO pin 21 to digital high (on)
                pwmA.ChangeDutyCycle(100)
                pwmB.ChangeDutyCycle(100)
            elif key == 'a':
                GPIO.output(A1,GPIO.HIGH) 		# Set GPIO pin 21 to digital high (on)
                GPIO.output(B1,GPIO.HIGH) 		# Set GPIO pin 21 to digital high (on)
                GPIO.output(A2,GPIO.LOW) 		# Set GPIO pin 21 to digital high (on)
                GPIO.output(B2,GPIO.LOW) 		# Set GPIO pin 21 to digital high (on)
                pwmA.ChangeDutyCycle(0)
                pwmB.ChangeDutyCycle(100)
            elif key == 'd':
                GPIO.output(A1,GPIO.HIGH) 		# Set GPIO pin 21 to digital high (on)
                GPIO.output(B1,GPIO.HIGH) 		# Set GPIO pin 21 to digital high (on)
                GPIO.output(A2,GPIO.LOW) 		# Set GPIO pin 21 to digital high (on)
                GPIO.output(B2,GPIO.LOW) 		# Set GPIO pin 21 to digital high (on)
                pwmA.ChangeDutyCycle(100)
                pwmB.ChangeDutyCycle(0)
            elif key == 'r':
                GPIO.output(A1,GPIO.HIGH) 		# Set GPIO pin 21 to digital high (on)
                GPIO.output(B1,GPIO.LOW) 		# Set GPIO pin 21 to digital high (on)
                GPIO.output(A2,GPIO.LOW) 		# Set GPIO pin 21 to digital high (on)
                GPIO.output(B2,GPIO.HIGH) 		# Set GPIO pin 21 to digital high (on)
                pwmA.ChangeDutyCycle(100)
                pwmB.ChangeDutyCycle(100)
            elif key == 'q':
                print("Quitting ...")
                GPIO.cleanup()
                break
            else:
                print("Unknown Command")

    def gpioClean(self):
        self.drive(0, 0)
        GPIO.cleanup()
