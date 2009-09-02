// display the difference between adjacent frames (press any key to exit)
// g++ -Wall --pedantic `pkg-config --cflags opencv` `pkg-config --libs opencv` -o diff diff.c
#include "highgui.h"
#include "cv.h"

//#pragma comment(lib, "cxcore.lib")

#define r(j) differenceImage->imageData[j+2] // red pixel in difference image
#define g(j) differenceImage->imageData[j+1] // green pixel in difference image
#define b(j) differenceImage->imageData[j]    // blue pixel in difference image

int main()
{
    CvCapture* capture         = cvCreateCameraCapture(0);    // connect to a camera
    IplImage* image            = cvQueryFrame(capture);       // get the first frame of video
    IplImage* previousFrame    = cvCloneImage( image );       // allocate image buffer for previous frame
    IplImage* differenceImage  = cvCloneImage( image );       // allocate image buffer for difference image
    cvNamedWindow("difference images",  CV_WINDOW_AUTOSIZE);                    // title display window
    while (cvWaitKey(10) < 0)
    {
        cvCopy( image, previousFrame );                       // backup current frame
        image = cvQueryFrame(capture);                        // get the next frame of video
        cvAbsDiff( image, previousFrame, differenceImage );   // diff current frame with previous frame
        
        cvThreshold( differenceImage, differenceImage, 32, 0, CV_THRESH_TOZERO );//threshold difference image
        
        for(int i=0; i<image->imageSize; i+=3)              // highlight all remaining difference pixels
             if (r(i)||g(i)||b(i)) r(i)=g(i)=b(i)=255;      // turn off for real pixels from diff image
        
        // median filter out the salt & pepper noise in the difference image
        cvSmooth(differenceImage, differenceImage, CV_MEDIAN, 5);
        
        // Filter with gaussian
        cvSmooth(differenceImage, differenceImage, CV_GAUSSIAN, 3);
        
        //cvErode(differenceImage, differenceImage,NULL, 5);
        
        cvShowImage("difference images", differenceImage);    // display highlighted difference image
    }
    cvReleaseCapture( &capture );
    return 0;
}

