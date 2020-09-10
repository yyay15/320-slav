import RPi.GPIO as GPIO
import time

servoPin = 17

def SetAngle(angle):
    duty = angle / 18 + 2
    GPIO.output(servoPin, True)
    pwm.ChangeDutyCycle(duty)
    sleep(1)
    GPIO.output(servoPin, False)
    pwm.ChangeDutyCycle(0)


def sample_uncovered():  # Start sample_retrival 110mm away
    SetAngle(90)
    sleep(5)
    SetAngle(0)


#def sample_covered()    # 
    



