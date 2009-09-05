#!/usr/bin/env python

"""
Load, Filter then Show an image with opencv in python
Brian Thorne 2009
"""

from VideoCapturePlayer import VideoCapturePlayer as VCP
import numpy
from scipy.ndimage import gaussian_filter,maximum_filter
from numpy import array,ones,zeros,nonzero
from opencv import cv

import sys

# import the necessary things for OpenCV
from opencv import cv
from opencv import highgui

#############################################################################
# some "constants"

win_size = 10
MAX_COUNT = 500

#############################################################################
# some "global" variables

image = None
pt = None
add_remove_pt = False
flags = 0
night_mode = False
need_to_init = False
# the default parameters
quality = 0.01
min_distance = 10



def harrisResponse(frame):
    """pyvision/point/DetectorHarris.py
    Runs at 10.5 fps...
    """
    #gray = cv.cvCreateImage( cv.cvGetSize(image), 8, 1 )
    #corners = cv.cvCreateImage( cv.cvGetSize(image), 32, 1 )
    #cv.cvCvtColor( image, gray, cv.CV_BGR2GRAY )

    #cv.cvCornerHarris(gray,corners,15)
    
    # This could be done in a persistant way
    # create the images we need
    image = cv.cvCreateImage (cv.cvGetSize (frame), 8, 3)
    grey = cv.cvCreateImage (cv.cvGetSize (frame), 8, 1)
    prev_grey = cv.cvCreateImage (cv.cvGetSize (frame), 8, 1)
    pyramid = cv.cvCreateImage (cv.cvGetSize (frame), 8, 1)
    prev_pyramid = cv.cvCreateImage (cv.cvGetSize (frame), 8, 1)
    eig = cv.cvCreateImage (cv.cvGetSize (frame), cv.IPL_DEPTH_32F, 1)
    temp = cv.cvCreateImage (cv.cvGetSize (frame), cv.IPL_DEPTH_32F, 1)
    points = [[], []]

    # copy the frame, so we can draw on it
    cv.cvCopy (frame, image)

    # create a grey version of the image
    cv.cvCvtColor (image, grey, cv.CV_BGR2GRAY)

        
    # search the good points
    points [1] = cv.cvGoodFeaturesToTrack (
        grey, eig, temp,
        MAX_COUNT,
        quality, min_distance, None, 3, 0, 0.04)
    
    # refine the corner locations
    cv.cvFindCornerSubPix (
        grey,
        points [1],
        cv.cvSize (win_size, win_size), cv.cvSize (-1, -1),
        cv.cvTermCriteria (cv.CV_TERMCRIT_ITER | cv.CV_TERMCRIT_EPS,
                           20, 0.03))
                                           
    if len (points [0]) > 0:
        # we have points, so display them

        # calculate the optical flow
        [points [1], status], something = cv.cvCalcOpticalFlowPyrLK (
            prev_grey, grey, prev_pyramid, pyramid,
            points [0], len (points [0]),
            (win_size, win_size), 3,
            len (points [0]),
            None,
            cv.cvTermCriteria (cv.CV_TERMCRIT_ITER|cv.CV_TERMCRIT_EPS,
                               20, 0.03),
            flags)
        
        # initializations
        point_counter = -1
        new_points = []
        
        for the_point in points [1]:
            # go trough all the points

            # increment the counter
            point_counter += 1
            
            if add_remove_pt:
                # we have a point to add, so see if it is close to
                # another one. If yes, don't use it
                dx = pt.x - the_point.x
                dy = pt.y - the_point.y
                if dx * dx + dy * dy <= 25:
                    # too close
                    add_remove_pt = 0
                    continue

            if not status [point_counter]:
                # we will disable this point
                continue

            # this point is a correct point
            new_points.append (the_point)

            # draw the current point
            cv.cvCircle (image,
                         cv.cvPointFrom32f(the_point),
                         3, cv.cvScalar (0, 255, 0, 0),
                         -1, 8, 0)

        # set back the points we keep
        points [1] = new_points
        
    

    # swapping
    prev_grey, grey = grey, prev_grey
    prev_pyramid, pyramid = pyramid, prev_pyramid
    points [0], points [1] = points [1], points [0]


    return image

if __name__ == "__main__":
    title = "Harris Feature Detection"
    VCP(harrisResponse, title).main()
