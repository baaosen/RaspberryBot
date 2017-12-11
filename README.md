# RaspberryBot
The RaspberryBot is a Raspberry Pi web controlled robot that transmits a live stream, GUI for motor controls, and transmits data from four Time-of-Flight (ToF) sensors to a web GUI. The robot uses an H-Bridge [TB6612FNG](https://www.sparkfun.com/products/9457) to connect the motors to the Raspberry Pi. Four ToF [VL53L0X](https://www.adafruit.com/product/3317) sensors are used to inform the user of the distance around the robot. A Raspberry Pi Camera Module transmits a live stream to a website, but you can also use an USB camera. This project also uses Flask to allow the webserver and a Python program to comunicate between each other. 
## Components
- [Raspberry Pi 3 Model B](https://www.raspberrypi.org/products/raspberry-pi-3-model-b/)
- [Raspberry Pi Camera Module V2](https://www.raspberrypi.org/products/camera-module-v2/)
- [H-Bridge TB6612FNG](https://www.sparkfun.com/products/9457)
- [Tof Sensors VL53L0X](https://www.adafruit.com/product/3317) 
- [Motors](https://www.sparkfun.com/products/13302)
- [Wheels](https://www.sparkfun.com/products/13259)
- [Robot Base](https://www.sparkfun.com/products/13301)

## Pinouts

| **Pi Pinout**  |          |
| ------------- | ------------- |
| GPIO 11  | PWMA-HB  |
| GPIO 12  | PWMB-HB  |
| GPIO 13  | AIN2-HB  |
| GPIO 15  | AIN1-HB  |
| GPIO 16  | BIN1-HB  |
| GPIO 18  | BIN2-HB  |
| **H-Bridge**  |               |
| ------------- | ------------- |
| STBY          | 3.3V |
| VM           | 5.0V(Pi Pin 1) |
| VCC | 3.3V |
| A01      | Left Motor + |
| A02      | Left Motor - |
| B02      | Right Motor - |
| A01      | Right Motor + |
|GND (All) | GND |
| **ToF**  |               |
| ------------- | ------------- |
| Sensors Vin (All) | 3.3V|
| Sensors GND (All) | GND|
| Sensors SCL (All) | Pi GPIO 03 |
| Sensors SDA (All) | Pi GPIO 02 |
| Sensor Front SHDN | Pi GPIO 20 |
| Sensor Left SHDN | Pi GPIO 21 |
| Sensor Right SHDN | Pi GPIO 19 |
| Sensor Back SHDN  | Pi GPIO 26 |



## Raspberry Pi Software Setup

### Installing Motion
For installing motion, we used [this tutorial](https://pimylifeup.com/raspberry-pi-webcam-server/comment-page-2/). The setup is intuitive with the Raspberry Pi. Just make sure you use the correct version for raspberry pi. Also if you are using the camera module, there is and extra step at the end (adding bcm2835-v4l2 to sudo nano /etc/modules). When enabling the camera in the ```sudo raspi-config``` you should also enable the I2C, this will be used for the ToF sensors. If you are using an USB camera you should be able to skip the extra step. 

### Installing Flask
The first step is to make sure the python library  is installed for flask.
```sudo apt-get install python-pip```
Then the next step is to install flask
```sudo pip install Flask```
The ```index.html``` file should be in the /templates folder. At the root should be the ```app.py```. This way the Flask server will be able see the html file for the 'GET' requests. 

### ToF Sensors
If you haven't endable I2C in the ```raspi-config``` go ahead and do it now. This should enable the use of the ToF sensors. This project took advantage of the [written libarary](https://github.com/johnbryanmoore/VL53L0X_rasp_python) for the VL53L0X. Now you should be able to download the code, and run it. 

### Video Demo
[![Watch the video](https://img.youtube.com/vi/VID/0.jpg)](https://youtu.be/b65ucAXas-0)
