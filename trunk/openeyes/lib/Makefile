#
# File:  Makefile (for cvEyeTrack library)
#

PREFIX = /usr/local/
#PREFIX = ./opt/

LIB = libCvEyeTrack.so

LIBDEST = $(PREFIX)lib/
INCDEST = $(PREFIX)include/

LIBHEADER = cvEyeTracker.h

EXAMPLE = tracker_example

CXX			=	g++
CXXFLAGS	=	-g -Wall -fPIC

#DEFINES= -O2
DEFINES=

# -L/usr/local/lib
LIBDIRS		=	-L/usr/X11R6/lib -L/lib -L/usr/lib
LIBS		=	-lm -ldc1394_control -lraw1394 -lcv -lcvaux -lhighgui
INCLUDES	=	-I/usr/include/opencv

OBJS 		= 	remove_corneal_reflection.o \
				ransac_ellipse.o \
				svd.o \
				timing.o \
				cvEyeTracker.o \
			  	
			  	  
HEADDERS 	=	remove_corneal_reflection.h \
				ransac_ellipse.h \
				svd.h \
				timing.h \
				$(LIBHEADER)
				
LIBSRC = cvEyeTracker.c

#LIBOBJ = $(LIBSRC:.c=.o)


default:
	@echo ""
	@echo "Build and install the cvEyeTracker library to /usr/local/lib"
	@echo "with the command: 'sudo make install'"
	@echo "Or build inplace with 'make build'"
	@echo ""
	
install: build $(LIB)
	@echo lib Makefile - installing $(LIB)
	@install -m 444 $(LIB) $(LIBDEST)
	@install -m 444 $(LIBHEADER) $(INCDEST)
	@echo "Install Complete."
	
	
$(LIB): $(libObj)
	@echo lib Makefile - archiving $(LIB)
#	@$(AR) r $(LIB) $(LIBOBJ)

build: $(OBJS)
	@echo "Linking" 
	$(CXX) -shared -o $(LIB) *.o
	@echo "Library Built."

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
	rm -f *~
	rm -f $(LIB)
	
