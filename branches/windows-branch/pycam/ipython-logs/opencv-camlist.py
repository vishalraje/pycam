#log# Automatic Logger file. *** THIS MUST BE THE FIRST LINE ***
#log# DO NOT CHANGE THIS LINE OR THE TWO BELOW
#log# opts = Struct({'__allownew': True, 'logfile': 'ipython-logs/opencv-camlist.py'})
#log# args = []
#log# It is safe to make manual edits below here.
#log#-----------------------------------------------------------------------
import opencv
import opencv.cv as cv
import opencv.highgui as hg
import conversionUtils
# on the olpc this takes ages!
cap = hg.cvCreateCameraCapture(0)

cap
#?cap
q = hg.cvQueryFrame(cap)
del cap
#cam still on
hg.cvReleaseCapture(2)
hg.cvReleaseCapture(cap)
#bugger
quit()
