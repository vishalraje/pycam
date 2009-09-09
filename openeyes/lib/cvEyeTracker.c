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

#include <stdio.h>
#include <stdlib.h>
#include <signal.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <errno.h>
#include <unistd.h>
#include <linux/videodev.h>
#include <sys/ioctl.h>
#include <string.h>
#include <sys/mman.h>
#include <time.h>
#include <math.h>
#include <sys/time.h>
#include <libraw1394/raw1394.h>
#include <libdc1394/dc1394_control.h>


#include "remove_corneal_reflection.h"
#include "ransac_ellipse.h"
#include "timing.h"
#include "svd.h"
#include "colour_conversions.h"

//#ifdef _CH_
//#pragma package <opencv>
//#endif
//
//#ifndef _EiC
//#include "cv.h"
//#include "highgui.h"
//#endif


#include "cvEyeTracker.h"


#define UINT8 unsigned char

#ifndef PI
#define PI 3.141592653589
#endif

#define DEBUG 1

FILE *calfile;
#define CAL(args...) fprintf(logfile,args);

#define INFO(args...) if (DEBUG) {printf(args) ; CAL(args)}

#define CLIP(x,l,u) ((x)<(l)?((l)):((x)>(u)?(u):(x)))
#define ISIN(x,l,u) ((x)<(l)?((0)):((x)>(u)?(0):(1)))

#define CALIBRATIONPOINTS    9

FILE *logfile;
#define Log(args...) fprintf(logfile,args);

FILE *ellipse_log;

#define MIN_PUPIL_CONTOUR_POINTS  	500   
#define MAX_PUPIL_CONTOUR_POINTS  	10000    
#define PUPIL_SIZE_TOLERANCE 		1000	//range of allowed pupil diameters
#define MAX_CONTOUR_COUNT		20

// Firewire Capture Variables
int dev;
int width=640,height=480,framerate=30;
FILE* imagefile;
dc1394_cameracapture cameras[2];
int numNodes;
int numCameras;
raw1394handle_t handle;
nodeid_t * camera_nodes;
dc1394_feature_set features;

// Load the source image. 
IplImage *eye_image=NULL;
IplImage *original_eye_image=NULL;
IplImage *threshold_image=NULL;
IplImage *ellipse_image=NULL;
IplImage *scene_image=NULL;

char Feature_Names[9][30] ={
 "BRIGHTNESS",
 "EXPOSURE",
 "SHARPNESS",
 "WHITE BALANCE",
 "HUE",
 "SATURATION",
 "GAMMA",
 "SHUTTER",
 "GAIN"};

typedef struct {
    int offset_value;
    int value;
    int min;
    int max;
    int available;   
    void (*callback)(int);
} camera_features;

camera_features eye_camera_features[9];

CvPoint pupil = {0,0};              //coordinates of pupil in tracker coordinate system
CvPoint corneal_reflection = {0,0}; //coordinates of corneal reflection in tracker coordinate system
CvPoint diff_vector = {0,0};             //vector between the corneal reflection and pupil
int corneal_reflection_r = 0;       //the radius of corneal reflection

int view_cal_points = 1;
int do_map2scene = 0;

int number_calibration_points_set = 0;
int ok_calibrate = 0;

// An int boolean that is set to indicated whether the last point 
// calculation succeeded.
// This is dirty hack that only passes information from functions 
// that I've (R. Ramsay) seen fail.
int valid_point_calc = 1;	
// An int boolean that is set to indicated whether the ellipse was
// about the right size to be a pupil
int valid_ellipse = 1;	

CvPoint  calipoints[CALIBRATIONPOINTS];       //conversion from eye to scene calibration points
CvPoint  scenecalipoints[CALIBRATIONPOINTS]; //captured (with mouse) calibration points
CvPoint  pucalipoints[CALIBRATIONPOINTS];   //captured eye points while looking at the calibration points in the scene
CvPoint  crcalipoints[CALIBRATIONPOINTS];    //captured corneal reflection points while looking at the calibration points in the scene
CvPoint  vectors[CALIBRATIONPOINTS];         //differences between the corneal reflection and pupil center

//scene coordinate interpolation variables
float a, b, c, d, e;                            //temporary storage of coefficients
float aa, bb, cc, dd, ee;                       //pupil X coefficients    
float ff, gg, hh, ii, jj;			//pupil Y coefficients 

float centx, centy;                             // translation to center pupil data after biquadratics
float cmx[4], cmy[4];                           // corner correctioncoefficients 
int inx, iny;                                   // translation to center pupil data before biquadratics

CvScalar White,Red,Green,Blue,Yellow;
int frame_number=0;

#define FRAMEW 640
#define FRAMEH 480

int monobytesperimage=FRAMEW*FRAMEH;
int yuv411bytesperimage=FRAMEW*FRAMEH*12/8;

int cameramode[2]={MODE_640x480_MONO,MODE_640x480_YUV411};

const double beta = 0.2;	//hysteresis factor for noise reduction
double *intensity_factor_hori = (double*)malloc(FRAMEH*sizeof(double)); //horizontal intensity factor for noise reduction
double *avg_intensity_hori = (double*)malloc(FRAMEH*sizeof(double)); //horizontal average intensity

//parameters for the algorithm
int edge_threshold = 20;		//threshold of pupil edge points detection
int rays = 18;				//number of rays to use to detect feature points
int min_feature_candidates = 10;	//minimum number of pupil feature candidates
int cr_window_size = 301;		//corneal refelction search window size

// The result, a point on the scene image the user is looking at.
CvPoint gaze_point;

