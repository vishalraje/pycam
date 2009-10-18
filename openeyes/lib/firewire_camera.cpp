/*
 *      firewire_camera.c
 *      
 *      This program is free software; you can redistribute it and/or modify
 *      it under the terms of the GNU General Public License as published by
 *      the Free Software Foundation; either version 2 of the License, or
 *      (at your option) any later version.
 *      
 *      This program is distributed in the hope that it will be useful,
 *      but WITHOUT ANY WARRANTY; without even the implied warranty of
 *      MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 *      GNU General Public License for more details.
 *      
 *      You should have received a copy of the GNU General Public License
 *      along with this program; if not, write to the Free Software
 *      Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
 *      MA 02110-1301, USA.
 */

//----------------------- Firewire Image Capture Code -----------------------//


#include "firewire_camera.h"
#include "colour_conversions.h"

#include <stdio.h>

// Firewire Capture Variables

int firewire_width=640, firewire_height=480;
int dev;
int framerate=30;
FILE* imagefile;

//dc1394_cameracapture cameras[2];
CvCapture *cameras[2];

int numNodes;
int numCameras;

//raw1394handle_t handle;
//nodeid_t * camera_nodes;
//dc1394_feature_set features;

typedef struct {
    int offset_value;
    int value;
    int min;
    int max;
    int available;   
    void (*callback)(int);
} camera_features;

camera_features eye_camera_features[9];


int Get_Height(){return firewire_height;}
int Get_Width(){return firewire_width;}

//int cameramode[2]={MODE_640x480_MONO, MODE_640x480_YUV411};


void FirewireFrame_to_RGBIplImage(void *FirewireFrame, IplImage *OpenCV_image)
{
  uyyvyy2rgb((unsigned char *)FirewireFrame, (unsigned char *)OpenCV_image->imageData, 640*480);
}

IplImage *Get_Raw_Frame(unsigned int cam_index)
{
    return cvRetrieveFrame(cameras[cam_index]);
    //return (char *)cameras[cam_index].capture_buffer;
}

/**
 * Open the two firewire devices.
 * */
void Open_IEEE1394() 
{

    /*
       this requires a working
       video 4 linux (v4l) capture device
       or a linux FireWire (IEEE1394) device
       or a video for windows (wfv) device
       or a Matrox Imaging Library (MIL) device
    */
    CvCapture* cap = cvCaptureFromCAM(0);
    if(!cap) {
        fprintf(stderr, "could not get camera capture device!\n");
        exit(-1);
    }
    
    CvCapture* cap2 = cvCaptureFromCAM(1);
    if(!cap) {
        fprintf(stderr, "could not get second camera capture device!\n");
        exit(1);
    }

    // set frame size
    cvSetCaptureProperty(cap, CV_CAP_PROP_FRAME_WIDTH, 640);
    cvSetCaptureProperty(cap, CV_CAP_PROP_FRAME_HEIGHT, 480);
    
    cvSetCaptureProperty(cap2, CV_CAP_PROP_FRAME_WIDTH, 640);
    cvSetCaptureProperty(cap2, CV_CAP_PROP_FRAME_HEIGHT, 480);
    
    /* Can we figure out which one is black&white etc */
    cameras[0] = cap;
    cameras[1] = cap2;
    
    // Check we can get a frame from each image.
    IplImage* image = cvQueryFrame(cap); // do not release or modify this image...
    if(!image)
    {
        printf("could not get initial image from first camera capture device!\n");
        exit(1);
    }
    
    IplImage* image2 = cvQueryFrame(cap2); // do not release or modify this image...
    if(!image)
    {
        printf("could not get initial image from second camera capture device!\n");
        exit(1);
    }
    
    printf("Cameras Open\n");
  
}

void Grab_IEEE1394() 
{
    cvGrabFrame(cameras[0]);
    cvGrabFrame(cameras[1]);
}

void Release_IEEE1394() 
{
}

void Close_IEEE1394() 
{
  cvReleaseCapture(&cameras[0]);
  cvReleaseCapture(&cameras[1]);
}
