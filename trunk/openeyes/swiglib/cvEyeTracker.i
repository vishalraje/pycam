/* cvEyeTracker.i */

%exception
    {
    try { $action } 
    catch (...) 
        {
        return NULL;
        } 
    }
 
 
%include "exception.i"
 
%typemap(in) IplImage * (IplImage header){
	void * vptr;
	int res = SWIG_ConvertPtr($input, (&vptr), $descriptor( CvMat * ), 0);
	if ( res == -1 ){
		SWIG_exception( SWIG_TypeError, "%%typemap(in) IplImage * : could not convert to CvMat");
		SWIG_fail;
	}
	$1 = cvGetImage((CvMat *)vptr, &header);
}
 
%typemap(in) IplImage *mask{
	if ($input == Py_None){
	   $1 = NULL;
	}
	else {
		SWIG_exception( SWIG_TypeError, "%%typemap(in) IplImage *mask : masks not supported yet.");
		SWIG_fail;
	}
}
 
%typecheck(SWIG_TYPECHECK_POINTER) IplImage * {
  void *ptr;
  if (SWIG_ConvertPtr($input, (void **) &ptr, $descriptor( CvMat * ), 0) == -1) {
    $1 = 0;
    PyErr_Clear();
  } else {
    $1 = 1;
  }
}


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
 
 

