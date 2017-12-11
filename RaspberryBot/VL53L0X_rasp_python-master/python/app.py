from flask import Flask, render_template, request, redirect, url_for, make_response, jsonify
import RPi.GPIO as GPIO
import time
import sys
sys.path.append('/home/pi/Templates/RaspberryBot/VL53L0X_rasp_python-master/python')
import VL53L0X


app = Flask(__name__) #set up flask serverfrom flask import Flask, render_template, flash

app = Flask('testapp')

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM) # GPIO not pin

# initiate motor controls
# set up pin numbers for motor 1
M1A = 27 #(GPIO 27 - Pin 13)
M1B = 22 #(GPIO 22 - Pin 15)
M1E = 17 #(GPIO 17 - Pin 11)
# set up pin numbers for motor 2
M2A = 24 #(GPIO 24 - Pin 18)
M2B = 23 #(GPIO 23 - Pin 16)
M2E = 18 #(GPIO 18 - Pin 12)
# set all pins as output pins
GPIO.setup(M1A,GPIO.OUT)
GPIO.setup(M1B,GPIO.OUT)
GPIO.setup(M1E,GPIO.OUT)
GPIO.setup(M2A,GPIO.OUT)
GPIO.setup(M2B,GPIO.OUT)
GPIO.setup(M2E,GPIO.OUT)

# initiate sensor controls
# set up shutdown pins for VL53L0X sensors
sensor1_shutdown = 20 #(GPIO 20 - Pin 38)
sensor2_shutdown = 21 #(GPIO 21 - Pin 40)
sensor3_shutdown = 19 #(GPIO 19 - Pin 35)
sensor4_shutdown = 26 #(GPIO 26 - Pin 37)
# set all pins as output pins
GPIO.setup(sensor1_shutdown, GPIO.OUT)
GPIO.setup(sensor2_shutdown, GPIO.OUT)
GPIO.setup(sensor3_shutdown, GPIO.OUT)
GPIO.setup(sensor4_shutdown, GPIO.OUT)
# set all pins to 0
GPIO.output(sensor1_shutdown, GPIO.LOW)
GPIO.output(sensor2_shutdown, GPIO.LOW)
GPIO.output(sensor3_shutdown, GPIO.LOW)
GPIO.output(sensor4_shutdown, GPIO.LOW)
time.sleep(0.50)
# set addresses to all the VL53L0X sensors
tof = VL53L0X.VL53L0X(address=0x2B)
tof1 = VL53L0X.VL53L0X(address=0x2D)
tof2 = VL53L0X.VL53L0X(address=0x2E)
tof3 = VL53L0X.VL53L0X(address=0x31)

#
@app.route('/', methods =['POST','GET'])
def index():
    return render_template('index.html')

# Left
@app.route('/1')
def turnLeft():
    GPIO.output(M1A,GPIO.HIGH)
    GPIO.output(M1B,GPIO.LOW)
    GPIO.output(M1E,GPIO.HIGH)
    GPIO.output(M2A,GPIO.LOW)
    GPIO.output(M2B,GPIO.HIGH)
    GPIO.output(M2E,GPIO.HIGH)
    response = make_response(redirect(url_for('index')))
    return(response)

# forward
@app.route('/2')
def forward():
    GPIO.output(M1A,GPIO.LOW)
    GPIO.output(M1B,GPIO.HIGH)
    GPIO.output(M1E,GPIO.HIGH)
    GPIO.output(M2A,GPIO.LOW)
    GPIO.output(M2B,GPIO.HIGH)
    GPIO.output(M2E,GPIO.HIGH)
    response = make_response(redirect(url_for('index')))
    return(response)

# right
@app.route('/3')
def turnRight():
    GPIO.output(M1A,GPIO.LOW)
    GPIO.output(M1B,GPIO.HIGH)
    GPIO.output(M1E,GPIO.HIGH)
    GPIO.output(M2A,GPIO.HIGH)
    GPIO.output(M2B,GPIO.LOW)
    GPIO.output(M2E,GPIO.HIGH)
    response = make_response(redirect(url_for('index')))
    return(response)

# backward
@app.route('/4')
def backward():
    GPIO.output(M1A,GPIO.HIGH)
    GPIO.output(M1B,GPIO.LOW)
    GPIO.output(M1E,GPIO.HIGH)
    GPIO.output(M2A,GPIO.HIGH)
    GPIO.output(M2B,GPIO.LOW)
    GPIO.output(M2E,GPIO.HIGH)
    response = make_response(redirect(url_for('index')))
    return(response)

# stop
@app.route('/5')
def stop():
    GPIO.output(M1A,GPIO.LOW)
    GPIO.output(M1B,GPIO.LOW)
    GPIO.output(M1E,GPIO.LOW)
    GPIO.output(M2A,GPIO.LOW)
    GPIO.output(M2B,GPIO.LOW)
    GPIO.output(M2E,GPIO.LOW)
    response = make_response(redirect(url_for('index')))
    return(response)

# send sensor information to the website
@app.route('/_func', methods =['POST','GET'])
def fun():
    # start up TOF sensors by giving them addresses on the I2C bus
    GPIO.output(sensor1_shutdown, GPIO.HIGH)
    time.sleep(0.01)
    tof.start_ranging(VL53L0X.VL53L0X_BETTER_ACCURACY_MODE)

    GPIO.output(sensor2_shutdown, GPIO.HIGH)
    time.sleep(0.01)
    tof1.start_ranging(VL53L0X.VL53L0X_BETTER_ACCURACY_MODE)

    GPIO.output(sensor3_shutdown, GPIO.HIGH)
    time.sleep(0.01)
    tof2.start_ranging(VL53L0X.VL53L0X_BETTER_ACCURACY_MODE)

    GPIO.output(sensor4_shutdown, GPIO.HIGH)
    time.sleep(0.01)
    tof3.start_ranging(VL53L0X.VL53L0X_BETTER_ACCURACY_MODE)

    # measure distance of each TOF sensor
    distance = tof1.get_distance()

    distance1= tof.get_distance()

    distance2 = tof3.get_distance()

    distance3 = tof2.get_distance()

    # shutdown all TOF sensors
    tof3.stop_ranging()
    GPIO.output(sensor4_shutdown, GPIO.LOW)
    tof2.stop_ranging()
    GPIO.output(sensor3_shutdown, GPIO.LOW)
    tof1.stop_ranging()
    GPIO.output(sensor2_shutdown, GPIO.LOW)
    tof.stop_ranging()
    GPIO.output(sensor1_shutdown, GPIO.LOW)

    # send JSON file with all the distances to the website
    return jsonify(variable=distance, variable1=distance1, variable2=distance2,variable3=distance3)

# run app on port 8000    
app.run(threaded=True,debug=True, host='0.0.0.0', port=8000)
