#====================================#
# EGB320
# Main Script
# Group SLAVES: Group 13
# 2020 Semester 2
# Alan Yu
# 
#====================================#


#---------------#
# Preamble
#---------------#
# Import Python Library for main
import sys, time
import RPi.GPIO as GPIO

# Import Python Library for CommandCentre
from flask import Flask
from flask import render_template, request
app = Flask(__name__, template_folder='commandCentre')

# Set Global Parameters 
LED_GREEN = 0
LED_RED = 1
LED_YELLOW = 2
global command

# Local modules
from mobilityScript import mobilityScript
from navigationScript.VREP_PythonCode import navigation, state
from visionScript import vision
# from collectionScript import

#---------------#
# Function definitions
#---------------#

def ledIndicator(state):
    if (state == 1):
        GPIO.output(LED_RED, HIGH)
        GPIO.output(LED_YELLOW, LOW)
        GPIO.output(LED_GREEN, LOW)
    elif (state == 3 or state == 7):
        GPIO.output(LED_YELLOW, HIGH)
        GPIO.output(LED_GREEN, LOW)
        GPIO.output(LED_RED, LOW)
    elif (state == 5 or state == 6):
        GPIO.output(LED_GREEN, HIGH)
        GPIO.output(LED_RED, LOW)
        GPIO.output(LED_YELLOW, LOW)
    else:
        GPIO.output(LED_RED, LOW)
        GPIO.output(LED_YELLOW, LOW)
        GPIO.output(LED_GREEN, LOW)

def ledSetup():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(LED_GREEN, GPIO.OUT)
    GPIO.setup(LED_YELLOW, GPIO.OUT)
    GPIO.setup(LED_RED, GPIO.OUT) 



#---------------#
# Flask Function
#---------------#

@app.route("/")
def index():
    print("Our websever has launched!")
    return render_template('commandCentre.html')


# Use MobilityScript Method to set command
@app.route('/mobility/<command>')
def mobilityControl(command):
    print("================")
    print(command)
    print("================")
    drive.commandCentreTest(command)
    return '{}'

@app.route('/setSpeed/')
def set_speed(speed):
    ser.write('2,' + speed)
    return '{}'


#---------------#
# Initialise
#---------------#

# Initialise Functions and Classes
# Subsystem
drive = mobilityScript.Mobility()
#vision = vision.Vision()
# nav
nav = navigation.Navigation() 
state = state.State()
ledSetup() #nav

#---------------#
# MainScript
#---------------#
print("beforemain")
if __name__ == '__main__':
    # Initialise States for All System
    v = 0
    w = 0

    # Try Loading And running
    try:
        print("beforeWhile...")

        while(1):
            print("""
            Please select Drive Mode
            a    Automatic
            m    Manual - Discrete (Enter Button)
            n    Manual - Continuous (Hold button)
            c    CommandCentre (TESTING)
            q    quit
            """)
            userSelect = input()
            if  userSelect == "a":
                # CHUCK THAT CHUNK HERE
                while True:
                    vision.UpdateObjectPositions()
                    objects = vision.GetDetectedObjects()
                    #sampleCollected = vision.SampleCollected()
                    state.updateState(objects, True)
                    v, w = nav.updateVelocities(state)
                    drive.drive(v, w) # not in navMain
                    print(state.sampleRB)
                
            elif userSelect == "m":
                drive.manualControl()
            elif userSelect == "n":
                drive.continuousControl()
            elif userSelect == "c":
                print("Starting Command Centre ...")
                app.run(host='0.0.0.0',port=6969,debug=False)
            elif userSelect == "q":
                drive.gpioClean()
                break
            else:
                print("Unknown Command")
    # Clean up when closing        
    except KeyboardInterrupt:
        drive.gpioClean()
        print("CleanergoVRMMM...")


