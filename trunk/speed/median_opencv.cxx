/*
 *      blur_opencv.cxx
 *      
 *      Copyright 2009 Brian Thorne <brian.thorne@canterbury.ac.nz>
 * 
 *      Compile with:
 * 
 * g++ -O3 -Wall `pkg-config --cflags opencv` `pkg-config --libs opencv` -o median median_opencv.cxx videoCapturePlayer.cxx
 *  
 */


#include <iostream>
#include "videoCapturePlayer.h"

CvMat * medianBlur(CvMat *x)
{
    int filterSize = 43;
    cvSmooth(x, x, CV_MEDIAN, filterSize);
    return x;
}

int main( int argc, char** argv )
{
    std::cout << "Starting Median Blur C++ demo" << std::endl;
    std::cout << "Press 'q' to exit the program" << std::endl;
    VideoCapturePlayer vcp = VideoCapturePlayer(&medianBlur);
    vcp.init(); vcp.main();
    return 0;
}

