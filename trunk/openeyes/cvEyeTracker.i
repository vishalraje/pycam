/* cvEyeTracker.i */
 %module cvEyeTrack
 %{
 /* Put header files here or function declarations like below */
 //define SWIG_FILE_WITH_INIT
 #include "cvEyeTracker.h"
 %}
 
 // Tell swig to put type information into the functions docstrings...
%feature("autodoc", "1");

// Tell swig to parse the header file.
%include "cvEyeTracker.h"

//extern int inliers_num;
//extern void Draw_Cross(IplImage *image, int centerx, int centery, int x_cross_length, int y_cross_length, CvScalar color);
 
 

