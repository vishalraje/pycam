"""
Sometimes we may have to use a pygame interface to the camera, sometimes opencv, 
to avoid changing lots of code this camera class is a wrapper around the opencv code - looking like pygames camera.
"""

import opencv
import opencv.cv as cv
import opencv.highgui as hg
import conversionUtils

import pygame
from pygame.locals import *
from pygame import surfarray

opencv_camera = True


class Camera():
    """
    Simulate the pygame camera class using opencv for capturing.
    Takes one additional parameter than a pygame.camera.Camera - imageType which is the return type,
    can be set as:
         'opencv' - this returns an opencv.CvMat
         'pygame' - returns a pygame surface, if surface is passed in - it will try blit directly to it.

    """
    def __init__(self, device, size, mode, imageType='opencv'):
        self.imageType = imageType
        self.size = self.width, self.height = size
        self.device = device

        self.capture = hg.cvCreateCameraCapture(self.device)

        # set the wanted image size from the camera
        hg.cvSetCaptureProperty (self.capture, hg.CV_CAP_PROP_FRAME_WIDTH, self.width)
        hg.cvSetCaptureProperty (self.capture, hg.CV_CAP_PROP_FRAME_HEIGHT, self.height)
    
    def get_image(self,surface=None,*argv,**argd):
        """Since we are using opencv, this will return a cvmat image or if pygame was specified a 3dpixel array"""
        if self.imageType == "pygame":
            try:
                surfarray.blit_array(surface,conversionUtils.cv2SurfArray(hg.cvQueryFrame(self.capture)))
                return surface
            except:
                return surfarray.make_surface(conversionUtils.cv2SurfArray(hg.cvQueryFrame(self.capture))).convert()
        return hg.cvQueryFrame(self.capture)

    def start(self):
        pass
    
    def query_image(self):
        return True
    
def list_cameras():
    #return [0]  # FIXME
    cams = []
    for i in range(3):
        try:
            capture = hg.cvCreateCameraCapture( i )  # Must be a better way of doing this...
            if capture is not None:
                cams.append(i)
        except Exception, e:
            pass
        finally:
            hg.cvReleaseCapture(capture)
    return cams
       
        
def init():
    """
    Work out at this point what we will use...
    """
    pass

def opencvSnap(dev,size):
    # First lets take a picture using opencv, and display it using opencv...
    cvWin = hg.cvNamedWindow( "Opencv Rendering and Capture", 0 )

    print("Opening device %s, with video size (%s,%s)" % (dev,size[0],size[1]))
    
    # creates the camera of the specified size and in RGB colorspace
    cam = Camera(dev, size, "RGB")
    
    a = cam.get_image()
    hg.cvShowImage ('Opencv Rendering and Capture', a)
    # Wait for any key then clean up - close the capture stream to avoid problems later
    k = hg.cvWaitKey()
    hg.cvDestroyWindow("Opencv Rendering and Capture")
    hg.cvReleaseCapture(cam.capture)
    del cam
 
def pygameSnap(dev,size):
    # Take a picture in opencv and display it in pygame...

    print("Opening device %s, with video size (%s,%s), in pygame mode (returns pygame surface)" % (dev,size[0],size[1]))
    
    # creates the camera of the specified size in pygame mode
    cam = Camera(dev, size, "RGB", imageType='pygame')

    display = pygame.display.set_mode( size, 0 )
    pygame.display.set_caption("Pygame Render, Opencv Capture")
    snapshot = cam.get_image()
    
    display.blit(snapshot, (0,0))
    while(True):
        pygame.display.flip()
        e = pygame.event.poll()
        if e.type == QUIT or e.type == KEYDOWN and e.key == K_ESCAPE:
            break
    pygame.quit()
                   
if __name__ == "__main__":
    init()
    
    clist = list_cameras()
    if not clist:
        raise ValueError("Sorry, no cameras detected.")
    
    dev = clist[0]
    size = (640,480)
    
    opencvSnap(dev,size)
    
    pygameSnap(dev,size)

    


