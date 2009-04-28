import pygame
import pygame.camera
from pygame.locals import *
import numpy

class VideoCapturePlayer(object):
    """A VideoCapturePlayer object is an encapsulation of 
    the display of a video stream. A process can be 
    given (as a function) that is done on every frame
    
    For example a filter function that takes and returns a 
    surface can be given. This player will take the webcam image, 
    pass it through the filter then display the result.
    
    If the function takes significant computation time (>1second)
    The VideoCapturePlayer takes 3 images between each, this ensures 
    an updated picture is used in the next computation.
    
    """
    size = width,height = 640, 480
   
    def __init__(self, processFunction = None, forceOpenCv = False, **argd):
        self.__dict__.update(**argd)
        super(VideoCapturePlayer, self).__init__(**argd)
        
        pygame.init()
        pygame.camera.init()
        
        if forceOpenCv:
            import os
            os.environ["PYGAME_CAMERA"] = "opencv"
        
        self.processFunction = processFunction
        
        # create a display surface. standard pygame stuff
        self.display = pygame.display.set_mode( self.size, 0 )

        # gets a list of available cameras.
        self.clist = pygame.camera.list_cameras()
        if not self.clist:
            raise ValueError("Sorry, no cameras detected.")

        # creates the camera of the specified size and in RGB colorspace
        self.camera = pygame.camera.Camera(self.clist[0], self.size, "RGB")

        # starts the camera
        self.camera.start()
        
        self.waitForCam()

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
        self.snapshot = self.camera.get_image(self.snapshot).convert()
        #self.snapshot = self.camera.get_image(self.snapshot) # if not use this line
   
        # todo would this work? - Would be far better style!
        #self.snapshot = self.camera.get_image()
   
        if self.processFunction:
            self.processClock.tick()
            if self.processClock.get_fps() < 2:
                print "Running your resource intensive process at %f fps" % self.processClock.get_fps()
                # flush the camera buffer to get a new image... 
                # we have the time since the process is so damn slow...
                for i in range(3):
                    self.waitForCam()
                    self.snapshot = self.camera.get_image(self.snapshot).convert()
            self.snapshot = self.processFunction(self.snapshot)
        
        # blit it to the display surface.  simple!
        self.display.blit(self.snapshot, (0,0))
        pygame.display.flip()
   
    def waitForCam(self):
       # Wait until camera is ready to take image
        while not self.camera.query_image():
            pass
    
    def main(self):
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
                    print "fps: ",fpslist[-1]
        print "Video Capture &  Display complete."
        print "Average Frames Per Second " 
        avg = numpy.average(fpslist)
        print avg
        
if __name__ == "__main__":
    
    vcp = VideoCapturePlayer(processFunction=None,forceOpenCv=True)
    vcp.main()
    pygame.quit()
