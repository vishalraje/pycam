/*
 * This VideoCapturePlayer is the code behind all the C/C++ examples.
 * This is the interface to the VideoCapturePlayer (VCP) written in C++
 * The VCP optionally takes a function pointer to a function that proccess
 * each frame.
 * 
 * Brian Thorne <brian.thorne@hitlabnz.org>
*/

//  Example Usage Follows
/*
// This is a template for a function that can be fed into VideoCapturePlayer
// It must take a CvMat, and return a CvMat.
// It draws a rectangle on the screen with OpenCV.
CvMat * drawBox(CvMat *x)
{
    CvPoint pt1, pt2;
    pt1.x = pt1.y = 200;
    pt2.x = pt2.y = 250;
    cvRectangle( x, pt1, pt2, CV_RGB(30,0,200) );
    return x;
}

// An example main function creating a VideoCapturePlayer
// with a process function.
int main( int argc, char** argv )
{
    cout << "Starting VideoCapturePlayer demo" << endl;
    cout << "Press 'q' to exit the program" << endl;
    // With or without a process function:
    //VideoCapturePlayer vcp = VideoCapturePlayer(&drawBox);
    VideoCapturePlayer vcp = VideoCapturePlayer();
    vcp.init();
    vcp.main();
    return 0;
}
*/


#include <string>
#include <iostream>

#include "videoCapturePlayer.h"

#include <stdio.h>  // todo remove printf

#define WINDOW_TITLE "Video Aquisition" 

using namespace std;


VideoCapturePlayer::VideoCapturePlayer( CvMat *( *processFunction)(CvMat *), int device, bool show) 
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
    
    // Check that we can get an image
    for(int i = 100;i;--i)
    {
        IplImage  *frame = cvQueryFrame( capture );
        if(frame) break;
        cout << "couldn't receive image from capture, trying again" << endl;
    }
        
    
    
    if(show){
        /* open the display window */
        cvNamedWindow( WINDOW_TITLE, CV_WINDOW_AUTOSIZE );
    }
    t_setup = cvGetTickCount();
    cout << "Setup time=" << (double)(t_setup-t_begin)/(1000000 * cvGetTickFrequency()) << endl;

    
}

void VideoCapturePlayer::main()
{
    bool timing_now = false;
    
    // start main loop - quit if user press 'q'
    while( (char)key != 'q' )
    {
        // start the clock after the system has been running for a few 
        // frames and has flushed buffers etc...
        if( !timing_now && num_frames > 5){
            num_frames = 0;
            timing_now = true;
            t_start = cvGetTickCount();
        }
        
        // count how many frames we process
        ++num_frames;
        
        // made new scope so frame & temp_mat get cleaned up quickly.
        {
            // get a frame - image should not be released or modified
            IplImage  *frame = cvQueryFrame( capture );
            
            // always check that we received a frame
            if( !frame ){ cout << "Failed to receive image!" << endl; break;}
            
            // cloning the mat instead of the image due to smaller size
            CvMat temp_mat;
            mat_frame = cvCloneMat( cvGetMat( frame, &temp_mat) );
        }
        
        
        
        // Give the CvMat to the supplied external function for processing.
        if (processFunc)
        {
            mat_frame = processFunc(mat_frame);
        }
        
        // display frame
        if(show)
        {
            cvShowImage( WINDOW_TITLE, mat_frame );
        }

        // reveive any key event
        key = cvWaitKey( 5 );
    }
    t_end = cvGetTickCount();
    
    // Post processing
    float tickFreq = cvGetTickFrequency();
    //cout << "Frames captured: " << num_frames << endl;
    //cout << "Running ticks:" << (double)(t_end-t_start) << endl;
    //cout << "tick freq: " << tickFreq << endl;
    float elapsed_time_s = (t_end-t_start)/(1000000 * tickFreq);
    //cout << "Elapsed Time(s): " << elapsed_time_s << endl;
    fps = num_frames/elapsed_time_s;
    cout << "FPS: " << fps << endl;
}