// Constants that must be shared between process_image() 
// and process_image_display().
int *inliers_index;
CvSize ellipse_axis;


double map_matrix[3][3];
int save_image = 0;
int image_no = 0;
int save_ellipse = 0;
int ellipse_no = 0;
char eye_file[30];
char scene_file[30];
char ellipse_file[40];



#define FIX_UINT8(x) ( (x)<0 ? 0 : ((x)>255 ? 255:(x)) )

//----------------------- Firewire Image Capture Code -----------------------//

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

//------------ map pupil coordinates to screen coordinates ---------/
CvPoint homography_map_point(CvPoint p)
{
  CvPoint p2;
  double z = map_matrix[2][0]*p.x + map_matrix[2][1]*p.y + map_matrix[2][2];
  p2.x = (int)((map_matrix[0][0]*p.x + map_matrix[0][1]*p.y + map_matrix[0][2])/z);
  p2.y = (int)((map_matrix[1][0]*p.x + map_matrix[1][1]*p.y + map_matrix[1][2])/z);
  return p2;
}

// r is result matrix
void affine_matrix_inverse(double a[][3], double r[][3])
{
  double det22 = a[0][0]*a[1][1] - a[0][1]*a[1][0];
  r[0][0] = a[1][1]/det22;
  r[0][1] = -a[0][1]/det22;
  r[1][0] = -a[1][0]/det22;
  r[1][1] = a[0][0]/det22;

  r[2][0] = r[2][1] = 0;
  r[2][2] = 1/a[2][2];

  r[0][2] = -r[2][2] * (r[0][0]*a[0][2] + r[0][1]*a[1][2]);
  r[1][2] = -r[2][2] * (r[1][0]*a[0][2] + r[1][1]*a[1][2]);
}

// r is result matrix
void matrix_multiply33(double a[][3], double b[][3], double r[][3])
{
  int i, j;
  double result[9];
  double v = 0;
  for (j = 0; j < 3; j++) {
    for (i = 0; i < 3; i++) {
      v = a[j][0]*b[0][i];
      v += a[j][1]*b[1][i];
      v += a[j][2]*b[2][i];
      result[j*3+i] = v;
    }
  }
  for (i = 0; i < 3; i++) {
    r[i][0] = result[i*3];
    r[i][1] = result[i*3+1];
    r[i][2] = result[i*3+2];
  }
}

int cal_calibration_homography(void)
{
  int i, j;
  stuDPoint cal_scene[9], cal_eye[9];
  stuDPoint scene_center, eye_center, *eye_nor, *scene_nor;
  double dis_scale_scene, dis_scale_eye;  

  for (i = 0; i < 9; i++) {
    cal_scene[i].x = scenecalipoints[i].x;  
    cal_scene[i].y = scenecalipoints[i].y;
    cal_eye[i].x = vectors[i].x;
    cal_eye[i].y = vectors[i].y;
  }

  scene_nor = normalize_point_set(cal_scene, dis_scale_scene, scene_center, CALIBRATIONPOINTS);
  eye_nor = normalize_point_set(cal_eye, dis_scale_eye, eye_center, CALIBRATIONPOINTS);

  INFO("normalize_point_set end\n");
  INFO("scene scale:%lf  center (%lf, %lf)\n", dis_scale_scene, scene_center.x, scene_center.y);
  INFO("eye scale:%lf  center (%lf, %lf)\n", dis_scale_eye, eye_center.x, eye_center.y);

  const int homo_row=18, homo_col=9;
  double A[homo_row][homo_col];
  int M = homo_row, N = homo_col; //M is row; N is column
  double **ppa = (double**)malloc(sizeof(double*)*M);
  double **ppu = (double**)malloc(sizeof(double*)*M);
  double **ppv = (double**)malloc(sizeof(double*)*N);
  double pd[homo_col];
  for (i = 0; i < M; i++) {
    ppa[i] = A[i];
    ppu[i] = (double*)malloc(sizeof(double)*N);
  }
  for (i = 0; i < N; i++) {
    ppv[i] = (double*)malloc(sizeof(double)*N);
  }

  for (j = 0;  j< M; j++) {
    if (j%2 == 0) {
      A[j][0] = A[j][1] = A[j][2] = 0;
      A[j][3] = -eye_nor[j/2].x;
      A[j][4] = -eye_nor[j/2].y;
      A[j][5] = -1;
      A[j][6] = scene_nor[j/2].y * eye_nor[j/2].x;
      A[j][7] = scene_nor[j/2].y * eye_nor[j/2].y;
      A[j][8] = scene_nor[j/2].y;
    } else {
      A[j][0] = eye_nor[j/2].x;
      A[j][1] = eye_nor[j/2].y;
      A[j][2] = 1;
      A[j][3] = A[j][4] = A[j][5] = 0;
      A[j][6] = -scene_nor[j/2].x * eye_nor[j/2].x;
      A[j][7] = -scene_nor[j/2].x * eye_nor[j/2].y;
      A[j][8] = -scene_nor[j/2].x;
    }
  }

  INFO("normalize_point_set end\n");

  svd(M, N, ppa, ppu, pd, ppv);
  int min_d_index = 0;
  for (i = 1; i < N; i++) {
    if (pd[i] < pd[min_d_index])
      min_d_index = i;
  }

  for (i = 0; i < N; i++) {
      map_matrix[i/3][i%3] = ppv[i][min_d_index];   // the column of v that corresponds to the smallest singular value,
                                                    // which is the solution of the equations
  }

  double T[3][3] = {{0}};
  double T1[3][3] = {{0}};
  
  INFO("\nT1: \n");
  for (j = 0; j < 3; j++) {
    for (i = 0; i < 3; i++) {
      INFO("%8lf ", T1[j][i]);
    }
    INFO("\n");
  }  

  T[0][0] = T[1][1] = dis_scale_eye;
  T[0][2] = -dis_scale_eye*eye_center.x;
  T[1][2] = -dis_scale_eye*eye_center.y;
  T[2][2] = 1;

  INFO("\nmap_matrix: \n");
  for (j = 0; j < 3; j++) {
    for (i = 0; i < 3; i++) {
      INFO("%8lf ", map_matrix[j][i]);
    }
    INFO("\n");
  }   
  INFO("\nT: \n");
  for (j = 0; j < 3; j++) {
    for (i = 0; i < 3; i++) {
      INFO("%8lf ", T[j][i]);
    }
    INFO("\n");
  }  

  matrix_multiply33(map_matrix, T, map_matrix); 

  T[0][0] = T[1][1] = dis_scale_scene;
  T[0][2] = -dis_scale_scene*scene_center.x;
  T[1][2] = -dis_scale_scene*scene_center.y;
  T[2][2] = 1;

  INFO("\nmap_matrix: \n");
  for (j = 0; j < 3; j++) {
    for (i = 0; i < 3; i++) {
      INFO("%8lf ", map_matrix[j][i]);
    }
    INFO("\n");
  } 
  INFO("\nT: \n");
  for (j = 0; j < 3; j++) {
    for (i = 0; i < 3; i++) {
      INFO("%8lf ", T[j][i]);
    }
    INFO("\n");
  }   

  affine_matrix_inverse(T, T1);
  matrix_multiply33(T1, map_matrix, map_matrix);

  INFO("\nmap_matrix: \n");
  for (j = 0; j < 3; j++) {
    for (i = 0; i < 3; i++) {
      INFO("%8lf ", map_matrix[j][i]);
    }
    INFO("\n");
  }   

  for (i = 0; i < M; i++) {
    free(ppu[i]);
  }
  for (i = 0; i < N; i++) {
    free(ppv[i]);
  }
  free(ppu);
  free(ppv);
  free(ppa);
      
  free(eye_nor);
  free(scene_nor);
  INFO("\nfinish calculate calibration\n");
  return EXIT_SUCCESS;
}

