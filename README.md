# This is a fork from https://github.com/EbenKouao/pi-camera-stream-flask I used for JHU EN.605.715 project. You guys should check out the original project. It's awesome.

## How it works
The Pi streams the output of the camera module over the web via Flask server. Devices connected to the same network would be able to access the camera stream via

```
<raspberry_pi_ip:5000>
```
The original project uses OpenCV. My project uses picamera2.
I modified the index.html and only get what I need.
I added the gpsd-py3 module (from https://github.com/MartijnBraam/gpsd-py3) to get the gps location from the G-Mouse GPS module.

## Library dependencies
Install the following dependencies to create camera stream.

```
sudo apt-get update
sudo apt-get upgrade

sudo pip3 install flask
sudo pip3 install picamera2
sudo pip3 install gpsd-py3
sudo pip3 install smbus
```

Since it uses picamera2, we don't need to enable legacy camera interface.

## How to run the flask server
```
python3 main.py
```

or 

```
./start_camera.sh
```

## How to setup Autostart your Pi Stream

```
sudo crontab -e
```

Add the following line:
```
@reboot PATH_TO_start_camera.sh
```

## How to flip the camera

There's a vflip and hfip in the `camera.py`, or if you only care about upside down, you can adjust the `flip` boolean flag when init `VideoCamera` object 

## 3D print part

`camera holder.stl` is the 3D model of the camera holder mount
