/*
 *      blur_opencv.cxx
 *      
 *      Copyright 2009 Brian Thorne <brian.thorne@canterbury.ac.nz>
 * 
 *      Compile with:
 * 
 * g++ -Wall `pkg-config --cflags opencv` `pkg-config --libs opencv` -o blur blur_opencv.cxx videoCapturePlayer.cxx
 *  
 */


#include <iostream>
#include "videoCapturePlayer.h"

CvMat * gaussianBlur(CvMat *x)
{
    // Filter with gaussian smoothing
    int filterSize = 43;
    cvSmooth(x, x, CV_GAUSSIAN, filterSize);
    return x;
}

int main( int argc, char** argv )
{
    std::cout << "Starting Gassian Blur C++ demo" << std::endl;
    std::cout << "Press 'q' to exit the program" << std::endl;
    VideoCapturePlayer vcp = VideoCapturePlayer(&gaussianBlur);
    vcp.init(); vcp.main();
    return 0;
}

