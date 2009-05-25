"""
Sometimes we may have to use a pygame interface to the camera, sometimes opencv.
"""

import opencv
import opencv.cv as cv
import opencv.highgui as hg
import conversionUtils

opencv_camera = True

size = width,height = 640,480

class Camera():
    
    def __init__(self, imageType='opencv'):
        self.imageType = imageType
        clist = list_cameras()
        self.capture = hg.cvCreateCameraCapture(clist[0])

        self.storage = cv.cvCreateMemStorage(0)
        
        
        # set the wanted image size from the camera
        hg.cvSetCaptureProperty (self.capture, hg.CV_CAP_PROP_FRAME_WIDTH, width)
        hg.cvSetCaptureProperty (self.capture, hg.CV_CAP_PROP_FRAME_HEIGHT, height)
    
    def get_image(self,*argv,**argd):
        """Since we are using opencv, this will return a cvmat image unless forced."""
        if self.imageType == "pygame":
            return conversionUtils.cv2SurfArray(hg.cvQueryFrame(self.capture))
        return hg.cvQueryFrame(self.capture)

    def start(self):
        pass
    
    def query_image(self):
        return True
    
def list_cameras():
    return [0]  # FIXME
    cams = []
    for i in range(6):
        try:
            #capture = hg.cvCreateCameraCapture( i )  # Must be a better way of doing this...
            if capture is not None:
                cams.append(i)
        except Exception, e:
            pass
    return cams
       
        
def init():
    """
    Work out at this point what we will use...
    """
    try:
        raise "aoeu"
        #import pygame.camera as pygameCamera
        #import pygame.camera.Camera as Camera
        #use_pygame = True
        #pygameCamera.init()
    except:
        use_pygame = False
        
if __name__ == "__main__":
    init()
    cvWin = hg.cvNamedWindow( "result", 1 ) # is this needed? return value?
    cam = Camera()
    a = cam.get_image()
    k = ''

    while(k != "\x1b"):
            # handle events
            k = hg.cvWaitKey(10)
            a = cam.get_image()
            hg.cvShowImage ('result', a)