CvPoint map_point(CvPoint p)      
{
 CvPoint p2;
 int quad=0;
 float x1,y1,xx,yy;

 // correct eye position by recentering offset:
 x1 = (float) p.x;    
 y1 = (float) p.y;

 // translate before biquadratic:
 x1 -= inx;        
 y1 -= iny;

 // biquadratic mapping:
 xx = aa+bb*x1+cc*y1+dd*x1*x1+ee*y1*y1;   
 yy = ff+gg*x1+hh*y1+ii*x1*x1+jj*y1*y1;

 // translate after biquadratic:
 x1 = xx - centx;                 
 y1 = yy - centy;

 // determine quadrant of point:
 if      (( x1<0 )&&( y1<0 )) quad = 0;   
 else if (( x1>0 )&&( y1<0 )) quad = 1;
 else if (( x1<0 )&&( y1>0 )) quad = 2;
 else if (( x1>0 )&&( y1>0 )) quad = 3;

 // fix up by quadrant:
 p2.x = (int)(xx + x1*y1*cmx[quad]);       
 p2.y = (int)(yy + x1*y1*cmy[quad]);

 return p2;
}



//---------- calibration  coefficient calculation ---------------//
// biquadratic equation fitter               
// x, y are coordinates of eye tracker point 
// X is x or y coordinate of screen point    
// computes a, b, c, d, and e in the biquadratic 
// X = a + b*(x-inx) + c*(y-iny) + d*(x-inx)*(x-inx) + e*(y-iny)*(y-iny) 
// where inx = x1, y1 = y1 to reduce the solution to a 4x4 matrix        

