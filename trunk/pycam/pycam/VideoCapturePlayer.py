import pygame
from pygame.locals import *
import numpy
import exceptions

import logging
verbose = True

"""
Future API changing notes.
It would be good to combine the VideoCapturePlayers (VCP) for OpenCV and for Pygame.
Maybe using functools a VCP could be made using the optimal data storage format?

Or could have in the constructor args a opencvprocess and a numpyprocess and a surface process
and depending on what is given create the right display and use the right data storage...


"""

logging.debug("Pygame Version: %s" % pygame.__version__)

class VideoCapturePlayer(object):
    """
    A VideoCapturePlayer object is an encapsulation of 
    the display of a video stream. 
    
    A process can be given (as a function) that is run
    on every frame between capture and display.
    
    For example a filter function that takes and returns a 
    surface can be given. This player will take the webcam image, 
    pass it through the filter then display the result.
    
    If the function takes significant computation time (>1second)
    The VideoCapturePlayer takes 3 images between each, this flushes
    the buffer, ensuring an updated picture is used in the next computation.
     
    If a new version of pygame is installed - this class uses the pygame.camera module, otherwise 
    it uses opencv.
    """
    size = width,height = 640, 480
   
    def __init__(self, processFunction = None, forceOpenCv = False, displaySurface=None, show=True, **argd):
        self.__dict__.update(**argd)
        super(VideoCapturePlayer, self).__init__(**argd)
        logging.debug("Initializing Video Capture Class")
        self.processFunction = processFunction
        self.processRuns = 0
        
        self.show = show
        
        self.display = displaySurface
        if self.display is None:
            if show is True:
                # create a display surface. standard pygame stuff
                self.display = pygame.display.set_mode( self.size, 0 )
            else:
                pygame.display.init()
                #pygame.display.set_mode((0,0),0)
                self.display = pygame.surface.Surface(self.size)
        
        if forceOpenCv:
            import camera
        else:
            import pygame.camera as camera
        camera.init()
        
        # gets a list of available cameras.
        self.clist = camera.list_cameras()
        if not self.clist:
            raise ValueError("Sorry, no cameras detected.")
        
        logging.info("Opening device %s, with video size (%s,%s)" % (self.clist[0],self.size[0],self.size[1]))
        
        # creates the camera of the specified size and in RGB colorspace
        if not forceOpenCv:
            try:
                self.camera = camera.Camera(self.clist[0], self.size, "RGB")
                # starts the camera
                self.camera.start()
            except:
                logging.debug("Ignoring that pygame camera failed - we will try opencv")
                forceOpenCv = True
                del camera
                import camera
                self.clist = camera.list_cameras()
        if forceOpenCv:
            logging.debug("Trying to open the OpenCV wrapped camera")
            self.camera = camera.Camera(self.clist[0], self.size, "RGB", imageType="pygame")
            self.camera.start()
            
        logging.info("Waiting for camera...")
        self.waitForCam()
        logging.info("Camera ready.")

        self.clock = pygame.time.Clock()
        self.processClock = pygame.time.Clock()

        # create a surface to capture to.  for performance purposes, you want the
        # bit depth to be the same as that of the display surface.
        self.snapshot = pygame.surface.Surface(self.size, 0, self.display)

    def get_and_flip(self):
        """We will take a snapshot, do some arbitrary process (eg in numpy/scipy)
        then display it.       
        """
        # capture an image
        self.snapshot = self.camera.get_image(self.snapshot)#.convert()
        #self.snapshot = self.camera.get_image(self.snapshot) # if not use this line
   
        if self.processFunction:
            self.processClock.tick()
            if self.processRuns > 5 and self.processClock.get_fps() < 2:
                # The function is really slow so take a few frames.
                if verbose:
                    print "Running your resource intensive process at %f fps" % self.processClock.get_fps()
                # flush the camera buffer to get a new image... 
                # we have the time since the process is slow...
                for i in range(5):
                    self.waitForCam()
                    self.snapshot = self.camera.get_image(self.snapshot)#.convert()
            else:
                self.waitForCam()
                self.snapshot = self.camera.get_image(self.snapshot)
            #try:
            res = self.processFunction(self.snapshot)
            if isinstance(res,pygame.Surface): self.snapshot = res
            self.processRuns += 1
                    
                #except Exception, e:
                #    print e
                #    raise exceptions.RuntimeError("error while running the process function")
        if self.show is not False:
            # blit it to the display surface.  simple!
            self.display.blit(self.snapshot, (0,0))
            pygame.display.flip()
   
    def waitForCam(self):
       # Wait until camera is ready to take image
        while not self.camera.query_image():
            pygame.time.wait(100)
    
    def main(self):
        """Start the video capture loop"""
        if verbose:
            print "Video Capture & Display Started... press Escape to quit"
        going = True
        fpslist = []
        while going:
            events = pygame.event.get()
            for e in events:
                if e.type == QUIT or (e.type == KEYDOWN and e.key == K_ESCAPE):
                    going = False
            
            # if you don't want to tie the framerate to the camera, you can check and
            # see if the camera has an image ready.  note that while this works
            # on most cameras, some will never return true.
            # note seems to work on my camera at hitlab - Brian
            if self.camera.query_image():
                self.get_and_flip()
                self.clock.tick()
                if self.clock.get_fps():
                    fpslist.append(self.clock.get_fps())
                    if verbose:
                        print "fps: ",fpslist[-1]
        print "Video Capture &  Display complete."
        print "Average Frames Per Second " 
        avg = numpy.average(fpslist)
        print avg
        if self.processFunction:
            print "Process ran at %f fps" % self.processClock.get_fps()

if __name__ == "__main__":
    vcp = VideoCapturePlayer(processFunction=None,forceOpenCv=False)
    vcp.main()
    pygame.quit()
