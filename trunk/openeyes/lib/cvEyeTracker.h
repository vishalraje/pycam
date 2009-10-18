/*
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

#ifndef CVEYETRACKER
#define CVEYETRACKER

//#ifdef _CH_
//#pragma package <opencv>
//#endif

//#ifndef _EiC

#include <cv.h>
#include <cxcore.h>
#include <highgui.h>

//#endif



// Function summary: 
//
//		void Draw_Cross(IplImage *image, int centerx, int centery, int x_cross_length, int y_cross_length, CvScalar color);
//
//		void eyetracker_set_calibration_point(int x, int y);
//		void eyetracker_activate_calibration();
//		void eyetracker_set_pupil_search_startpoint(int x, int y);
//
//		void eyetracker_save_eye_and_scene_images(void);
//		void eyetracker_save_image(void);
//		void eyetracker_save_ellipse(void);
//
//		int eyetracker_calc_gaze(void);
//		CvPoint eyetracker_get_gaze_target(void);
//
//		void eyetracker_setup(int argc, char **argv);
//		void eyetracker_cleanup(void);
//		void eyetracker_setup_image_buffs(void);
//		void eyetracker_cleanup_image_buffs(void);
//
//		IplImage * eyetracker_get_eye_image(void);
//		IplImage * eyetracker_get_original_eye_image(void);
//		IplImage * eyetracker_get_ellipse_image(void);
//		IplImage * eyetracker_get_scene_image(void);
//
//		int * eyetracker_get_pupil_edge_thres_ptr(void);
//		int * eyetracker_get_rays_ptr(void);
//		int * eyetracker_get_min_feature_candidates_ptr(void);
//		int * eyetracker_get_cr_window_size_ptr(void);
//
//		int eyetracker_get_FRAMEH(void);
//



void Draw_Cross(IplImage *image, int centerx, int centery, int x_cross_length, int y_cross_length, CvScalar color);


// Register a calibration point (9 are needed), which is a
// point on the scene that the user is looking at, at this 
// instant.
void eyetracker_set_calibration_point(int x, int y);

// Calibrate the Eye tracker once all 9 points have been 
// registered with eyetracker_set_calibration_point().
void eyetracker_activate_calibration();

void eyetracker_set_pupil_search_startpoint(int x, int y);


void eyetracker_save_eye_and_scene_images(void);

void eyetracker_save_image(void);

void eyetracker_save_ellipse(void);




// Returns true/false
int eyetracker_calc_gaze(void);


CvPoint eyetracker_get_gaze_target(void);

// Code removed from the main function, when this was rewritten
// as a lib system. 
void eyetracker_setup(int argc, char **argv);

// Code removed from the main function (when this was rewritten
// as a lib system).
void eyetracker_cleanup(void);

//  Close_Ellipse_Log();
void eyetracker_setup_image_buffs(void);

void eyetracker_cleanup_image_buffs(void);



IplImage * eyetracker_get_eye_image(void);

IplImage * eyetracker_get_original_eye_image(void);

IplImage * eyetracker_get_ellipse_image(void);

IplImage * eyetracker_get_scene_image(void);



int * eyetracker_get_pupil_edge_thres_ptr(void);

int * eyetracker_get_rays_ptr(void);

int * eyetracker_get_min_feature_candidates_ptr(void);

int * eyetracker_get_cr_window_size_ptr(void);



int eyetracker_get_FRAMEH(void);

#endif //CVEYETRACKER