void dqfit( float x1, float y1, 
	    float x2, float y2, 
	    float x3, float y3, 
	    float x4, float y4, 
	    float x5, float y5,
	    float X1, float X2, float X3, float X4, float X5 )
{
 float den;
 float x22,x32,x42,x52;    // squared terms 
 float y22,y32,y42,y52;

 inx = (int)x1;            // record eye tracker centering constants 
 iny = (int)y1;
 a = X1;                    // first coefficient 
 X2 -= X1;  X3 -= X1;       // center screen points 
 X4 -= X1;  X5 -= X1;
 x2 -= x1;  x3 -= x1;       // center eye tracker points 
 x4 -= x1;  x5 -= x1;
 y2 -= y1;  y3 -= y1;  
 y4 -= y1;  y5 -= y1;
 x22 = x2*x2; x32 = x3*x3;   // squared terms of biquadratic 
 x42 = x4*x4; x52 = x5*x5;
 y22 = y2*y2; y32 = y3*y3;
 y42 = y4*y4; y52 = y5*y5;

 //Cramer's rule solution of 4x4 matrix */
 den = -x2*y3*x52*y42-x22*y3*x4*y52+x22*y5*x4*y32-y22*x42*y3*x5-
    x32*y22*x4*y5-x42*x2*y5*y32+x32*x2*y5*y42-y2*x52*x4*y32+
    x52*x2*y4*y32+y22*x52*y3*x4+y2*x42*x5*y32+x22*y3*x5*y42-
    x32*x2*y4*y52-x3*y22*x52*y4+x32*y22*x5*y4-x32*y2*x5*y42+
    x3*y22*x42*y5+x3*y2*x52*y42+x32*y2*x4*y52+x42*x2*y3*y52-
    x3*y2*x42*y52+x3*x22*y4*y52-x22*y4*x5*y32-x3*x22*y5*y42;

 b =  (-y32*y2*x52*X4-X2*y3*x52*y42-x22*y3*X4*y52+x22*y3*y42*X5+
    y32*y2*x42*X5-y22*x42*y3*X5+y22*y3*x52*X4+X2*x42*y3*y52+
    X3*y2*x52*y42-X3*y2*x42*y52-X2*x42*y5*y32+x32*y42*y5*X2+
    X2*x52*y4*y32-x32*y4*X2*y52-x32*y2*y42*X5+x32*y2*X4*y52+
    X4*x22*y5*y32-y42*x22*y5*X3-x22*y4*y32*X5+x22*y4*X3*y52+
    y22*x42*y5*X3+x32*y22*y4*X5-y22*x52*y4*X3-x32*y22*y5*X4)/den;

 c =  (-x32*x4*y22*X5+x32*x5*y22*X4-x32*y42*x5*X2+x32*X2*x4*y52+
    x32*x2*y42*X5-x32*x2*X4*y52-x3*y22*x52*X4+x3*y22*x42*X5+
    x3*x22*X4*y52-x3*X2*x42*y52+x3*X2*x52*y42-x3*x22*y42*X5-
    y22*x42*x5*X3+y22*x52*x4*X3+x22*y42*x5*X3-x22*x4*X3*y52-
    x2*y32*x42*X5+X2*x42*x5*y32+x2*X3*x42*y52+x2*y32*x52*X4+
    x22*x4*y32*X5-x22*X4*x5*y32-X2*x52*x4*y32-x2*X3*x52*y42)/den;

 d = -(-x4*y22*y3*X5+x4*y22*y5*X3-x4*y2*X3*y52+x4*y2*y32*X5-
    x4*y32*y5*X2+x4*y3*X2*y52-x3*y22*y5*X4+x3*y22*y4*X5+
    x3*y2*X4*y52-x3*y2*y42*X5+x3*y42*y5*X2-x3*y4*X2*y52-
    y22*y4*x5*X3+y22*X4*y3*x5-y2*X4*x5*y32+y2*y42*x5*X3+
    x2*y3*y42*X5-y42*y3*x5*X2+X4*x2*y5*y32+y4*X2*x5*y32-
    y42*x2*y5*X3-x2*y4*y32*X5+x2*y4*X3*y52-x2*y3*X4*y52)/den;

 e = -(-x3*y2*x52*X4+x22*y3*x4*X5+x22*y4*x5*X3-x3*x42*y5*X2-
    x42*x2*y3*X5+x42*x2*y5*X3+x42*y3*x5*X2-y2*x42*x5*X3+
    x32*x2*y4*X5-x22*y3*x5*X4+x32*y2*x5*X4-x22*y5*x4*X3+
    x2*y3*x52*X4-x52*x2*y4*X3-x52*y3*x4*X2-x32*y2*x4*X5+
    x3*x22*y5*X4+x3*y2*x42*X5+y2*x52*x4*X3-x32*x5*y4*X2-
    x32*x2*y5*X4+x3*x52*y4*X2+x32*x4*y5*X2-x3*x22*y4*X5)/den;
}


int CalculateCalibration(void)
{
  int i, j;
  float x, y, wx[9], wy[9];   	//work data points
  int calx[10], caly[10];	//scene coordinate interpolation variables
  int eye_x[10], eye_y[10];	//scene coordinate interpolation variables

  // Place scene coordinates into calx and caly
  for(i = 0; i<9;i++) {
    calx[i] = scenecalipoints[i].x;  caly[i] = scenecalipoints[i].y;
  }

  // Set the last "tenth"  point
  calx[9] = scenecalipoints[0].x;  caly[9] = scenecalipoints[0].y;

  // Store pupil into eye_x and eye_y
  for(i = 0; i < 9; i++) {
   eye_x[i] = vectors[i].x;
   eye_y[i] = vectors[i].y;
  }

  // Solve X biquadratic
  dqfit((float)eye_x[0],(float)eye_y[0],(float)eye_x[1],(float)eye_y[1],(float)eye_x[2],   
        (float)eye_y[2],(float)eye_x[3],(float)eye_y[3],(float)eye_x[4],(float)eye_y[4],
        (float)calx[0],(float)calx[1],(float)calx[2],(float)calx[3],(float)calx[4]);
  aa = a; bb = b; cc = c; dd = d; ee = e;

  // Solve Y biquadratic
  dqfit((float)eye_x[0],(float)eye_y[0],(float)eye_x[1],(float)eye_y[1],(float)eye_x[2],
        (float)eye_y[2],(float)eye_x[3],(float)eye_y[3],(float)eye_x[4],(float)eye_y[4],
        (float)caly[0],(float)caly[1],(float)caly[2],(float)caly[3],(float)caly[4]);
  ff = a; gg = b; hh = c; ii = d; jj = e;

  // Biquadratic mapping of points
  for(i = 0; i < 9; i++) {
    x = (float)(eye_x[i] - inx);
    y = (float)(eye_y[i] - iny);
    wx[i] = aa+bb*x+cc*y+dd*x*x+ee*y*y;
    wy[i] = ff+gg*x+hh*y+ii*x*x+jj*y*y;
  }
  
  // Shift screen points to center for quadrant compute
  centx = wx[0];      
  centy = wy[0];
    
  // Normalize to center:
  for(i = 0; i < 9; i++) {
   wx[i] -= centx;
   wy[i] -= centy;
  }
  
  // Compute coefficents for each quadrant
  for(i = 0; i < 4; i++) {
   j = i + 5;
   cmx[i] = (calx[j]-wx[j]-centx)/(wx[j]*wy[j]);
   cmy[i] = (caly[j]-wy[j]-centy)/(wx[j]*wy[j]);
  }

  return 0;
}


