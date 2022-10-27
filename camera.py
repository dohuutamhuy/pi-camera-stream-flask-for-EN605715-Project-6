#Modified by smartbuilds.io
#Date: 27.09.20
#Desc: This scrtipt script..

import time
import io
from libcamera import Transform
from picamera2 import Picamera2
from datetime import datetime


class VideoCamera(object):
    def __init__(self, flip = False, file_type  = ".jpg", photo_string= "stream_photo"):
        self.vs = Picamera2()
        self.capture_config = self.vs.create_still_configuration()
        self.vs.configure(self.vs.create_preview_configuration({"size": (800, 600)}, transform=Transform(hflip=flip, vflip=True)))
        self.vs.start()
        self.file_type = file_type # image type i.e. .jpg
        self.photo_string = photo_string # Name to save the photo
        time.sleep(2.0)

    def __del__(self):
        print("STOP")

    def get_frame(self):
        jpeg = io.BytesIO()
        try:
                self.vs.capture_file(jpeg, format='jpeg')
        except RuntimeError:
                jpeg = self.previous_frame
        self.previous_frame = jpeg
        return jpeg.getbuffer()

    # Take a photo, called by camera button
    def take_picture(self):
        today_date = datetime.now().strftime("%m%d%Y-%H%M%S") # get current time
        print(self.vs.capture_file(today_date+self.file_type))
