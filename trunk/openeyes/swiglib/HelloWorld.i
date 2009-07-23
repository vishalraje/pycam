/* Iterface to the c++ hello world app */

// Tells swig to use its inbuilt libs for things like string
%include stl.i

//%feature("autodoc","docstring")

%module helloWorld
%{
    /* Put header files here or function declarations like below */
    #include "Hello World.h"
%}



// Tell swig to put type information into the functions docstrings...
%feature("autodoc", "1");


// Tell swig to parse the header file.
%include "Hello World.h"

