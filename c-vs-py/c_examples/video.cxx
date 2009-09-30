/*
 *  A webcam streamer using the VideoCapturePlayer class.
 * 
 *  Compile with:
 * 
 *  g++ -O3 -Wall `pkg-config --cflags opencv` `pkg-config --libs opencv` -o VCP video.cxx videoCapturePlayer.cxx
 * 
 *  Brian Thorne 2009 <brian.thorne@hitlabnz.org>
 */


#include <iostream>
#include "videoCapturePlayer.h"

int main( int argc, char** argv )
{
    std::cout << "Starting Video Capture C++ demo" << std::endl;
    std::cout << "Press 'q' to exit the program" << std::endl;
    VideoCapturePlayer vcp = VideoCapturePlayer();
    
    vcp.init();     // Start the camera, create the windows etc.
    vcp.main();     // Start the program running.
    
    return 0;
}

