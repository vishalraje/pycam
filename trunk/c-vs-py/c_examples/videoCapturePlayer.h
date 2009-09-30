/*
 * This is the interface to the VideoCapturePlayer (VCP) written in C++
 * The VCP optionally takes a function pointer to a function that proccess
 * each frame.
 *
 *  Brian Thorne 31/08/09  <brian.thorne@hitlabnz.org>
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
    
    /* Try load a webcam, exits on fail, open an OpenCV display window */
    void init();
    
    /* Run the main loop: capture, process, and display. Times exectution */
    void main();

private:
    /* Pointer to process function */
    CvMat *( *processFunc)(CvMat *);
    
    const bool show;    // Display the output from the process function
    const int device;   // Which camera device to run off
    CvCapture *capture; // The camera capture device
    
    // save a local copy of image in each frame.
    CvMat *mat_frame;
    
    int key;
    int num_frames;
    int64 t_start, t_end;
    float fps;

};
