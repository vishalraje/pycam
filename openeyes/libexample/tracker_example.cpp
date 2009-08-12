/*
 * cvEyeTracker is free software; you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation; either version 2 of the License, or
 * (at your option) any later version.
 *
 * cvEyeTracker is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with cvEyeTracker; if not, write to the Free Software
 * Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
 *
 *
 * Example program using the openEyes Library
 * 
 *
 */

#include <stdio.h>
#include "cvEyeTracker.h"


#ifdef _CH_
#pragma package <opencv>
#endif

#ifndef _EiC
#include "cv.h"
#include "highgui.h"
#endif


// Window handles
const char* eye_window = "Eye Image Window";
const char* original_eye_window = "Original Eye Image";
const char* ellipse_window = "Fitted Ellipse Window";
const char* scene_window = "Scene Image Window";
const char* control_window = "Parameter Control Window";


/*
 * The mouse scene image is the main input and output of this program.
 * To calibrate the eyetracker, 9 points must be registered with the left
 * mouse button in this window. To activate the calibration, click the right
 * mouse button.
 */
void on_mouse_scene( int event, int x, int y, int flags, void* param )
{
	switch (event) {
    	case CV_EVENT_LBUTTONDOWN:
       		eyetracker_set_calibration_point(x, y);
       		break;
     
     	case CV_EVENT_RBUTTONDOWN:
       		eyetracker_activate_calibration();
       		break;
   	}
}

/*   
 * If the mouse is clicked in the eye image, use that point at a starting point
 * for the pupil search.
 */
void on_mouse_eye( int event, int x, int y, int flags, void* param )
{
  	switch (event) {
    	case CV_EVENT_LBUTTONDOWN:
	    	eyetracker_set_pupil_search_startpoint(x, y);
      		break;
   	}
}


void Update_Gui_Windows( IplImage *eye_image, IplImage *original_eye_image, IplImage *scene_image, IplImage *ellipse_image)
{
	cvShowImage(eye_window, eye_image);
	cvShowImage(original_eye_window, original_eye_image);
	cvShowImage(scene_window, scene_image);
	cvShowImage(ellipse_window, ellipse_image);

	cvResizeWindow(eye_window,320,240);
	cvResizeWindow(original_eye_window,320,240);
	cvResizeWindow(ellipse_window,320,240);
}

void Open_GUI()
{
	int *pupil_edge_thres_ptr;
	int *rays_ptr;
	int *min_feature_candidates_ptr;
	int *cr_window_size_ptr;
	int frameh;

	//Create the windows
	cvNamedWindow(control_window, 1);
	cvNamedWindow(ellipse_window, 0);
	cvNamedWindow(scene_window, 0);
	cvNamedWindow(eye_window, 0);
	cvNamedWindow(original_eye_window, 0);

	//setup the mouse call back funtion here for calibration    
	cvSetMouseCallback(scene_window, on_mouse_scene, 0);        
	cvSetMouseCallback(eye_window, on_mouse_eye, 0);        

	// Setup the paramater-sliders, in the control window.
	pupil_edge_thres_ptr = eyetracker_get_pupil_edge_thres_ptr();
	rays_ptr = eyetracker_get_rays_ptr();
	min_feature_candidates_ptr = eyetracker_get_min_feature_candidates_ptr();
	cr_window_size_ptr = eyetracker_get_cr_window_size_ptr();

	// ??: This should probably be done another way.
	frameh = eyetracker_get_FRAMEH();

	cvCreateTrackbar("Edge Threshold", control_window, pupil_edge_thres_ptr, 255, NULL );
	cvCreateTrackbar("Rays Number", control_window, rays_ptr, 180, NULL );
	cvCreateTrackbar("Min Feature Candidates", control_window, min_feature_candidates_ptr, 30, NULL );
	cvCreateTrackbar("Corneal Window Size", control_window, cr_window_size_ptr, frameh, NULL );

}

void Close_GUI() 
{
	cvDestroyWindow(eye_window);
	cvDestroyWindow(original_eye_window);
	cvDestroyWindow(ellipse_window);
	cvDestroyWindow(scene_window);
	cvDestroyWindow(control_window);
}

int main( int argc, char** argv )
{
	int calc_rslt;
	char c;

	CvPoint gaze_target;
	IplImage *eye_im=NULL;
	IplImage *original_eye_im=NULL;
	IplImage *ellipse_im=NULL;
	IplImage *scene_im=NULL;

	eyetracker_setup(argc, argv);

	Open_GUI();

	/* Enter main event loop. */
	while ((c=cvWaitKey(50))!='q') 
	{
		switch (c) {
			case 's':
				eyetracker_save_eye_and_scene_images();
				break;
			case 'c':
				eyetracker_save_image();
				break;
			case 'e':
				eyetracker_save_ellipse();
				break;
		}


		calc_rslt = eyetracker_calc_gaze();

		eye_im = eyetracker_get_eye_image();
		original_eye_im	= eyetracker_get_original_eye_image();
		ellipse_im = eyetracker_get_ellipse_image();
		scene_im = eyetracker_get_scene_image();

		// If the gaze-calculation was valid print it as a Red cross on the scene.
		if (calc_rslt) {
			gaze_target = eyetracker_get_gaze_target();
			Draw_Cross(scene_im, gaze_target.x, gaze_target.y, 60, 60, CV_RGB(255,0,0));
		}

		Update_Gui_Windows(eye_im, original_eye_im, scene_im, ellipse_im);

	}

	Close_GUI();

	eyetracker_cleanup();

	return 0;
}

#ifdef _EiC
main(1,"cvEyeTracker.c");
#endif




