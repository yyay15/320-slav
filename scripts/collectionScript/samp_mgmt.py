
import RPi.GPIO as GPIO
import time

servoPin = 17
GPIO.setmode(GPIO.BCM)
GPIO.setup(servoPin, GPIO.OUT)

#GPIO.output
pwm = GPIO.PWM(servoPin, 50)
pwm.start(2.5)

def SetAngle(angle):
    duty = angle / 18 + 1
    GPIO.output(servoPin, True)
    pwm.ChangeDutyCycle(duty)
    time.sleep(1)
    GPIO.output(servoPin, False)
    pwm.ChangeDutyCycle(0)


def sample_uncovered():  # Start sample_retrival 110mm away
    SetAngle(90)
    time.sleep(2)
    SetAngle(0)

def sample_covered():  # Start sample_retrival 110mm away
    SetAngle(0)
    time.sleep(2)
    SetAngle(90)

while True:
    sample_uncovered()
    sample_covered()

#def sample_covered()    # 
    



#sample_uncovered()
