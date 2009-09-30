/*
 * Carry out Gaussian blur on a live webcam stream.
 * 
 * 
 *      Compile with:
 * 
 * g++ -O3 -Wall `pkg-config --cflags opencv` `pkg-config --libs opencv` -o blur blur_opencv.cxx videoCapturePlayer.cxx
 * 
 *  Brian Thorne 2009 <brian.thorne@hitlabnz.org>
 */


#include <iostream>
#include "videoCapturePlayer.h"


/*
 * The gaussian blur function, takes an OpenCV CvMat image,
 * filters it and returns.
 * */
CvMat * gaussianBlur(CvMat *x)
{
    // Filter with gaussian smoothing
    int filterSize = 43;
    cvSmooth(x, x,CV_GAUSSIAN, filterSize, 0, 6.949999999999999);
    return x;
}


/*
 * Test the gaussian blur function on the lena dataset.
 * */
bool test_guassian_blur()
{
    std::cout << "Testing Median Blur C++ function" << std::endl;
    CvMat temp;
    CvMat *i = cvGetMat( cvLoadImage("/usr/share/doc/opencv-doc/examples/c/lena.jpg"), &temp );
    CvMat *blurred_image = gaussianBlur(i);
    cvSaveImage("blurred_imag_cpp_opencv_gaussian.jpg", blurred_image);
    return true;
}

/*
 * If any command line args are given, run the static test, else run
 * live stream demo.
 * */
int main( int argc, char** argv )
{
    if(argc > 1){
        test_guassian_blur();
    } else {
        std::cout << "Starting Gassian Blur C++ demo" << std::endl;
        std::cout << "Press 'q' to exit the program" << std::endl;
        VideoCapturePlayer vcp = VideoCapturePlayer(&gaussianBlur);
        vcp.init(); vcp.main();
    }
    return 0;
}

