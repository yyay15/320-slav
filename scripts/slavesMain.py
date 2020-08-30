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



# Set Global Parameters 
SIMULATION = False

# Local modules
if SIMULATION:

    #drive = vrep.mobility()
    pass
else:
    from mobilityScript import mobilityScript
    # from navigationScript import 
    # from collectionScript import
    # from visionScript import

    # Initialise Functions and Classes
    drive = mobilityScript.Mobility()


#---------------#
# MainScript
#---------------#

if __name__ == '__slavesMain__':
    # Load Objects or Simulation
    if SIMULATION:
        # Load nav tings
    else:
        
        # Launch command centre

        # Initialise States for All System
        v = 0
        w = 0


        # Try Loading And running
        try:
            while True:
                print("""
                Please select Drive Mode
                a    Automatic
                m    Manual
                q    quit
                """)
                userSelect = input()
                if  userSelect == "a":
                    # CHUCK THAT CHUNK HERE
                    pass
                elif userSelect == "m":
                    drive.manualControl()
                elif userSelect == "q":
                    drive.gpioClean()
                    break
                else:
                    print("Unknown Command")
        # Clean up when closing        
        except KeyboardInterrupt:
            if not SIMULATION:
                drive.gpioClean()
