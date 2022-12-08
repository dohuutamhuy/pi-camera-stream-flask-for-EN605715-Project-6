# main.py
# import the necessary packages
from flask import Flask, render_template, Response, request, send_from_directory
from camera import VideoCamera
import os
import gpsd
import asyncio
import serial
import time
from smbus import SMBus


pi_camera = VideoCamera(flip=True) # flip pi camera if upside down.
gpsd.connect()

# App Globals (do not edit)
app = Flask(__name__, static_folder='static')

# Setup I2C connection
addr = 0x8
bus = SMBus(1)

@app.route('/')
def index():
    return render_template('index.html') #you can customze index.html here

def gen(camera):
    #get camera frame
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')        

@app.route('/video_feed')
def video_feed():
    return Response(gen(pi_camera),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/gps_feed')
def gps_feed():    
    try:
        gps = gpsd.get_current()
        lat = gps.position()[0]
        if lat < 0:
            lat = f'{-lat}' + ' S'
        else:
            lat = f'{lat}' + ' N'
        long = gps.position()[1]
        if long < 0:
            long = f'{-long}' + ' W'
        else:
            long = f'{-long}' + ' E'
        gps_time = gps.time
        alt = gps.alt
        speed = gps.hspeed
        track = gps.track
        climb = gps.climb
        mode = gps.mode
        if mode == 1:
            mode = "No Fix"
        elif mode == 2:
            mode = "2D Fix"
        elif mode == 3:
            mode = "3D Fix"
        error = gps.error
        data = f'Time: {gps_time}<br>' + \
                f'Latitude: {lat}<br>' + f'Longitude: {long} <br>' + \
                f'Altitude (MSL): {alt} meters<br>' + f'HSpeed: {speed} meters/sec<br>' + \
                f'Track: {track} deg<br>' + f'Climb: {climb} meters/sec<br>' + \
                f'Status: {mode} <br>' + \
                f'Long Error: {error["x"]} meters <br>' + \
                f'Lat Error: {error["y"]} meters <br>' + \
                f'Alt Error: {error["v"]} meters <br>' + \
                f'Speed Error: {error["s"]} meters/sec <br>' + \
                f'Time offset: {error["t"]} sec <br>' + \
                f'Satellites: {gps.sats}'
        return Response(data.encode('UTF-8'),
                        mimetype='text/plain')
    except Exception as e:
        print(e)
        return Response(f"Failed to retrieve data due to error: {e}".encode("UTF-8"), mimetype='text/plain')

def imu_gen():
    try:
        IMUdata = bus.read_i2c_block_data(addr, 0)
        arr = ""
        for each in IMUdata:
            if each == 255:
                break
            arr += chr(each)
        if len(arr) > 2:
            elements = arr.split(",")
            line_string = f"Yaw: {elements[0]}\tPitch: {elements[1]}\tRoll: {elements[2]}"
            line_byte = line_string.encode('ascii')
            line_string = line_string.replace('\t', "&ensp;&ensp;")
            is_bluetooth_connected = False
            bluetooth_ser = None
            if not is_bluetooth_connected:
                try:
                    bluetooth_ser = serial.Serial('/dev/rfcomm0', 115200)
                    is_bluetooth_connected = True
                except Exception as e:				
                    pass
                if line_string != '':
                    if is_bluetooth_connected:
                        try:
                            bluetooth_ser.write(line_byte)
                        except:
                            is_bluetooth_connected = False
            return line_string.encode('UTF-8')
    except Exception as e:
        print(f"Failed to retrieve data due to error: {e}")
        return f"Failed to retrieve data due to error: {e}".encode("UTF-8")



    ### Old way with bluetooth
    # try:
    #     with serial.Serial('/dev/ttyUSB0', 115200) as ser:
    #         is_bluetooth_connected = False
    #         bluetooth_ser = None
    #         while True:
    #             if not is_bluetooth_connected:
    #                 try:
    #                     bluetooth_ser = serial.Serial('/dev/rfcomm0', 115200)
    #                     is_bluetooth_connected = True
    #                 except Exception as e:				
    #                     pass 
    #             line_byte = ser.readline()
    #             line_string = line_byte.decode('utf-8').rstrip("\n")
    #             line_string = line_string.replace('\t', "&ensp;&ensp;")
    #             if line_string != '':
    #                 if is_bluetooth_connected:
    #                     try:
    #                         bluetooth_ser.write(line_byte)
    #                     except:
    #                         is_bluetooth_connected = False
    #                 yield(line_string)
    # except Exception as e:
    #     print(e)
    #     return f"Failed to retrieve data due to error: {e}".encode("UTF-8")

@app.route('/imu_feed')
def imu_feed():
    return Response(imu_gen(),
                    mimetype='text/plain')

# Take a photo when pressing camera button
@app.route('/picture')
def take_picture():
    pi_camera.take_picture()
    return "None"

if __name__ == '__main__':

    app.run(host='0.0.0.0', debug=False)
