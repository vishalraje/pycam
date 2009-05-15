// Random test library for use with swig...
/* Include all the standard libs we wish to use */

// iostream allows us to interact with the standard in and std out.
#include <iostream>

// include the string type and functions...
#include <string>

// include the opencv library
//#include "opencv/cv.h"

// preprocessor defined constant
#define AUTHOR "Brian Thorne"

// const defined constant
const int yearMade = 2008;

void printString();

void printLine(std::string s);
void simpleProcess();
void commaOp();
void booltest();
void wait4in();

int factorial(int num);

int add(int x1, int x2, int x3=0,int x4=0);

/** Ask for a name using cin and cout. */
std::string getName();

void runAll(int,std::string);


