#
# File:  Makefile (for example using the library)
#


EXAMPLE = boxy

CXX			=	g++

#DEFINES= -O2
DEFINES=

# This is the base directory for the cvEyeTrack library
# Underneath there may be a lib, and an include dir
CV_EYE_PREFIX = /usr/local

# This must point to the dir with cvEyeTrack.h
CV_EYE_INC = $(CV_EYE_PREFIX)/include


# The following settings should probably not need to be changed.

# This must point to the dir with the shared library
CV_EYE_LIB = $(CV_EYE_PREFIX)/lib

CXXFLAGS	= -g -Wall 

# Insert the path of the cvEyeTrack library for runtime execution.
# Was nessasary if libCvEyeTrack is not installed
#LINKERFLAGS = -Wl,-rpath $(CV_EYE_LIB)

INCLUDES	=	`pkg-config --cflags opencv`	\
				-I$(CV_EYE_INC)

LIBDIRS		=	-L/usr/X11R6/lib -L/lib `pkg-config --libs-only-L opencv`
LIBS		=	-lm 							\
				`pkg-config --libs opencv` 		\
				-lCvEyeTrack

OBJS 		= 	boxy.o
			  	  
HEADDERS 	=	

default: boxy
	
boxy: boxy.o $(OBJS)
	$(CXX) $(CXXFLAGS) $(LINKERFLAGS) $(DEFINES) $(LIBDIRS) $(LIBS) \
		-pg -o boxy $(OBJS)

boxy.o: boxy.c $(HEADDERS)
	$(CXX) $(CXXFLAGS) $(DEFINES) $(INCLUDES) -c boxy.c 
	
clean:
	rm -f *.o
	rm -f *~
	rm -f boxy