void Draw_Cross(IplImage *image, int centerx, int centery, int x_cross_length, int y_cross_length, CvScalar color)
{
  CvPoint pt1,pt2,pt3,pt4;

  pt1.x = centerx - x_cross_length;
  pt1.y = centery;
  pt2.x = centerx + x_cross_length;
  pt2.y = centery;

  pt3.x = centerx;
  pt3.y = centery - y_cross_length;
  pt4.x = centerx;
  pt4.y = centery + y_cross_length;

  cvLine(image,pt1,pt2,color,1, 8, 0);
  cvLine(image,pt3,pt4,color,1, 8, 0);
}

void Show_Calibration_Points()
{
  int i; 
  for (i=0;i<CALIBRATIONPOINTS;i++) 
    Draw_Cross(scene_image, scenecalipoints[i].x, scenecalipoints[i].y, 25, 25, CV_RGB(255,255,255));
}

void Zero_Calibration() 
{ 
  int i;
 
  for (i=0;i<CALIBRATIONPOINTS;i++) {
    scenecalipoints[i].x = 0;  
    scenecalipoints[i].y = 0;
 
    pucalipoints[i].x = 0;    
    pucalipoints[i].y = 0;
    
    crcalipoints[i].x = 0;    
    crcalipoints[i].y = 0;

    vectors[i].x = 0; 
    vectors[i].y = 0;
  }
  number_calibration_points_set=0;
}

void Set_Calibration_Point(int x, int y)
{

   if (number_calibration_points_set<CALIBRATIONPOINTS) {

     //store xy mouse "scene" coordinates into calibration array    
     scenecalipoints[number_calibration_points_set].x = x;
     scenecalipoints[number_calibration_points_set].y = y;

     //grab the "pupil" position
     pucalipoints[number_calibration_points_set].x = pupil.x;
     pucalipoints[number_calibration_points_set].y = pupil.y;
       
     //grab the "corneal reflection" points  
     crcalipoints[number_calibration_points_set].x = corneal_reflection.x;   
     crcalipoints[number_calibration_points_set].y = corneal_reflection.y;   
       
     //grab the "delta pupil cr" position 
     vectors[number_calibration_points_set].x = diff_vector.x; 
     vectors[number_calibration_points_set].y = diff_vector.y; 

     number_calibration_points_set++;
     INFO("calibration points number: %d (total 9)\n", number_calibration_points_set);
   } else {

     Zero_Calibration();

   }
}

void Set_Calibration_Point1(int x, int y)
{

   if (number_calibration_points_set<CALIBRATIONPOINTS) {

     //store xy mouse "scene" coordinates into calibration array    
     scenecalipoints[number_calibration_points_set].x = x;
     scenecalipoints[number_calibration_points_set].y = y;

     //grab the "pupil" position
     pucalipoints[number_calibration_points_set].x = pupil.x;
     pucalipoints[number_calibration_points_set].y = pupil.y;
       
     //grab the "corneal reflection" points  
     //crcalipoints[number_calibration_points_set].x = corneal_reflection.x;   
     //crcalipoints[number_calibration_points_set].y = corneal_reflection.y;   
       
     //grab the "delta pupil cr" position 
     vectors[number_calibration_points_set].x = pupil.x; 
     vectors[number_calibration_points_set].y = pupil.y; 

     number_calibration_points_set++;

   } else {

     Zero_Calibration();

   }
}





void Activate_Calibration() 
{
  int i;
  int calibration_result;

  INFO("Map eye to scene image\n");

  if (number_calibration_points_set==CALIBRATIONPOINTS) {
    //calibration_result = CalculateCalibration();
    calibration_result = cal_calibration_homography();
 
    INFO("Calibration result = %d\n", calibration_result);
 
    do_map2scene = !do_map2scene;
    view_cal_points = !view_cal_points;

    INFO("Scene coordinates:\n");
    for(i=0;i< CALIBRATIONPOINTS;i++) {
      INFO("pt %d x = %d , y = %d \n", i, scenecalipoints[i].x, scenecalipoints[i].y);
    }
    INFO("\n");

    INFO("Eye coordinates\n");
    for(i=0;i< CALIBRATIONPOINTS;i++) {
      INFO("pt %d x = %d , y = %d \n", i, pucalipoints[i].x, pucalipoints[i].y);
    }
    INFO("\n");

    INFO("Corneal reflection coordinates\n");
    for(i=0;i< CALIBRATIONPOINTS;i++) {
      INFO("pt %d x = %d , y = %d \n", i, crcalipoints[i].x, crcalipoints[i].y);
    }
    INFO("\n");
  } else {
    INFO("Attempt to activate calibration without a full set of points.\n");
  }
   
}



void Average_Frames(UINT8 *result_image, UINT8 *prev_image, UINT8 *now_image, UINT8 *next_image)
{
  int npixels = FRAMEW * FRAMEH;
  int i;
  for (i = 0; i < npixels; i++) {
    *result_image = (*prev_image + *now_image + *next_image) / 3;
    result_image++;
    prev_image++;
    now_image++;
    next_image++;
  }
}

