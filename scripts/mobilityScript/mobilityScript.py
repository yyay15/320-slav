import RPi.GPIO as GPIO
import numpy as np
import time

# Pin configurations
MOTOR_PINS = np.array([[19, 16], [26, 20]])

# Drive parameters
WHEEL_RADIUS = 0.042   # metres
WHEEL_BASE = 0.1       # metres
POWER_TO_RADS = 40     # motor percent per rad/s
#MULTIPLIER_L = 0.8
#MULTIPLIER_R = 1

# Right motor scaling function parameters
# POWER_R_SCALED = POWER_R * SCALING_M + SCALING_C
SCALING_M = 0.75
SCALING_C = 25

class Drive:

    def __init__(self):

        # Setup GPIO
        GPIO.setmode(GPIO.BCM)
        for pin in np.concatenate([MOTOR_PINS.flatten(), [KICKER_PIN], DRIBBLER_PINS]):
            GPIO.setup(int(pin), GPIO.OUT)

        # Setup PWM
        self.motorPWM = [[GPIO.PWM(MOTOR_PINS[0,0], 100), GPIO.PWM(MOTOR_PINS[0,1], 100)],
                         [GPIO.PWM(MOTOR_PINS[1,0], 100), GPIO.PWM(MOTOR_PINS[1,1], 100)]]

        # Turn everything off
        self.drive(0, 0)

    def turnMotor(self, pwms, speed):
        #print(speed)
        # Constrain speed to 100 and -100
        if speed > 100:  speed = 100
        if speed < -100: speed = -100

        # Forward
        if speed >= 0:
            pwms[0].start(speed)
            pwms[1].stop()
        
        # Backwards
        else:
            pwms[0].stop()
            pwms[1].start(-speed)
	
    def drive(self, v, w):

        # Convert v and w to motor percentages
        speed_l, speed_r = self.vw2wheels(v, w)
        #speed_l *= MULTIPLIER_L
        #speed_r *= MULTIPLIER_R
        
        # Apply scaling to right motor
        speed_r = speed_r * SCALING_M + SCALING_C

        self.drivePower(speed_l, speed_r)

    def drivePower(self, power_l, power_r):
        """ Drive speeds from -100 to 100 """

        # Turn motors
        self.turnMotor(self.motorPWM[0], power_l)
        self.turnMotor(self.motorPWM[1], power_r)

    def vw2wheels(self, v, w):
        
		# Calculate linear velocity for each wheel
        v_l = v - w * WHEEL_BASE
        v_r = 2 * v - v_l

		# Calculate angular velocity for each wheel
        w_l = v_l / WHEEL_RADIUS
        w_r = v_r / WHEEL_RADIUS

        # Convert to power value from 0 to 100
        power_l = w_l * POWER_TO_RADS
        power_r = w_r * POWER_TO_RADS

        return power_l, power_r


    def cleanup(self):
        GPIO.cleanup()
