# Import Library
import RPi.GPIO as GPIO
import numpy as np
import time


# Custom Functions
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


# Pin configurations
PWMA = 5
PWMB = 21
A1 = 13
A2 = 6
B1 = 20
B2 = 26
STBY = 19

GPIO.setmode(GPIO.BCM)				# Set the GPIO pin naming convention
GPIO.setup(PWMB, GPIO.OUT)			# Set our GPIO pin to output
GPIO.setup(PWMA, GPIO.OUT)			# Set our GPIO pin to output
GPIO.setup(STBY, GPIO.OUT)			# Set our GPIO pin to output
GPIO.setup(A1 , GPIO.OUT)			# Set our GPIO pin to output
GPIO.setup(A2 , GPIO.OUT)			# Set our GPIO pin to output
GPIO.setup(B1 , GPIO.OUT)			# Set our GPIO pin to output
GPIO.setup(B2 , GPIO.OUT)			# Set our GPIO pin to output



GPIO.output(STBY,GPIO.HIGH)
GPIO.output(A1,GPIO.HIGH) 		# Set GPIO pin 21 to digital high (on)
GPIO.output(B1,GPIO.HIGH) 		# Set GPIO pin 21 to digital high (on)
GPIO.output(A2,GPIO.LOW) 		# Set GPIO pin 21 to digital high (on)
GPIO.output(B2,GPIO.LOW) 		# Set GPIO pin 21 to digital high (on)

pwmA = GPIO.PWM(PWMA, 100)			# Initiate the PWM signal
pwmA.start(0)					# Start a PWM signal with duty cycle at 50%
pwmB = GPIO.PWM(PWMB, 100)			# Initiate the PWM signal
pwmB.start(0)					# Start a PWM signal with duty cycle at 50%




while(1):

    key = getch() 

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
    
    elif key == 'q':
        print("quitting")
        pwmA.stop()					# Stop the PWM signal
        pwmB.stop()					# Stop the PWM signal
        GPIO.output(A1,GPIO.LOW) 		# Set GPIO pin 21 to digital high (on)
        GPIO.output(B1,GPIO.LOW) 		# Set GPIO pin 21 to digital high (on)
        GPIO.output(A2,GPIO.LOW) 		# Set GPIO pin 21 to digital high (on)
        GPIO.output(B2,GPIO.LOW) 		# Set GPIO pin 21 to digital high (on)
        GPIO.cleanup()
        break

    else:
        pwmA.ChangeDutyCycle(0)
        pwmB.ChangeDutyCycle(0)

    # Clean
    char = ""
    pwmA.ChangeDutyCycle(0)
    pwmB.ChangeDutyCycle(0)


    
    # for dc in range (0, 101, 10):
    #     pwmA.ChangeDutyCycle(dc)
    #     pwmB.ChangeDutyCycle(dc)
    #     time.sleep(0.5)
 

# pwmA.stop()					# Stop the PWM signal
# pwmB.stop()					# Stop the PWM signal

# GPIO.output(A1,GPIO.LOW) 		# Set GPIO pin 21 to digital high (on)
# GPIO.output(B1,GPIO.LOW) 		# Set GPIO pin 21 to digital high (on)

# GPIO.cleanup()

################################################################
# Custom Functions
###############################################################

# wip : OOP for mobility

class Mobility:

    def __init__(self):
        # Set up GPIO Pins
        GPIO.setmode(GPIO.BCM)				# Set the GPIO pin naming convention
        GPIO.setup(PWMB, GPIO.OUT)			# Set our GPIO pin to output
        GPIO.setup(PWMA, GPIO.OUT)			# Set our GPIO pin to output
        GPIO.setup(STBY, GPIO.OUT)			# Set our GPIO pin to output
        GPIO.setup(A1 , GPIO.OUT)			# Set our GPIO pin to output
        GPIO.setup(A2 , GPIO.OUT)			# Set our GPIO pin to output
        GPIO.setup(B1 , GPIO.OUT)			# Set our GPIO pin to output
        GPIO.setup(B2 , GPIO.OUT)			# Set our GPIO pin to output


    def gpioClean(self):
        GPIO.cleanup()








###############################################################
# Reference
###############################################################

# # MOTOR_PINS = np.array([[19, 16], [26, 20]])


# # Drive parameters
# WHEEL_RADIUS = 0.042   # metres
# WHEEL_BASE = 0.1       # metres
# POWER_TO_RADS = 40     # motor percent per rad/s

# # Right motor scaling function parameters
# # POWER_R_SCALED = POWER_R * SCALING_M + SCALING_C
# SCALING_M = 0.75
# SCALING_C = 25

# class Drive:

#     def __init__(self):

#         # Setup GPIO
#         GPIO.setmode(GPIO.BCM)
#         for pin in np.concatenate([MOTOR_PINS.flatten(), [KICKER_PIN], DRIBBLER_PINS]):
#             GPIO.setup(int(pin), GPIO.OUT)

#         # Setup PWM
#         self.motorPWM = [[GPIO.PWM(MOTOR_PINS[0,0], 100), GPIO.PWM(MOTOR_PINS[0,1], 100)],
#                          [GPIO.PWM(MOTOR_PINS[1,0], 100), GPIO.PWM(MOTOR_PINS[1,1], 100)]]

#         # Turn everything off
#         self.drive(0, 0)

#     def turnMotor(self, pwms, speed):
#         #print(speed)
#         # Constrain speed to 100 and -100
#         if speed > 100:  speed = 100
#         if speed < -100: speed = -100

#         # Forward
#         if speed >= 0:
#             pwms[0].start(speed)
#             pwms[1].stop()
        
#         # Backwards
#         else:
#             pwms[0].stop()
#             pwms[1].start(-speed)
	
#     def drive(self, v, w):

#         # Convert v and w to motor percentages
#         speed_l, speed_r = self.vw2wheels(v, w)
#         #speed_l *= MULTIPLIER_L
#         #speed_r *= MULTIPLIER_R
        
#         # Apply scaling to right motor
#         speed_r = speed_r * SCALING_M + SCALING_C

#         self.drivePower(speed_l, speed_r)

#     def drivePower(self, power_l, power_r):
#         """ Drive speeds from -100 to 100 """

#         # Turn motors
#         self.turnMotor(self.motorPWM[0], power_l)
#         self.turnMotor(self.motorPWM[1], power_r)

#     def vw2wheels(self, v, w):
        
# 		# Calculate linear velocity for each wheel
#         v_l = v - w * WHEEL_BASE
#         v_r = 2 * v - v_l

# 		# Calculate angular velocity for each wheel
#         w_l = v_l / WHEEL_RADIUS
#         w_r = v_r / WHEEL_RADIUS

#         # Convert to power value from 0 to 100
#         power_l = w_l * POWER_TO_RADS
#         power_r = w_r * POWER_TO_RADS

#         return power_l, power_r


#     def cleanup(self):
#         GPIO.cleanup()
