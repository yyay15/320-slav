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
from flask import Response
app = Flask(__name__, template_folder='commandCentre')

import cv2

# Set Global Parameters 
LED_GREEN = 26
LED_RED = 13
LED_YELLOW = 19
global command


# Local modules
from mobilityScript import mobilityScript
from navigationScript.VREP_PythonCode import navigation, state, localisation
from visionScript import vision3
from collectionScript import collection

#---------------#
# Function definitions
#---------------#

def ledIndicator(state):
    if (state == 1):
        GPIO.output(LED_RED, GPIO.HIGH)
        GPIO.output(LED_YELLOW, GPIO.LOW)
        GPIO.output(LED_GREEN, GPIO.LOW)
    elif (state == 3 or state == 7):
        GPIO.output(LED_YELLOW, GPIO.HIGH)
        GPIO.output(LED_GREEN, GPIO.LOW)
        GPIO.output(LED_RED, GPIO.LOW)
    elif (state == 5 or state == 6 or state == 8 or state == 11):
        GPIO.output(LED_GREEN, GPIO.HIGH)
        GPIO.output(LED_RED, GPIO.LOW)
        GPIO.output(LED_YELLOW, GPIO.LOW)
    else:
        GPIO.output(LED_GREEN, GPIO.LOW)
        GPIO.output(LED_RED, GPIO.LOW)
        GPIO.output(LED_YELLOW, GPIO.LOW)


def ledSetup():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(LED_GREEN, GPIO.OUT)
    GPIO.setup(LED_YELLOW, GPIO.OUT)
    GPIO.setup(LED_RED, GPIO.OUT) 


class Tee(object):
    def __init__(self, *files):
        self.files = files
    def write(self, obj):
        for f in self.files:
            f.write(obj)

f = open('logfile', 'w')
backup = sys.stdout
sys.stdout = Tee(sys.stdout, f)



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
    drive.commandCentreMobilityControl(command)
    return '{}'

# Use MobilityScript Method to set command
@app.route('/collection/<command>')
def collectionControl(command):
    print("================")
    print(command)
    print("================")
    collection.commandCentreCollectionControl(command)
    return '{}'

# Use MobilityScript Method to set command
@app.route('/vision/<command>')
def visionControl(command):
    print("================")
    print(command)
    print("================")
    vision.commandCentreVisionControl(command)
    return '{}'

@app.route('/navigation/<command>')
def navigationControl(command):
    print("================")
    print(command)
    print("================")
    if (command == "n"):
        nav.commandNav = True
    else:
        nav.commandNav = False
        drive.drive(0, 0, False) # not in navMain

    while nav.commandNav == True:
        vision.UpdateObjectPositions()
        objects = vision.GetDetectedObjects()
        sampleCollected = vision.sampleCollected()
        state.updateState(objects,sampleCollected)
        v, w = nav.updateVelocities(state)
        ledIndicator(nav.stateMode)
        collection.sampleManage(nav.rotState)
        drive.drive(v, w, nav.centering) # not in navMain
    return '{}'



def gen():
    while True:
        frame = vision.selfCapRead()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')


@app.route('/video_feed')
def video_feed():
    return Response(gen(),mimetype='multipart/x-mixed-replace; boundary=frame')



#---------------#
# Initialise
#---------------#

# Initialise Functions and Classes
# Subsystem
drive = mobilityScript.Mobility()
vision = vision3.Vision()
collection = collection.Collection()

# nav

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
        collection.ROT_BOOT()

        while(1):
            print("""
            Please select Drive Mode
            a    Automatic
            m    Manual - Discrete (Enter Button)
            n    Manual - Continuous (Hold button)
            c    CommandCentre (TESTING)
            t    Playspace ;) 
            q    quit
            """)
            userSelect = input()
            if  userSelect == "a":
                print("Choose starting state, 0 - 13")
                startState = int(input())
                loc = localisation.Localisation()
                nav = navigation.Navigation() 
                state = state.State()
                nav.stateMode = startState
                # CHUCK THAT CHUNK HERE
                while True:
                    print("==========================================")
                    print("State:",nav.stateMode, "Samples", nav.numSampleCollected)
                    print("==========================================")
                    # vision.updateVisionState(nav.stateMode)
                    objects = vision.GetDetectedObjects(nav.stateMode)
                    sampleCollected = vision.sampleCollected()
                    state.updateState(objects,sampleCollected, vision.landerArea)
                    v, w = nav.updateVelocities(state)
                    loc.getWheelAngVel(v, w)
                    ledIndicator(nav.stateMode)
                    collection.sampleManage(nav.rotState)
                    drive.drive(v, w, nav.centering) # not in navMain
                
            elif userSelect == "m":
                collection.Lander()
                drive.manualControl()
            elif userSelect == "n":
                drive.continuousControl()
            elif userSelect == "c":
                print("Starting Command Centre ...")
                app.run(host='0.0.0.0',port=6969,debug=False)
            elif userSelect == "t":
                print("testing")
                while True:
                    collection.Hard_Open_ROT()
                    time.sleep(2)
                    collection.Hard_Close_ROT()
                    time.sleep(1)
    
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


