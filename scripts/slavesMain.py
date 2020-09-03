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
    pass
else:
    from mobilityScript import mobilityScript
    # from navigationScript import 
    # from collectionScript import
    # from visionScript import


#---------------#
# MainScript
#---------------#

if __name__ == '__slavesMain__':
    # Load Objects or Simulation
    if SIMULATION:
        pass
    else:
        drive = mobilityScript.Mobility()

    # Initialise States
    vel = 0
    angVel = 0


    # Try Loading And running
    try:
        while True:
            if SIMULATION:
                pass
            else:
                print("""
                Please select Drive Mode
                a    Automatic
                m    Manual
                q    quit
                """)
                userSelect = input()
                if  userSelect == "a":
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
