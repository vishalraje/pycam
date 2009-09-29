/*
 This example has no error checking, it should not be used!

 Should be able to compile with:
 gcc -Wall `pkg-config --cflags opencv` `pkg-config --libs opencv` -o webcamShow webcamShow.c
 Brian Thorne
*/


#include "cv.h"
#include "highgui.h"

int main()
{
    IplImage  *frame;
    CvCapture *capture;
    capture = cvCreateCameraCapture(0);
    cvNamedWindow( "Snapshot", 0 );
    frame = cvQueryFrame( capture );
    cvShowImage( "Snapshot", frame );
    
    cvReleaseCapture( &capture );
    cvWaitKey(10000);   // Wait for 10 seconds, or till key is pressed
    cvDestroyWindow( "Snapshot" );
}
