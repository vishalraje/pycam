
all : tracker_example

SOURCES		=	tracker_example.c

OBJS 		= 	remove_corneal_reflection.o \
				    ransac_ellipse.o \
				    svd.o \
				    timing.o \
				    cvEyeTracker.o \
			  	  tracker_example.o
			  	  
HEADDERS 	=	remove_corneal_reflection.h \
				    ransac_ellipse.h \
				    svd.h \
				    timing.h \
				    cvEyeTracker.h


CXX			=	g++
CXXFLAGS	=	-g -Wall

#DEFINES= -O2
DEFINES=

# -L/usr/local/lib
LIBDIRS		=	-L/usr/X11R6/lib -L/lib
LIBS		=	-lm -ldc1394_control -lraw1394 -lcv -lcvaux -lhighgui
INCLUDES	=	-I/usr/include/opencv 


tracker_example: tracker_example $(OBJS)
	$(CXX) $(CXXFLAGS) $(DEFINES) $(LIBDIRS) $(LIBS) \
		-pg -o tracker_example $(OBJS) 

tracker_example.o: tracker_example.c $(HEADDERS)
	$(CXX) $(CXXFLAGS) $(DEFINES) $(INCLUDES) -c tracker_example.c 

cvEyeTracker.o: cvEyeTracker.c $(HEADDERS)
	$(CXX) $(CXXFLAGS)  $(DEFINES) $(INCLUDES)  -c cvEyeTracker.c 

remove_corneal_reflection.o: remove_corneal_reflection.c $(HEADDERS)
	$(CXX) $(CXXFLAGS)  $(DEFINES) $(INCLUDES)  -c remove_corneal_reflection.c 

ransac_ellipse.o: ransac_ellipse.cpp $(HEADDERS)
	$(CXX) $(CXXFLAGS)  $(DEFINES)  -c ransac_ellipse.cpp 

svd.o: svd.c $(HEADDERS)
	$(CXX) $(CXXFLAGS)  $(DEFINES)  -c svd.c

timing.o: timing.c $(HEADDERS)
	$(CXX) $(CXXFLAGS)  $(DEFINES)  -c timing.c


clean:
	rm -f *.o 

purge: clean
	rm *~ tracker_example

