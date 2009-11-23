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


#include "openEyesCameraReader.h"
#include "colour_conversions.h"

#include <stdio.h>
#include <libraw1394/raw1394.h>
#include <libdc1394/dc1394_control.h>



/* ---- Local Functions ---- */

static void setup_image_buffs(void);
static void cleanup_image_buffs(void);


/* ---- Local Variables ---- */

// Buffers for the images. One for each camera.
IplImage *cam0_image;
IplImage *cam1_image;

int firewire_width=640, firewire_height=480;
int firewire_frame_size = firewire_width * firewire_height;

dc1394_cameracapture cameras[2];

int numNodes;
int numCameras;

raw1394handle_t handle;
nodeid_t *camera_nodes;



int cameramode[2]={MODE_640x480_MONO, MODE_640x480_YUV411};



/* ---- Functions ---- */

int Get_Height()
{
	return firewire_height;
}


int Get_Width()
{
	return firewire_width;
}


void FirewireFrame_to_RGBIplImage(void *FirewireFrame, IplImage *OpenCV_image)
{
  uyyvyy2rgb((unsigned char *)FirewireFrame, (unsigned char *)OpenCV_image->imageData, firewire_width*firewire_height);
}


// Returns pointer to image buffer on success otherwise NULL.
// The buffer will be valid untill it is overwritten by the next Get_Raw_Frame() call with 
// same cam_index value.
IplImage *Get_Raw_Frame(unsigned int cam_index)
{
	if (cam_index == 0) 
	{
 		memcpy(cam0_image->imageData,(char *)cameras[cam_index].capture_buffer, firewire_frame_size);
    	return cam0_image;
	}
	else if (cam_index == 1) 
	{
	 	FirewireFrame_to_RGBIplImage( (unsigned char *)cameras[1].capture_buffer, cam1_image);
    	return cam1_image;
	}
	else 
	{
		return NULL;	// Error
	}

}


/**
 * Open the two firewire devices.
 * */
void Open_IEEE1394() 
{
	int i;

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
		fprintf( stderr, "No cameras found :(\n");
		dc1394_destroy_handle(handle);
		exit(1);
	}
	else if (numCameras==1) {
		fprintf( stderr, "Only 1 camera found. 2 are needed.\n");
		exit(1);
 	}

	for (i = 0; i < numCameras; i++) {
		dc1394_camera_on(handle, camera_nodes[i]);

		if (dc1394_dma_setup_capture(handle,camera_nodes[i],
			i, /* channel */ 
			FORMAT_VGA_NONCOMPRESSED,
			cameramode[i],
			SPEED_400,
			FRAMERATE_30,40,1,"/dev/video1394/0",
			&cameras[i]) != DC1394_SUCCESS) 
		{
			fprintf( stderr,"Unable to setup camera\n");
			dc1394_release_camera(handle,&cameras[i]);
			dc1394_destroy_handle(handle);
			exit(1);
		}

		if (dc1394_start_iso_transmission(handle,cameras[i].node) !=DC1394_SUCCESS) 
		{
			fprintf( stderr, "Unable to start camera iso transmission\n");
			dc1394_release_camera(handle,&cameras[i]);
			dc1394_destroy_handle(handle);
			exit(1);
		}
		printf("Camera %d Open\n",i);
	}
	

	setup_image_buffs();

}


void Grab_IEEE1394() 
{
	if (dc1394_dma_multi_capture(cameras, numCameras) != DC1394_SUCCESS) 
		fprintf( stderr, "unable to capture a frame\n");
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

	for (i=0; i<numCameras; i++) 
	{
		if (dc1394_stop_iso_transmission(handle,cameras[i].node) != DC1394_SUCCESS)
			printf("couldn't stop the camera?\n");

		dc1394_camera_off(handle, cameras[i].node); 
		dc1394_dma_release_camera(handle,&cameras[i]);
	}

	dc1394_destroy_handle(handle);


	cleanup_image_buffs();
}


// Allocate the buffers used to return camera images.
static void setup_image_buffs(void)
{
	//Camera one records the eye and is monochrome.
	cam0_image=cvCreateImageHeader(cvSize(firewire_width,firewire_height), 8, 1 );
	cam0_image->imageData=(char *)malloc(firewire_width*firewire_height);
	
	//Camera two records the scene and is RGB.
	cam1_image=cvCreateImageHeader(cvSize(firewire_width,firewire_height), 8, 3 );
	cam1_image->imageData=(char *)malloc(firewire_width*firewire_height*3);
}


// Cleanup the buffers used to return camera images.
void cleanup_image_buffs(void)
{
	cvReleaseImage(&cam0_image);
	cvReleaseImage(&cam1_image);

//	cvReleaseImageHeader(&cam0_image );
//	cvReleaseImageHeader(&cam1_image );
}



