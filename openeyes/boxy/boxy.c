/*
 * Boxy a cvEyetracker demo that prints text on a screen when the 
 * cvEyetracker indicates gaze in that area.
 *
 * Author: Rob Ramsay.
 *
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
 * cvEyeTracker - Version 1.2.5
 * Part of the openEyes ToolKit -- http://hcvl.hci.iastate.edu/openEyes
 * Release Date:
 * Authors : Dongheng Li <dhli@iastate.edu>
 *           Derrick Parkhurst <derrick.parkhurst@hcvl.hci.iastate.edu>
 *           Jason Babcock <babcock@nyu.edu>
 *           David Winfield <dwinfiel@iastate.edu>
 * Copyright (c) 2004-2006
 * All Rights Reserved.
 *
 */

#include <stdio.h>
//#include <stdlib.h>
//#include <signal.h>
//#include <sys/types.h>
//#include <sys/stat.h>
//#include <fcntl.h>
//#include <errno.h>
//#include <unistd.h>
//#include <string.h>
//#include <time.h>
//#include <math.h>
//#include <sys/time.h>

#include "cvEyeTracker.h"
#include "boxy.h"


// Window handles
const char* eye_window = "Eye Image Window";
const char* original_eye_window = "Original Eye Image";
const char* ellipse_window = "Fitted Ellipse Window";
const char* scene_window = "Scene Image Window";
const char* control_window = "Parameter Control Window";



void on_mouse_scene( int event, int x, int y, int flags, void* param )
{

   switch (event) {
     //This is really the left mouse button
     case CV_EVENT_LBUTTONDOWN:
       eyetracker_set_calibration_point(x, y);
       break;
    
     //This is really the right mouse button
     case CV_EVENT_MBUTTONDOWN:
       eyetracker_activate_calibration();
       break;
     
     //This is really the scroll button
     case CV_EVENT_RBUTTONDOWN:
       break;
   }
}


void on_mouse_eye( int event, int x, int y, int flags, void* param )
{
   switch (event) {
     //This is really the left mouse button
     case CV_EVENT_LBUTTONDOWN:
	   eyetracker_set_pupil_search_startpoint(x, y);
       break;
    
     //This is really the right mouse button
     case CV_EVENT_MBUTTONDOWN:
       break;
     
     //This is really the scroll button
     case CV_EVENT_RBUTTONDOWN:
       break;
   }
}




  
void Update_Gui_Windows(	IplImage *eye_image, IplImage *original_eye_image, 
							IplImage *scene_image, IplImage *ellipse_image)
{
  cvShowImage(eye_window, eye_image);
  cvShowImage(original_eye_window, original_eye_image);
  cvShowImage(scene_window, scene_image);
  cvShowImage(ellipse_window, ellipse_image);
  
  cvResizeWindow(eye_window,320,240);
  cvResizeWindow(original_eye_window,320,240);
  cvResizeWindow(ellipse_window,320,240);
  cvResizeWindow(scene_window, 960, 720);
  
  // only OpenCV 0.9.6 has the function of cvMoveWindow(), now we are using version 0.9.5
  /*if (first) {
    cvMoveWindow(eye_window, 200, 0);
    cvMoveWindow(scene_window, 200+320, 0);
    cvMoveWindow(ellipse_window, 200, 240);
    first = 0;
  }*/

  
  // This isn't needed..
  //cvSetTrackbarPos("Edge Threshold", control_window, pupil_edge_thres);
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
  pupil_edge_thres_ptr			= eyetracker_get_pupil_edge_thres_ptr();
  rays_ptr  					= eyetracker_get_rays_ptr(); 
  min_feature_candidates_ptr	= eyetracker_get_min_feature_candidates_ptr();
  cr_window_size_ptr 			= eyetracker_get_cr_window_size_ptr();

  // ??: This should probably be done another way.
  frameh						= eyetracker_get_FRAMEH();

  cvCreateTrackbar("Edge Threshold", control_window, pupil_edge_thres_ptr, 255, NULL );
  cvCreateTrackbar("Rays Number", control_window, rays_ptr, 180, NULL );
  cvCreateTrackbar("Min Feature Candidates", control_window, min_feature_candidates_ptr, 30, NULL );
  cvCreateTrackbar("Corneal Window Size",control_window, cr_window_size_ptr, frameh, NULL );

}



