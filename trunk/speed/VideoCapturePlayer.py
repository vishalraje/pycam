from __future__ import division
from opencv import cv, highgui as hg
import time
import logging


class VideoCapturePlayer(object):
    """
    A VideoCapturePlayer object is an encapsulation of 
    the display of a video stream. 
    
    A process can be given (as a function) that is run
    on every frame between capture and display.
    
    For example a filter function that takes and returns a 
    cvMat can be given. This player will take the webcam image, 
    pass it through the filter then display the result.
    
    """
    #size = width,height = 640, 480
   
    def __init__(self, processFunction = None, title = "Video Capture Player", show=True, **argd):
        self.__dict__.update(**argd)
        super(VideoCapturePlayer, self).__init__(**argd)
        
        self.processFunction = processFunction
        self.processRuns = 0
        self.title = title
        self.show = show
        self.times = []

        if self.show is True:
            self.display = hg.cvNamedWindow(self.title)

        try:
            self.camera = hg.cvCreateCameraCapture(0)
        except:
            print("Couldn't open camera device, is it connected?")
            hg.cvDestroyWindow(title)
            raise SystemExit
        
        # Take a frame to get props and use in testing
        self.frame = hg.cvQueryFrame( self.camera )
        

    def process(self):
        """We will take a snapshot, optionally do some arbitrary process (eg in numpy/scipy)
        then display it.       
        """

            
        try:
            # capture an image
            self.snapshot = hg.cvQueryFrame( self.camera)
       
            if self.processFunction:
                res = self.processFunction(self.snapshot)
                assert isinstance(res,CvMat)
                self.snapshot = res
                self.processRuns += 1
                       
            if self.show:
                hg.cvShowImage( self.title, self.snapshot )
        finally:
            hg.cvDestroyWindow(title)
    

        #avg = numpy.average(fpslist)

    def main(self):
        """Add some timing and event handling code here

        Need two sets of timing code - one for the process itself and one for the system.
        """
        logging.debug("Starting main loop now")
        for i in xrange(1000):
            # save the time since last call
            now = time.clock()
            if has_attr(self,"last_time"):
                self.times.append(now - self.last_time)

            self.last_time = now

            self.process()
        logging.debug("Main loop complete")
        logging.info("Average time per Frame: %i" % sum(self.times)/len(self.times) )

def time_process(func):
    """
    This will just use a single image and repeatitively do the process.
    """
    import timeit
    setup_code = """from __main__ import VideoCapturePlayer
    vcp = VideoCapturePlayer(processFunction=None)"""
    test_code = """vcp.processFunction(vcp.frame)"""
    t = timeit.Timer(test_code, setup_code)
    print("Running tests now")
    print t.repeat()
    print("Tests complete")

if __name__ == "__main__":
    vcp = VideoCapturePlayer(processFunction=None)
    vcp.main()
    #time_process()
