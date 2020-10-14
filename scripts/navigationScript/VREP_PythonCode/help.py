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
        print("Choose starting state:")
        startState = int(input())
        while True:
            print(startState)
    