void Close_GUI() 
{
  cvDestroyWindow(eye_window);
  cvDestroyWindow(original_eye_window);
  cvDestroyWindow(ellipse_window);
  cvDestroyWindow(scene_window);
  cvDestroyWindow(control_window);

}


CvPoint averaging_filter(CvPoint point0, CvPoint point1, CvPoint point2) 
{
	CvPoint out;

	long tmp_x = point0.x + point1.x + point2.x;
	long tmp_y = point0.y + point1.y + point2.y;
	out.x = tmp_x / 3;
	out.y = tmp_y / 3;

	return out;
}


CvPoint point_filter(CvPoint point)
{
	static CvPoint point_buff[3];

	point_buff[2] = point_buff[1];
	point_buff[1] = point_buff[0];
	point_buff[0] = point;

	return averaging_filter(point_buff[0], point_buff[1], point_buff[2]);
}


void Draw_Sqaure(IplImage *image, CvRect square, CvScalar color, int line_width)
{
  CvPoint pt1, pt2;

  pt1.x = square.x;
  pt1.y = square.y;
  pt2.x = square.x + square.width;
  pt2.y = square.y + square.height;

  cvRectangle(image, pt1, pt2, color, line_width);
}

int is_point_in_box(CvRect box, CvPoint point) 
{
	if (	box.x <= point.x	&&	point.x <= box.x + box.width &&
			box.y <= point.y	&&	point.y <= box.y + box.height ) {
		return 1;
	} 
	else {
		return 0;
	}
}




int main( int argc, char** argv )
{
  int view_boxes = 0;
  int   view_curser = 0;
  int calc_rslt;
  char c;
  CvFont font;

  CvPoint gaze_target;
  IplImage *eye_im=NULL;
  IplImage *original_eye_im=NULL;
  IplImage *ellipse_im=NULL;
  IplImage *scene_im=NULL;


  eyetracker_setup(argc, argv);

  cvInitFont(&font, CV_FONT_HERSHEY_SIMPLEX, 1, 1, 0, 2, 8);

  Open_GUI();

  while ((c=cvWaitKey(50))!='q') {

    switch (c) {
      case 'b':
		view_boxes = !view_boxes;
		break;
      case 'v':
		view_curser = !view_curser;
		break;
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


    calc_rslt 		= eyetracker_calc_gaze();

  	eye_im			= eyetracker_get_eye_image();
  	original_eye_im	= eyetracker_get_original_eye_image();
  	ellipse_im		= eyetracker_get_ellipse_image();
  	scene_im		= eyetracker_get_scene_image();

	// Addd boxes to the screen.
	if (view_boxes) {
		Draw_Sqaure(scene_im, box1, box1_color, 1);
		Draw_Sqaure(scene_im, box2, box2_color, 1);
		Draw_Sqaure(scene_im, box3, box3_color, 1);
	}
	Draw_Sqaure(scene_im, align_box, align_box_color, 1);


	if (calc_rslt) {
		// If the gaze-calculation was valid print it as a Red cross on the scene
  		gaze_target = eyetracker_get_gaze_target();
  		gaze_target = point_filter(gaze_target);

		if (view_curser)
			Draw_Cross(scene_im, gaze_target.x, gaze_target.y, 60, 60, CV_RGB(255,0,0));

		// Trigger actions if the user is looking inside one of the boxes.
		if (is_point_in_box(box1, gaze_target) ) 
  			cvPutText (scene_im, txt1_txt, txt1_pt, &font, box1_color);
		if (is_point_in_box(box2, gaze_target) ) 
  			cvPutText (scene_im, txt2_txt, txt2_pt, &font, box2_color);
		if (is_point_in_box(box3, gaze_target) ) 
  			cvPutText (scene_im, txt3_txt, txt3_pt, &font, box3_color);
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




