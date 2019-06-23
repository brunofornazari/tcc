from picamera.array import PiRGBArray
from picamera import PiCamera


class Camera:
    def __init__(self):
        self.camera = PiCamera()
        self.camera.resolution = (320, 240)
        self.camera.framerate = 32
        self.rawCapture = PiRGBArray(self.camera, size=(320, 240))


    def capture(self):
        return self.camera.capture_continuous(self.rawCapture, format="bgr",
                                       use_video_port=True)