void Normalize_Line_Histogram(IplImage *in_image) 
{
 unsigned char *s=(unsigned char *)in_image->imageData;
 int x,y;
 int linesum;
 double factor=0;
 int subsample=10;
 double hwidth=(100.0f*(double)width/(double)subsample);
/*
 char adjustment;
 for (y=0;y<height;y++) {
   linesum=0; 
   for (x=0;x<width;x+=subsample) {
     linesum+=*s;
     s+=subsample;
   }
   s-=width;
   adjustment=(char)(128-(double)(linesum)/(double)(width/subsample));
   for (x=0;x<width;x++) {
     *s=MIN(*s+adjustment,255);
     s++;
   }
 }
*/
 for (y=0;y<height;y++) {
   linesum=1; 
   for (x=0;x<width;x+=subsample) {
     linesum+=*s;
     s+=subsample;
   }
   s-=width;
   factor=hwidth/((double)linesum);
   for (x=0;x<width;x++) {
     *s=(unsigned char)(((double)*s)*factor);
     s++;
   }
 }
}


void Calculate_Avg_Intensity_Hori(IplImage* in_image)
{
  UINT8 *pixel = (UINT8*)in_image->imageData;
  int sum;
  int i, j;
  for (j = 0; j < in_image->height; j++) {
    sum = 0;
    for (i = 0; i < in_image->width; i++) {
      sum += *pixel;
      pixel++;
    }
    avg_intensity_hori[j] = (double)sum/in_image->width;
  }
}

void Reduce_Line_Noise(IplImage* in_image)
{
  UINT8 *pixel = (UINT8*)in_image->imageData;
  int i, j;
  double beta2 = 1 - beta;
  int adjustment;

  Calculate_Avg_Intensity_Hori(in_image);
  for (j = 0; j < in_image->height; j++) {
    intensity_factor_hori[j] = avg_intensity_hori[j]*beta + intensity_factor_hori[j]*beta2;
    adjustment = (int)(intensity_factor_hori[j] - avg_intensity_hori[j]);
    for (i = 0; i < in_image->width; i++) {
      *pixel =  FIX_UINT8(*pixel+adjustment);
      pixel++;
    }
  }
}



void FirewireFrame_to_RGBIplImage(void *FirewireFrame, IplImage *OpenCV_image)
{
  uyyvyy2rgb((unsigned char *)FirewireFrame, (unsigned char *)OpenCV_image->imageData, 640*480);
}

void Grab_Camera_Frames()
{
  Grab_IEEE1394();

  memcpy(eye_image->imageData,(char *)cameras[0].capture_buffer,monobytesperimage);
  //memcpy(scene_image->imageData,(char *)cameras[1].capture_buffer,monobytesperimage);
  FirewireFrame_to_RGBIplImage((unsigned char *)cameras[1].capture_buffer, scene_image);

  if (original_eye_image != NULL) 
  	cvReleaseImage(&original_eye_image);
  original_eye_image = cvCloneImage(eye_image);

  if (frame_number == 0) {
    Calculate_Avg_Intensity_Hori(eye_image);
    memcpy(intensity_factor_hori, avg_intensity_hori, eye_image->height*sizeof(double));    
  }    

  Release_IEEE1394();
  frame_number++;
}




void Open_Logfile(int argc, char** argv) 
{
  char defaultlogfilename[]="logfile.txt";
  char *logfilename;
  
  if (argc>1) {
    logfilename=argv[1];
  } else {
    logfilename=defaultlogfilename;
  }

  logfile=fopen(logfilename,"w+");

  if (logfile!=NULL) {
    fprintf(logfile,"Timestamp (seconds)\t pupil X\t pupil Y\t Scene X\t Scene Y\n");
  } else {
    fprintf(stderr,"Error opening logfile %s.",logfilename);
    exit(-1);
  }
}

void Close_Logfile() 
{
  fclose(logfile);
}

void Open_Ellipse_Log()
{
  const char *ellipse_log_name = "./Ellipse_ellipse_log.txt";
  ellipse_log = fopen(ellipse_log_name,"w+");

  if (logfile!=NULL) {
    fprintf(logfile,"Timestamp (seconds)\t a\t pupil b\t centerx\t centery\t theta\n");
  } else {
    fprintf(stderr,"Error opening logfile %s.", ellipse_log_name);
    exit(-1);
  }
}


// ====	!! Additions Made by R. Ramsay		====
// ====	These log information about 		====
// ====	calibrations to a calfile.			====

void Open_Calfile(int argc, char** argv)
{
  char defaultcalfilename[]="calfile.txt";
  char *calfilename;

  if (argc>1) {
    calfilename=argv[1];
  } else {
    calfilename=defaultcalfilename;
  }

  calfile=fopen(calfilename,"w+");

  if (calfile==NULL) {
    fprintf(stderr,"Error opening calfile %s.",calfilename);
    exit(-1);
  }
}

void Close_Calfile()
{
  fclose(calfile);
}





// ================ Code Changed as part of and update	================
// ================ to make this a lib.					================




// Register a calibration point (9 are needed), which is a
// point on the scene that the user is looking at, at this 
// instant.
void eyetracker_set_calibration_point(int x, int y)
{
		// If valid_point_calc == 0, then one of the step in calculating the features
		// (ie ellipse or corneal reflection failed). I don't know which errors are 
		// fatal so valid_point_calc is cleared for any worrying printf messages, that
		// I (R. Ramsay) know about (ie this is a hack but should work).
       if (valid_point_calc) {
		   Set_Calibration_Point(x,y);
       } else {
		   INFO("Ahoy!: The calibration point was not set because the point-calculation failed.\n");
	   }
}


