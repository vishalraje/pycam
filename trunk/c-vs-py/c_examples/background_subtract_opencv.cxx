/*
 *  Carry out a simple background subtraction and show the changes.
 *
 *  Compile with:
 * 
 *  g++ -O3 -Wall `pkg-config --cflags opencv` `pkg-config --libs opencv` -o background_subtract background_subtract_opencv.cxx videoCapturePlayer.cxx
 *   
 *  Brian Thorne 2009 <brian.thorne@hitlabnz.org>
 */

#include <iostream>
#include "videoCapturePlayer.h"

CvMat *original;

/*
 * Takes the first 3 frames and throws them out.
 * Saves the forth frame.
 * Carries out a difference between each frame with this saved original.
 * Thresholds the difference, applies a median filter, blurs the mask
 * then masks the original frame with the changes, so only the changes appear.
 * 
 * */
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
    cvThreshold( differenceImage, temp, 50, 255, CV_THRESH_BINARY );
    
    // Convert the image to one channel
    /* get image properties */
    int width  = x->width; int height = x->height;
    /* create new image for the grayscale version */
    IplImage *gray = cvCreateImage( cvSize( width, height ), IPL_DEPTH_8U, 1 );
    
    cvCvtColor( temp, gray, CV_RGB2GRAY );  
    
    // median filter out the salt & pepper noise in the thresholded difference image
    cvSmooth(gray, gray, CV_MEDIAN, 15);
    
    // Carry out a dilate operation to improve the result
    // but adds a "border" around the object
    //cvDilate(gray, gray, 0, 9);
    cvSmooth(gray, gray, CV_GAUSSIAN, 5);
    
    cvSetZero(differenceImage);
    cvAnd(x, x, differenceImage, gray);
    
    cvReleaseMat(&x);
    cvReleaseImage(&gray);
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

