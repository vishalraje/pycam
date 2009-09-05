#!/usr/bin/env python
from __future__ import division
from opencv import cv, highgui as hg
import time
import logging

verbosity = logging.INFO
profiling = False

logging.basicConfig(filename=None,level=verbosity,)




class VideoCapturePlayer(object):
    """
    A VideoCapturePlayer object is an encapsulation of 
    the display of a video stream. 
    
    A process can be given (as a function) that is run
    on every frame between capture and display.
    
    For example a filter function that takes and returns a 
    cvMat can be given. This player will take the webcam image, 
    pass it through the filter then display the result.
    
    >>> vcp = VideoCapturePlayer()  # Open the webcam.
    >>> vcp.main()  # should start capturing and showing the webcam
    
    And defining and giving a process function to the player:
    
    >>> def drawBox(x):
    ....    pt1, pt2 = cv.CvPoint(), cv.CvPoint()
    ....    pt1.x = pt1.y = 200
    ....    pt2.x = pt2.y = 250
    ....    cv.cvRectangle( x, pt1, pt2, cv.CV_RGB(30,0,200) )
    ....    return x
    >>> vcp = VideoCapturePlayer(processFunction=drawBox)
    >>> vcp.main()
    
    """

   
    def __init__(self, processFunction = None, title = "Video Capture Player", show=True, **argd):
        self.__dict__.update(**argd)
        super(VideoCapturePlayer, self).__init__(**argd)
        t_begin = time.time()
        self.processFunction = processFunction
        self.title = title
        self.show = show

        if self.show is True:
            self.display = hg.cvNamedWindow(self.title)

        try:
            self.camera = hg.cvCreateCameraCapture(0)
        except:
            print("Couldn't open camera device, is it connected?")
            hg.cvDestroyWindow(title)
            raise SystemExit
        
        # Take a frame to get props and use in testing
        self.snapshot = cv.cvCloneMat( hg.cvQueryFrame( self.camera ) )
        # check that we got an image, otherwise try again.
        for i in xrange(100):
            if self.snapshot is not None: break
            self.snapshot = hg.cvQueryFrame( self.camera )
        

    def process(self, take_new_image=True):
        """We will take a snapshot, optionally do some arbitrary process (eg in numpy/scipy)
        then display it. If a frame is given use that instead of taking a new image.
        """
 
        try:
            if take_new_image:
                logging.debug("capturing an image")
                self.snapshot = cv.cvCloneMat( hg.cvQueryFrame( self.camera) )
       
            if self.processFunction is not None:
                logging.debug("Sending image to process function")
                res = self.processFunction(self.snapshot)
                logging.debug("Received result from processing function")
                assert isinstance(res,cv.CvMat), "Not CvMat"
                self.snapshot = res
                       
            if self.show:
                hg.cvShowImage( self.title, self.snapshot )
        except Exception, e:
            # If something goes wrong make sure we close the window
            logging.error("Error in processing image: %s" % e)
            hg.cvDestroyWindow(self.title)
            raise SystemExit


    def main(self):
        """
        Run and time the main loop.
        """
        logging.info("Starting main video capture loop now, press 'q' to quit")
        key = hg.cvWaitKey(1)
        
        num_frames = 0
        start_time = time.time()
        
        while(key is not "q" and key != '\x1b'):
            num_frames +=1
            self.process()
            key = hg.cvWaitKey(5)
            
        total_time = float(time.time()) - float(start_time)
        
        logging.debug("Main loop complete")
        logging.debug("Total time took %e" % total_time)
        
        logging.info("Average time per frame: %e" % (total_time/num_frames) )
        logging.info("Average frames per second: %f" % (num_frames/total_time) )


# Todo put in misc file
def drawBox(x):
    """
    This is a template for a function that can be fed into VideoCapturePlayer
    It must take a CvMat, and return a CvMat.
    It draws a rectangle on the screen."""
    pt1, pt2 = cv.CvPoint(), cv.CvPoint()
    pt1.x = pt1.y = 200
    pt2.x = pt2.y = 250
    
    cv.cvRectangle( x, pt1, pt2, cv.CV_RGB(30,0,200) )
    return x


if __name__ == "__main__":
    logging.info("Starting the example VideoCapturePlayer")
    
    #vcp = VideoCapturePlayer(processFunction=drawBox)
    vcp = VideoCapturePlayer()
    
    if profiling:
        import cProfile
        cProfile.run('vcp.main()', 'python_profile_data')
        del vcp
        import pstats
        p = pstats.Stats('python_profile_data')
        process_stats = p.strip_dirs().sort_stats('cum').print_stats("process",1)
        print("Ideally the 'percall' value is close to our estimate of time per frame")
        
    else:
        vcp.main()


def time_process():
    """
    This will just use a single image and repeatitively do the process.
    The camera has to be free for this to work
    """
    import timeit
    setup_code = """from VideoCapturePlayer import VideoCapturePlayer
vcp = VideoCapturePlayer(processFunction=None,show=False)"""
    test_code = "vcp.process(take_new_image=False)"
    t = timeit.Timer(test_code, setup_code)
    print("Running timeit on capture/display now")
    print t.repeat()
    print("Tests complete")