// Calibrate the Eye tracker once all 9 points have been 
// registered with eyetracker_set_calibration_point().
void eyetracker_activate_calibration()
{
	Activate_Calibration();
}


void eyetracker_set_pupil_search_startpoint(int x, int y)
{
       printf("left mouse eye window (%d,%d)\n", x, y);
       pupil.x = x;
       pupil.y = y;
       //if (!start) { 
         printf("start point: %d, %d\n", x, y); 
         start_point.x = x;
         start_point.y = y;
//         start = 1;
       //}
}



void eyetracker_save_eye_and_scene_images(void)
{
      sprintf(eye_file, "eye%05d.bmp", image_no);
      sprintf(scene_file, "scene%05d.bmp", image_no);
      image_no++;
      cvSaveImage(eye_file, eye_image);
      cvSaveImage(scene_file, scene_image);
      printf("thres: %d\n", pupil_edge_thres);
}


void eyetracker_save_image(void)
{
  save_image = 1 - save_image;
  printf("save_image = %d\n", save_image);
}



void eyetracker_save_ellipse(void)
{
  save_ellipse = 1 - save_ellipse;
  printf("save_ellipse = %d\n", save_ellipse);
  if (save_ellipse == 1) {
    Open_Ellipse_Log();
  } else {
    fclose(ellipse_log);
  }

}



void process_image()
{
  static int lost_frame_num = 0;
  Grab_Camera_Frames();
  cvZero(ellipse_image);

  valid_point_calc = 1;		// This is a valid point calculation so far.
  valid_ellipse = 1;		// This is a valid ellipse so far.

  cvSmooth(eye_image, eye_image, CV_GAUSSIAN, 5, 5);
  Reduce_Line_Noise(eye_image);  
  
  
  //corneal reflection
  remove_corneal_reflection(eye_image, threshold_image, (int)start_point.x, (int)start_point.y, cr_window_size, 
                   (int)eye_image->height/10, corneal_reflection.x, corneal_reflection.y, corneal_reflection_r, &valid_point_calc);  
  printf("corneal reflection: (%d, %d)\n", corneal_reflection.x, corneal_reflection.y);


  //starburst pupil contour detection
  starburst_pupil_contour_detection((UINT8*)eye_image->imageData, eye_image->width, eye_image->height,
                                edge_threshold, rays, min_feature_candidates, &valid_point_calc);
  
  inliers_num = 0;
  if (inliers_index != NULL) {
	  free(inliers_index); 
	  inliers_index = NULL;
  }
  inliers_index = pupil_fitting_inliers((UINT8*)eye_image->imageData, eye_image->width, eye_image->height, inliers_num, &valid_point_calc);
  ellipse_axis.width = (int)pupil_param[0];
  ellipse_axis.height = (int)pupil_param[1];
  pupil.x = (int)pupil_param[2];
  pupil.y = (int)pupil_param[3];



  if (ellipse_axis.width > 0 && ellipse_axis.height > 0) {
    start_point.x = pupil.x;
    start_point.y = pupil.y;

    diff_vector.x = pupil.x - corneal_reflection.x;
    diff_vector.y = pupil.y - corneal_reflection.y;
//	if (do_map2scene) {
      gaze_point = homography_map_point(diff_vector);
//   }
    lost_frame_num = 0;    
  } else {
    lost_frame_num++;
  	valid_ellipse = 0;		
  }
  if (lost_frame_num > 5) {
    start_point.x = FRAMEW/2;
    start_point.y = FRAMEH/2;
  }

}




