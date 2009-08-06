#
# File:  Makefile (for example using the library)
#


EXAMPLE = tracker_example

CXX			=	g++

#DEFINES= -O2
DEFINES=

# This is the base directory for the cvEyeTrack library
# Underneath there may be a lib, and an include dir
CV_EYE_PREFIX = /usr/local

# This must point to the dir with cvEyeTrack.h
CV_EYE_INC = $(CV_EYE_PREFIX)/include

# This must point to the dir with the shared library
CV_EYE_LIB = $(CV_EYE_PREFIX)/lib

CXXFLAGS	= -g -Wall 

# Insert the path of the cvEyeTrack library for runtime execution.
LINKERFLAGS = -Wl,-rpath $(CV_EYE_LIB)

INCLUDES	=	`pkg-config --cflags opencv`	\
				`pkg-config --cflags libdc1394`	\
				-I$(CV_EYE_INC)

LIBDIRS		=	-L/usr/X11R6/lib -L/lib `pkg-config --libs-only-L opencv`
LIBS		=	-lm 							\
				`pkg-config --libs opencv` 		\
				`pkg-config --libs libdc1394` 	\
				-lCvEyeTrack

OBJS 		= 	tracker_example.o
			  	  
HEADDERS 	=	

default: tracker_example
	
	
tracker_example: tracker_example.o $(OBJS)
	$(CXX) $(CXXFLAGS) $(LINKERFLAGS) $(DEFINES) $(LIBDIRS) $(LIBS) \
		-pg -o tracker_example $(OBJS)

tracker_example.o: tracker_example.cpp $(HEADDERS)
	$(CXX) $(CXXFLAGS) $(DEFINES) $(INCLUDES) -c tracker_example.cpp 
	


clean:
	rm -f *.o
	rm -f *~
	rm -f tracker_example
	
