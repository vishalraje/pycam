#!/usr/bin/python
"""
This library is used for object detection using haar-like features.
The program finds haar cascade objects in a camera image or video stream and displays a red box around them.

An objectDetector can be made with a harrcascade name.
Usage:
    >>> od = objectDetector("haarcascade_frontalface_default.xml")
    >>> object = od.detectObject(surfaceImage)
    >>> object.width
    45
    >>> object.x
    200
    


TODO: make into a class
TODO: make it standalone runnable as well...
TODO: use optparser

"""

from os import path
import sys
import exceptions
import opencv
from opencv.cv import *
from opencv.highgui import *

cascades = {
            'eye': "haarcascade_eye",
            'head': "haarcascade_frontalface_default",
            'face': "haarcascade_frontalface_alt",
            'profile': 'haarcascade_profileface',
            'fullbody': "haarcascade_fullbody",
            'upperbody':'haarcascade_upperbody',
            'lowerbody': 'haarcascade_lowerbody',
            }

cascadeExtension = ".xml"
# TODO: generate these from evironment vars... eg for windows...
cascadePaths = (
                '/usr/local/share/opencv/haarcascades/',
                '/usr/share/opencv/haarcascades/',
                ) 

def findCascade(cascade):
    """
    Given the most flimsy of names like "face" or "eye" give a valid file path of a Haar cascade.
        
        >>> findCascade('eye')
        '/usr/local/share/opencv/haarcascades/haarcascade_eye.xml'
        
    """
    if cascades.has_key(cascade):
        for cp in cascadePaths:
            testFile = cp + cascades[cascade] + cascadeExtension
            if path.exists(testFile):
                return testFile
    
    if not cascade.endswith(cascadeExtension):
        cascade += cascadeExtension
    
    if path.exists(cascade):
        return cascade
    
    for objectString in cascades:
        if cascade in objectString:
            return findCascade(cascades[objectString])
      

class ObjectDetector(object):
    """
    An ObjectDetector is used to detect harr like features in an image.
    """
    def __init__(self,cascadeName="face"):
        self.storage = cvCreateMemStorage(0)
        self.cascade_name = findCascade(cascadeName)
        print cascadeName
        
        # the OpenCV API says this function is obsolete, but we can't
        # cast the output of cvLoad to a HaarClassifierCascade, so use this anyways
        # the size parameter is ignored
        self.cascade = cvLoadHaarClassifierCascade( self.cascade_name, cvSize(1,1) )
        if( self.cascade ):
            print "cascade loaded..."
        else:
            raise exceptions.IOError("Could not locate cascade file.")
        self.cvWin = cvNamedWindow( "result", 1 ) # is this needed? return value?
        
        # Parameters for haar detection
        # From the API:
        # The default parameters (scale_factor=1.1, min_neighbors=3, flags=0) are tuned 
        # for accurate yet slow object detection. For a faster operation on real video 
        # images the settings are: 
        # scale_factor=1.2, min_neighbors=2, flags=CV_HAAR_DO_CANNY_PRUNING, 
        # min_size=<minimum possible object size
        self.min_size = cvSize(15,15)
        self.image_scale = 1.3        # TODO what does this one do?
        self.haar_scale = 1.2
        self.min_neighbors = 2
        self.haar_flags = 0



    def detectObject(self,img):
        """
        This should be pure opencv and reasonably quick.
        """
        # Could this go into init?
        gray = cvCreateImage( cvSize(img.width,img.height), 8, 1 )
        small_img = cvCreateImage( cvSize( cvRound (img.width/self.image_scale),
                                           cvRound (img.height/self.image_scale)), 8, 1 )
        cvCvtColor( img, gray, CV_BGR2GRAY )
        cvResize( gray, small_img, CV_INTER_LINEAR )
        cvEqualizeHist( small_img, small_img )
        cvClearMemStorage( self.storage )
    
        
        if( self.cascade ):
            t = cvGetTickCount()
            objects = cvHaarDetectObjects( small_img, self.cascade, self.storage,
                                         self.haar_scale, self.min_neighbors, self.haar_flags, self.min_size )
            t = cvGetTickCount() - t
            print "%i objects found, detection time = %gms" % (objects.total,t/(cvGetTickFrequency()*1000.))
            return objects
        else:
            print "no cascade"
    
    def detect_and_draw(self, img):
        """
        draw a box with opencv on the image around the detected faces.
        """
        objects = self.detectObject(img)
        if objects:
            for r in objects:
                print "Oject found at (x,y) = (%i,%i)" % (r.x*self.image_scale,r.y*self.image_scale)
                pt1 = cvPoint( int(r.x*self.image_scale), int(r.y*self.image_scale))
                pt2 = cvPoint( int((r.x+r.width)*self.image_scale), int((r.y+r.height)*self.image_scale) )
                cvRectangle( img, pt1, pt2, CV_RGB(255,0,0), 3, 8, 0 )
        cvShowImage( "result", img ) # This isreqd if opencv is rendering... TODO: what if pygame renders?

def main():
   
    input_name = '0'

    if input_name.isdigit():
        capture = cvCreateCameraCapture( int(input_name) )
    else:
        capture = cvCreateFileCapture( input_name )

    cvNamedWindow( "result", 1 )
    
    od = ObjectDetector("eye")
    
    if( capture ):
        frame_copy = None
        while True: 
            frame = cvQueryFrame( capture )
            if( not frame ):
                break;
            if( not frame_copy ):
                frame_copy = cvCreateImage( cvSize(frame.width,frame.height),
                                            IPL_DEPTH_8U, frame.nChannels )
            if( frame.origin == IPL_ORIGIN_TL ):
                cvCopy( frame, frame_copy )
            else:
                cvFlip( frame, frame_copy, 0 )
            
            od.detect_and_draw( frame_copy )

            if( cvWaitKey( 10 ) >= 0 ):
                break;

    else:
        image = cvLoadImage( input_name, 1 )

        if( image ):
        
            detect_and_draw( image )
            cvWaitKey(0)
        
    cvDestroyWindow("result")

if __name__ == '__main__':
    main()
