/* 
 * This shows a median blur applied to a live webcam stream.
 *     
 *  Brian Thorne 2009 <brian.thorne@canterbury.ac.nz>
 * 
 *  Compile with:
 * 
 *  g++ -O3 -Wall `pkg-config --cflags opencv` `pkg-config --libs opencv` -o median median_opencv.cxx videoCapturePlayer.cxx
 *  
 */


#include <iostream>
#include "videoCapturePlayer.h"

/*
 * The process function that carries out the median blur on a OpenCV CvMat image.
 * Returns the filtered CvMat image.
 * */
CvMat * medianBlur(CvMat *x)
{
    int filterSize = 43;
    cvSmooth(x, x, CV_MEDIAN, filterSize);
    return x;
}

/*
 * Function for testing the static performance of the median blur.
 * You might need to change the path to lena.
 * */
bool test_medianBlur()
{
    std::cout << "Testing Median Blur C++ function" << std::endl;
    CvMat temp;
    CvMat *i = cvGetMat( cvLoadImage("/usr/share/doc/opencv-doc/examples/c/lena.jpg"), &temp );
    CvMat *blurred_image = medianBlur(i);
    cvSaveImage("blurred_imag_cpp_opencv_median.jpg", blurred_image);
    return true;
}

int main( int argc, char** argv )
{
    std::cout << "Median Blur C++ file" << std::endl;
    //test_medianBlur();
    std::cout << "Starting Median Blur C++ Video Capture Demo" << std::endl;
    std::cout << "Press 'q' to exit the program" << std::endl;
    VideoCapturePlayer vcp = VideoCapturePlayer(&medianBlur);
    vcp.init(); vcp.main();
    return 0;
}

