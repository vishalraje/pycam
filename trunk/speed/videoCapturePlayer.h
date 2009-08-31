/*
 *  videoCapturePlayer.h
 *
 *  Created by Brian Thorne on 31/08/09.
 *  Copyright 2009 All rights reserved.
 *
 */

#include "cv.h"
#include "highgui.h"

#define WINDOW_TITLE "Video Aquisition" 

class VideoCapturePlayer
{
public:
    /* 
      A video capture player takes a pointer to a function 
      that may do something with an image, returning the possibly altered image 
    */
    VideoCapturePlayer( CvMat *( *processFunction)(CvMat *)=0, int device=0, bool show=true );
    
    ~VideoCapturePlayer();
    
    /* Try load a webcam, exits on fail, open the display window */
    void init();
    
    /* Run the main capture, process, display loop */
    void main();

private:
    /* Pointer to process function */
    CvMat *( *processFunc)(CvMat *);
    
    const bool show;    // Display the output from the process function
    const int device;   // Which camera device to run off
    CvCapture *capture; // The camera capture device
    
    // two types of image formats for each frame.
    IplImage  *frame;
    CvMat *mat_frame;
    
    int key;
    int fps;
        
};