
import RPi.GPIO as GPIO
import time

servoPin = 17
GPIO.setmode(GPIO.BCM)
GPIO.setup(servoPIN, GPIO.OUT)

pwm = GPIO.PWM(servoPIN, 50) # GPIO 17 for PWM with 50Hz
pwm.start(3) # Initialization


def Open_ROT():
    pwm.ChangeDutyCycle(7.5)
    pwm.ChangeDutyCycle(0)
    print("Open")
    time.sleep(1)

def Close_ROT():
    pwm.ChangeDutyCycle(3.5)    
    pwm.ChangeDutyCycle(0)
    print("Close")
    time.sleep(1)

def Release_Ball():
    pwm.ChangeDutyCycle(5)
    pwm.ChangeDutyCycle(0)
    print("Releasing Ball")
    time.sleep(1)

def sample_uncovered():  # Start sample_retrival 110mm away
    SetAngle(90)
    time.sleep(2)
    SetAngle(0)

def sample_covered():  # Start sample_retrival 110mm away
    SetAngle(0)
    time.sleep(2)
    SetAngle(90)

# def sample_uncovered():  # Start sample_retrival 110mm away
#     print("Sample Uncovered")
#     Open_ROT
#     print("Open")
#     time.sleep(1)
#     pwm.ChangeDutyCycle(4)
#     print("Closed")
#     time.sleep(3)

# def sample_covered():  # Start sample_retrival 110mm away
#     print("Sampled Covered")
#     pwm.ChangeDutyCycle(4)
#     print("Open")
#     time.sleep(1)
#     pwm.ChangeDutyCycle(7.5)
#     print("Closed")
#     time.sleep(1)
#     pwm.ChangeDutyCycle(4)
#     print("Open")
#     time.sleep(1)


# def sample_release():
#     print("Sample Release")
#     pwm.ChangeDutyCycle(3.5)
#     print("Open")
#     time.sleep(2)
#     pwm.ChangeDutyCycle(7.5)
#     print("Closed")
#     time.sleep(6)
#     pwm.ChangeDutyCycle(3.5)   

# def sample_reset():
#     print("Sample Reset")
#     pwm.ChangeDutyCycle(0.0)
#     print("clean")
#     time.sleep(2)
    
# try:
#   while True:
#     sample_reset()
#     time.sleep(2)
#     sample_covered()
#     time.sleep(2)
#     sample_reset()
#     time.sleep(5)
#     sample_uncovered()
# except KeyboardInterrupt:
#     pwm.stop()
#     GPIO.cleanup()
#     print("clean")
    

