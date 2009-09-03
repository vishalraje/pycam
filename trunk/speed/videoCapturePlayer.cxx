/*
Should be able to compile by uncommenting the main function at the bottom and using:
g++ -Wall `pkg-config --cflags opencv` `pkg-config --libs opencv` -o VCP videoCapturePlayer.cxx
*/

#include <string>
#include <iostream>

#include "videoCapturePlayer.h"

#include <stdio.h>  // todo remove printf

#define WINDOW_TITLE "Video Aquisition" 

using namespace std;


VideoCapturePlayer::VideoCapturePlayer( CvMat *( *processFunction)(CvMat *), int device, bool show ) 
:show(show), device(device), num_frames(0)
{
    processFunc = processFunction;
}
    
VideoCapturePlayer::~VideoCapturePlayer()
{
    /* free memory */
    cvReleaseCapture( &capture );
    cvDestroyWindow( WINDOW_TITLE );
}

void VideoCapturePlayer::init()
{
    int64 t_begin = cvGetTickCount(),t_setup;
    
    /* Try load a webcam */
    capture = cvCreateCameraCapture(device);
    
    /* always check that this worked! */
    if( !capture ){ 
        cout << "Couldn't create camera capture" << endl; 
    }
    
    /* get fps, needed to set the delay */
    //fps = ( int )cvGetCaptureProperty( capture, CV_CAP_PROP_FPS );
    //fps /= 2;
    
    
    if(show){
        /* open the display window */
        cvNamedWindow( WINDOW_TITLE, CV_WINDOW_AUTOSIZE );
    }
    t_setup = cvGetTickCount();
    cout << "Setup time=" << (double)(t_setup-t_begin) << endl;

    
}

void VideoCapturePlayer::main()
{
    t_start = cvGetTickCount();
    while( (char)key != 'q' )
    {
        /* get a frame - image should not be released or modified*/
        frame = cvQueryFrame( capture );
        
        /* Convert to a CvMat*/
        {
            CvMat temp_mat;
            mat_frame = cvGetMat( frame, &temp_mat);
        }
        
        /* always check */
        if( !frame ){ cout << "No frame!" << endl; break;}
        
        if (processFunc)
        {
            mat_frame = processFunc(mat_frame);
        }
        
        /* display frame */
        if(show)
        {
            cvShowImage( WINDOW_TITLE, mat_frame );
        }
        ++num_frames;
        /* quit if user press 'q' */
        key = cvWaitKey( 5 );
    }
    t_end = cvGetTickCount();
    float tickFreq = cvGetTickFrequency();
    //cout << "Frames captured: " << num_frames << endl;
    //cout << "Running ticks:" << (double)(t_end-t_start) << endl;
    //cout << "tick freq: " << tickFreq << endl;
    float elapsed_time_s = (t_end-t_start)/(1000000 * tickFreq);
    //cout << "Elapsed Time(s): " << elapsed_time_s << endl;
    fps = num_frames/elapsed_time_s;
    cout << "FPS: " << fps << endl;
}

//  Example Usage Follows

/**
 * This is a template for a function that can be fed into VideoCapturePlayer
 * It must take a CvMat, and return a CvMat.
 * It draws a rectangle on the screen.
 */
CvMat * doNothing(CvMat *x)
{
    ///*
    CvPoint pt1, pt2;
    pt1.x = pt1.y = 200;
    pt2.x = pt2.y = 250;
    
    cvRectangle( x, pt1, pt2, CV_RGB(30,0,200) );
    //*/
    return x;
}
/*
int main( int argc, char** argv )
{
    cout << "Starting VideoCapturePlayer demo" << endl;
    cout << "Press 'q' to exit the program" << endl;
    VideoCapturePlayer vcp = VideoCapturePlayer(&doNothing);
    //VideoCapturePlayer vcp = VideoCapturePlayer();
    vcp.init();
    vcp.main();
    
    return 0;
}
*/
