/*
 * Boxy a cvEyetracker demo that prints text on a screen when the 
 * cvEyetracker indicates gaze in that area.
 *
 * Author: Rob Ramsay.
 *
 * boxy is free software; you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation; either version 2 of the License, or
 * (at your option) any later version.
 *
 * boxy is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with boxy; if not, write to the Free Software
 * Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
 *
 *
 * Copyright (c) 2008
 * All Rights Reserved.
 *
 */

#ifdef _CH_
#pragma package <opencv>
#endif

#ifndef _EiC
#include "cv.h"
#include "highgui.h"
#endif


// Files that control where the boxes are on the screen
//
// There are 3 boxes where looking inside will trigger 
// and action, and one big box for alignment.
//


CvScalar align_box_color = CV_RGB(255,0,0);

//const CvRect align_box = cvRect(100, 50, 350, 275);
const CvRect align_box = cvRect(100, 100, 400, 315);


CvScalar box1_color = CV_RGB(0,255,0);
CvScalar box2_color = CV_RGB(0,0,255);
CvScalar box3_color = CV_RGB(255,0,255);

const CvRect box1 = cvRect(100, 50, 133, 150);
const CvRect box2 = cvRect(233, 50, 133, 150);
const CvRect box3 = cvRect(366, 50, 133, 150);

const CvPoint txt1_pt = cvPoint(10, 30);
const CvPoint txt2_pt = cvPoint(250, 30);
const CvPoint txt3_pt = cvPoint(450, 30);

const char *txt1_txt = "Woof";
const char *txt2_txt = "Moo";
const char *txt3_txt = "Oink";




