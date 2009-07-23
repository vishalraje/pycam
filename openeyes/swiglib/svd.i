/* Iterface to the cpp file svd.cpp */


%module svd
%{
    /* Put header files here or function declarations like below */
    #include "svd.h"
%}

// Tell swig to put type information into the functions docstrings...
%feature("autodoc", "1");

// Tell swig about the function to wrap...
extern void svd(int m, int n, double **a, double **p, double *d, double **q);
