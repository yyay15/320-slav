import RPi.GPIO as GPIO
import time

servoPin = 15

def SetAngle(angle):
    duty = angle / 18 + 2
    GPIO.output(servoPin, True)
    pwm.ChangeDutyCycle(duty)
    sleep(1)
    GPIO.output(servoPin, False)
    pwm.ChangeDutyCycle(0)



if sample_uncovered:
    if dis2samp = 100:

