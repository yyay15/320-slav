#====================================#
# EGB320
# Command Centre Interface Script
# Group SLAVES: Group 13
# 2020 Semester 2
# Alan Yu
# 
#====================================#


from flask import Blueprint
views_blueprint = Blueprint('views', __name__,)


#---------------#
# Function Definition
#---------------#

@app.route("/")
def index():
    return render_template('commandCentre/commandCentre.html')

@app.route('/leftTurn')
def leftTurn():
    # Command for left turn
    return 'true'

@app.route('/rightTurn')
def rightTurn():
    # Command for right turn
   return 'true'

@app.route('/forward')
def forward():
    # Command for forward
   return 'true'

@app.route('/backward')
def backward():
    # Command to reverse
   return 'true'

@app.route('/stop')
def stop():
    # Command to Stop Robot
   return  'true'
