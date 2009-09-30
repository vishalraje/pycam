/*
 * This is a standalone video capture and display loop with error checking.
 * 
 * Should be able to compile with:
 *  g++ -Wall `pkg-config --cflags opencv` `pkg-config --libs opencv` -o videoShow videoShow.c
 * 
 * Pass a video file as first arg, or it will try webcam.
 * 
 * Brian Thorne 2009 <brian.thorne@hitlabnz.org>
*/

#include <stdio.h>
#include "cv.h"
#include "highgui.h"

#define WINDOW_TITLE "Video Aquisition" 

int main( int argc, char** argv )
{
    IplImage  *frame;
    int key;
    CvCapture *capture;
    
    if( argc == 2 )
    {
      /* load the AVI file */
      capture = cvCaptureFromAVI( argv[1] );   

    } else {
      /* Try load a webcam */
      capture = cvCreateCameraCapture(0);
    }
    
    /* always check */
    if( !capture ) return 1;    

    /* get fps, needed to set the delay */
    int fps = ( int )cvGetCaptureProperty( capture, CV_CAP_PROP_FPS );
    //fps /= 2;
    
    /* set the camera height and width */
    cvSetCaptureProperty(capture, CV_CAP_PROP_FRAME_WIDTH, 320);
    cvSetCaptureProperty(capture, CV_CAP_PROP_FRAME_HEIGHT, 240);
    
    /* open the display window */
    cvNamedWindow( WINDOW_TITLE, CV_WINDOW_AUTOSIZE );
    
    while( (char) key != 'q' ) {
        
        /* get a frame */
        frame = cvQueryFrame( capture );
       
        /* always check */
        if( !frame ) break;
   
        /* display frame */
        cvShowImage( WINDOW_TITLE, frame );

        /* quit if user press 'q' */
        key = cvWaitKey( 5 );
    }
   
    /* free memory */
    cvReleaseCapture( &capture );
    cvDestroyWindow( WINDOW_TITLE );
    return 0;
}
