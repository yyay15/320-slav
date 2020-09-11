import RPi.GPIO as GPIO
import time


servoPin = 17
GPIO.setmode(GPIO.BCM)
GPIO.setup(servoPin, GPIO.OUT)

#GPIO.output
pwm = GPIO.PWM(servoPin, 100)

#def SetAngle(angle):
  #  duty = angle / 18 + 2
   # GPIO.output(servoPin, True)
  #  pwm.ChangeDutyCycle(duty)
 #   GPIO.output(servoPin, False)
 #   pwm.ChangeDutyCycle(0)


def sample_uncovered():  # Start sample_retrival 110mm away
    pwm.ChangeDutyCycle(12.5)
    time.sleep(5)
    pwm.ChangeDutyCycle(0)

def sample_covered():  # Start sample_retrival 110mm away
    pwm.ChangeDutyCycle(0)
    time.sleep(3)
    pwm.ChangeDutyCycle(12.5)

while True:
    sample_uncovered()
    sample_covered()

#def sample_covered()    # 
    



#sample_uncovered()
