#====================================#
# EGB320
# Command Centre Interface Script
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

# Import Python Library for CommandCentre
from flask import Flask
from flask import render_template, request
from views import views_blueprint

# Set Global Parameters 
SIMULATION = False
app = Flask(__name__)
global command


# Local modules
if SIMULATION:

    #drive = vrep.mobility()
    pass
else:
    from mobilityScript import mobilityScript
    # from navigationScript import 
    # from collectionScript import
    # from visionScript import
    print("loadingclass...")
    # Initialise Functions and Classes
    drive = mobilityScript.Mobility()

#---------------#
# MainScript
#---------------#
print("beforemain")
if __name__ == '__main__':
    # Load Objects or Simulation
    print("beforeSimCheck...")

    if SIMULATION:
        # Load nav tings
        pass
    else:
        print("afterSimCheck...")
        
        # Launch command centre

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
                    pass
                elif userSelect == "m":
                    drive.manualControl()
                elif userSelect == "n":
                    drive.continuousControl()
                elif userSelect == "c":
                    print("Starting Command Centre ...")
                    app.run(host='0.0.0.0',port=6969,debug=True)
                elif userSelect == "q":
                    drive.gpioClean()
                    break
                else:
                    print("Unknown Command")
        # Clean up when closing        
        except KeyboardInterrupt:
            if not SIMULATION:
                drive.gpioClean()
                print("CleanergoVRMMM...")


