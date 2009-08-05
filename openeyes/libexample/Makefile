#
# File:  Makefile (for library)
#


EXAMPLE = tracker_example


CXX			=	g++
CXXFLAGS	=	-g -Wall -Wl,-rpath /usr/local/lib/

#DEFINES= -O2
DEFINES=

# -L/usr/local/lib
LIBDIRS		=	-L/usr/X11R6/lib -L/lib -L/usr/local/lib/
LIBS		=	-lm -ldc1394_control -lraw1394 -lcv -lcvaux -lhighgui -lCvEyeTrack
INCLUDES	=	-I/usr/include/opencv -I./../lib/opt/include/

OBJS 		= 	tracker_example.o
			  	  
HEADDERS 	=	

default: tracker_example
	
	
tracker_example: tracker_example $(OBJS)
	$(CXX) $(CXXFLAGS) $(DEFINES) $(LIBDIRS) $(LIBS) \
		-pg -o tracker_example $(OBJS)

tracker_example.o: tracker_example.c $(HEADDERS)
	$(CXX) $(CXXFLAGS) $(DEFINES) $(INCLUDES) -c tracker_example.c 
	


clean:
	rm -f *.o
	rm *~
	rm tracker_example
	
