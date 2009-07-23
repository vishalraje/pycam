/* Iterface to the c file remove_corneal_reflection.c */
%module removeCornealReflection
%{
    /* Put header files here or function declarations like below */
    #include "opencv/cv.h"
    #include "remove_corneal_reflection.h"

%}

// Tell swig to put type information into the functions docstrings...
%feature("autodoc", "1");

// Tell swig to parse the header file.
%include "remove_corneal_reflection.h"
