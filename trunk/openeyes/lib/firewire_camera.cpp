/*
 *      firewire_camera.c
 *      
 *      Copyright 2009 Brian Thorne <brian@brian-hitlab>
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
dc1394_cameracapture cameras[2];
int numNodes;
int numCameras;
raw1394handle_t handle;
nodeid_t * camera_nodes;
dc1394_feature_set features;

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

int cameramode[2]={MODE_640x480_MONO,MODE_640x480_YUV411};

void FirewireFrame_to_RGBIplImage(void *FirewireFrame, IplImage *OpenCV_image)
{
  uyyvyy2rgb((unsigned char *)FirewireFrame, (unsigned char *)OpenCV_image->imageData, 640*480);
}

char *Get_Raw_Frame(unsigned int cam_index)
{
    return (char *)cameras[cam_index].capture_buffer;
}

void Open_IEEE1394() 
{
  int i;

  /* This section will have to be changed when moving from libdc1394 1.X API to 2.X */
  handle = dc1394_create_handle(0);
  if (handle==NULL) {
    fprintf( stderr, "Unable to aquire a raw1394 handle\n\n"
	"Please check \n"
	"  - if the kernel modules `ieee1394',`raw1394' and `ohci1394' are loaded \n"
	"  - if you have read/write access to /dev/raw1394\n\n");
    exit(1);
  }

  numNodes = raw1394_get_nodecount(handle);
  camera_nodes = dc1394_get_camera_nodes(handle,&numCameras,1);
  fflush(stdout);
  if (numCameras<1) {
    fprintf( stderr, "no cameras found :(\n");
    dc1394_destroy_handle(handle);
    exit(1);
  }

  for (i = 0; i < numCameras; i++) {
    dc1394_camera_on(handle, camera_nodes[i]);

    if (dc1394_dma_setup_capture(handle,camera_nodes[i],
			i, /* channel */ 
			FORMAT_VGA_NONCOMPRESSED,
			cameramode[i],
			SPEED_400,
			FRAMERATE_30,40,1,"/dev/video1394-0",
			&cameras[i])!=DC1394_SUCCESS) {
      fprintf( stderr,"unable to setup camera\n");
      dc1394_release_camera(handle,&cameras[i]);
      dc1394_destroy_handle(handle);
      exit(1);
    }
    if (dc1394_start_iso_transmission(handle,cameras[i].node) !=DC1394_SUCCESS) {
      fprintf( stderr, "unable to start camera iso transmission\n");
      dc1394_release_camera(handle,&cameras[i]);
      dc1394_destroy_handle(handle);
      exit(1);
    }
    printf("Camera %d Open\n",i);
  }
}

void Grab_IEEE1394() 
{
  if (dc1394_dma_multi_capture(cameras, numCameras)!=DC1394_SUCCESS) {
    fprintf( stderr, "unable to capture a frame\n");
  }
}

void Release_IEEE1394() 
{
  int i;

  for (i=0; i<numCameras; i++) {
    dc1394_dma_done_with_buffer(&cameras[i]);
  }
}

void Close_IEEE1394() 
{
  int i;

  for (i=0; i<numCameras; i++) {
    if (dc1394_stop_iso_transmission(handle,cameras[i].node)!=DC1394_SUCCESS) {
      printf("couldn't stop the camera?\n");
    }
    dc1394_camera_off(handle, cameras[i].node); 
    dc1394_dma_release_camera(handle,&cameras[i]);
  }
  dc1394_destroy_handle(handle);
}
