#!/usr/bin/env python
"""
Shows the simplest possible way of showing a single frame using OpenCV

Note: This example has no error checking, it should not be used!

Brian Thorne 2009 <brian.thorne@hitlabnz.org>
"""


from opencv import highgui as hg

capture = hg.cvCreateCameraCapture(0)
hg.cvNamedWindow( "Snapshot")
frame = hg.cvQueryFrame( capture )
hg.cvShowImage( "Snapshot", frame )

hg.cvWaitKey(10000) # Wait for timeout or input