// Display code removed from process_image().
void process_image_display(void)
{
  if (save_image == 1) {
    printf("save image %d\n", image_no);
    sprintf(eye_file, "./Eye_eye_%05d.jpg", image_no);
    image_no++;
    cvSaveImage(eye_file, eye_image);
  }
 
  Draw_Cross(ellipse_image, corneal_reflection.x, corneal_reflection.y, 15, 15, Yellow);  

  Draw_Cross(ellipse_image, pupil.x, pupil.y, 15, 15, Red);
  cvLine(eye_image, pupil, corneal_reflection, Red, 4, 8, 0);
  cvLine(ellipse_image, pupil, corneal_reflection, Red, 4, 8, 0);
  

  printf("ellipse a:%lf; b:%lf, cx:%lf, cy:%lf, theta:%lf; inliers_num:%d\n\n", 
         pupil_param[0], pupil_param[1], pupil_param[2], pupil_param[3], pupil_param[4], inliers_num);


  bool is_inliers = 0;
  for ( int i = 0; i < (int)edge_point.size(); i++) {
    is_inliers = 0;
    for (int j = 0; j < inliers_num; j++) {
      if (i == inliers_index[j])
        is_inliers = 1;
    }
    stuDPoint *edge = edge_point.at(i);
    if (is_inliers)
      Draw_Cross(ellipse_image, (int)edge->x,(int)edge->y, 5, 5, Green);
    else
      Draw_Cross(ellipse_image, (int)edge->x,(int)edge->y, 3, 3, Yellow);
  }
  free(inliers_index); 
  inliers_index = NULL;


 if (ellipse_axis.width > 0 && ellipse_axis.height > 0) {
    //printf("start_point: %d,%d\n", start_point.x, start_point.y);
    Draw_Cross(eye_image, pupil.x, pupil.y, 10, 10, Green);
    cvEllipse(eye_image, pupil, ellipse_axis, -pupil_param[4]*180/PI, 0, 360, Red, 2);
    cvEllipse(ellipse_image, pupil, ellipse_axis, -pupil_param[4]*180/PI, 0, 360, Green, 2);

    if (do_map2scene) {
      printf("gaze_point: (%d,%d)\n", gaze_point.x, gaze_point.y);  
//      Draw_Cross(scene_image, gaze_point.x, gaze_point.y, 60, 60, Red);
    }
  }

  
  Draw_Cross(ellipse_image, (int)start_point.x, (int)start_point.y, 7, 7, Blue);
  Draw_Cross(eye_image, (int)start_point.x, (int)start_point.y, 7, 7, Blue);

  if (save_ellipse == 1) {
    printf("save ellipse %d\n", ellipse_no);
    sprintf(ellipse_file, "./Ellipse_ellipse_%05d.jpg", ellipse_no);
    ellipse_no++;
    cvSaveImage(ellipse_file, ellipse_image);
    fprintf(ellipse_log, "%.3f\t %8.2lf %8.2lf %8.2lf %8.2lf %8.2lf\n",
            Time_Elapsed(), pupil_param[0], pupil_param[1], pupil_param[2], pupil_param[3], pupil_param[4]);
  }
  
  printf("Time elapsed: %.3f\n", Time_Elapsed()); 
  fprintf(logfile,"%.3f\t%d\t%d\t%d\t%d\t%d\t%d\t%d\t%d\n",
					Time_Elapsed(),
					pupil.x,    
					pupil.y,    
					corneal_reflection.x,    
					corneal_reflection.y,
					diff_vector.x,    
					diff_vector.y,    
					gaze_point.x,    
					gaze_point.y);    

  if (view_cal_points) Show_Calibration_Points();
}




// Returns true/false
int eyetracker_calc_gaze(void)
{
// ??: This is unnecessary: 
//
//  if (start_point.x == -1 && start_point.y == -1)
//      Grab_Camera_Frames();
//  }

    process_image(); 
    process_image_display(); 

// ??: This is unnecessary: (unless we need to store one set of frames 
//     before we can search/print properly)
//
//    if (frame_number%1==0) Update_Gui_Windows(); 

	if (!valid_point_calc || !valid_ellipse || !do_map2scene) 
		return 0;
	else
		return 1;
}

CvPoint eyetracker_get_gaze_target(void)
{
	return gaze_point;
}

	



// Code removed from the main function, when this was rewritten
// as a lib system. 
void eyetracker_setup(int argc, char **argv)
{
  printf("Starting eyetracker setup\n");
  Open_IEEE1394();

  eyetracker_setup_image_buffs();

  Open_Logfile(argc,argv);
  Open_Calfile(argc, argv);
  Open_Ellipse_Log();

  Start_Timer();
  printf("Eyetracker is ready and setup\n");
}



// Code removed from the main function (when this was rewritten
// as a lib system).
void eyetracker_cleanup(void)
{
  eyetracker_cleanup_image_buffs();

  Close_Logfile();
  Close_Calfile();
//  Close_Ellipse_Log();

  Close_IEEE1394();
}


void eyetracker_setup_image_buffs(void)
{
  //Make the eye image (in monochrome):
  eye_image=cvCreateImageHeader(cvSize(640,480), 8, 1 );
  eye_image->imageData=(char *)malloc(640*480);
  
  //Make the eye image (in monochrome):
  threshold_image = cvCloneImage(eye_image);
  
  //Make the ellipse image (in RGB) :
  ellipse_image=cvCreateImageHeader(cvSize(640,480), 8, 3 );
  ellipse_image->imageData=(char *)malloc(640*480*3);
 
  //Make the scene image:    
  scene_image=cvCreateImageHeader(cvSize(640,480), 8, 3 );
  scene_image->imageData=(char *)malloc(640*480*3);
  

  //Init colors
  White = CV_RGB(255,255,255);
  Red = CV_RGB(255,0,0);
  Green = CV_RGB(0,255,0);
  Blue = CV_RGB(0,0,255);
  Yellow = CV_RGB(255,255,0);
}


void eyetracker_cleanup_image_buffs(void)
{  
  cvReleaseImageHeader(&eye_image );
  cvReleaseImageHeader(&threshold_image );
  cvReleaseImageHeader(&original_eye_image );
  cvReleaseImageHeader(&ellipse_image );
  cvReleaseImageHeader(&scene_image );

  cvReleaseImage(&eye_image);
  cvReleaseImage(&threshold_image);
  cvReleaseImage(&original_eye_image);
  cvReleaseImage(&ellipse_image);
  cvReleaseImage(&scene_image);
}




IplImage * eyetracker_get_eye_image(void)
  { return eye_image; }

IplImage * eyetracker_get_original_eye_image(void)
  { return original_eye_image; }

IplImage * eyetracker_get_ellipse_image(void)
  { return ellipse_image; }  	

IplImage * eyetracker_get_scene_image(void)
  { return scene_image; }



int * eyetracker_get_pupil_edge_thres_ptr(void)
  { return &pupil_edge_thres; }

int * eyetracker_get_rays_ptr(void)
  { return &rays; }

int * eyetracker_get_min_feature_candidates_ptr(void)
  { return &min_feature_candidates; }

int * eyetracker_get_cr_window_size_ptr(void)
  { return &cr_window_size; }



int eyetracker_get_FRAMEH(void)
  { return (int) FRAMEH; }

