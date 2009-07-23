/* Iterface to the cpp file ransac_ellipse.cpp */


%include stl.i

%module ransacEllipse
%{
    /* Put header files here or function declarations like below */
    #include "ransac_ellipse.h"
%}

// Tell swig to put type information into the functions docstrings...
%feature("autodoc", "1");

// Tell swig to parse the header file.
%include "ransac_ellipse.h"

