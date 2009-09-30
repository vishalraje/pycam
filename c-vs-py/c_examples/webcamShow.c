/*
 * This code is a simple snapshot display program.
 * It connects to a webcam, takes an image, and displays it using OpenCV.
 * 
 *  This example has no error checking, it should not be used in practise!
 *  
 * Compile with:
 *  g++ -Wall `pkg-config --cflags opencv` `pkg-config --libs opencv` -o webcamShow webcamShow.c
 * 
 *  Brian Thorne 2009 <brian.thorne@hitlabnz.org>
 * 
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
    return 0;
}
