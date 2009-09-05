/*
 *      blur_opencv.cxx
 *      
 *      Copyright 2009 Brian Thorne <brian.thorne@canterbury.ac.nz>
 * 
 *      Compile with:
 * 
 *   g++ -O3 -Wall `pkg-config --cflags opencv` `pkg-config --libs opencv` -o bg_sub background_subtract_opencv.cxx videoCapturePlayer.cxx
 * 
 *  
 */


#include <iostream>
#include "videoCapturePlayer.h"


CvMat *original;

CvMat * bg_subtract(CvMat *x)
{
    static int n = 0;
    ++n;
    if( n == 3) original = cvCloneMat( x );
    if( n < 4) return x;
    if(n%100 == 0) std::cout << "100 frames" << std::endl;
    
    CvMat * differenceImage  = cvCloneMat( x );
    
    cvAbsDiff( x, original, differenceImage );
    
    
    //CV_THRESH_TOZERO
    CvMat * temp  = cvCloneMat( x );
    cvSetZero(temp);
    cvThreshold( differenceImage, temp, 32, 255, CV_THRESH_BINARY );
    
    
    
    // median filter out the salt & pepper noise in the difference image
    cvSmooth(temp, temp, CV_MEDIAN, 5);
    
    cvSetZero(differenceImage);
    
    cvAnd(x, temp, differenceImage ); // NOTE I CANNOT WORK OUT MASK HERE...
    
    return differenceImage;
}

int main( int argc, char** argv )
{
    std::cout << "Starting Background Subtract C++ demo" << std::endl;
    std::cout << "Press 'q' to exit the program" << std::endl;
    VideoCapturePlayer vcp = VideoCapturePlayer(&bg_subtract);
    vcp.init(); vcp.main();
    return 0;
}

