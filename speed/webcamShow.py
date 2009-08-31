"""
 This example has no error checking, it should not be used!

 Brian Thorne
"""


from opencv import highgui as hg


capture = hg.cvCreateCameraCapture(0)
hg.cvNamedWindow( "Snapshot")
frame = hg.cvQueryFrame( capture )
hg.cvShowImage( "Snapshot", frame )
