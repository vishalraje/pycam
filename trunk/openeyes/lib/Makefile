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
				firewire_camera.o \
				colour_conversions.o
			  	
			  	  
HEADDERS 	=	remove_corneal_reflection.h \
				ransac_ellipse.h \
				svd.h \
				timing.h \
				firewire_camera.h \
				colour_conversions.h \
				$(LIBHEADER)
				
LIBSRC = cvEyeTracker.c

#LIBOBJ = $(LIBSRC:.c=.o)


default: build
	@echo ""
	@echo "Finished building the cvEyeTracker library.   "
	@echo "to install:"
	@echo "    'sudo make install'                "
	@echo ""
	
install: build $(LIB)
	@echo lib Makefile - installing $(LIB)
	@install -m 444 $(LIB) $(LIBDEST)
	@install -m 444 $(LIBHEADER) $(INCDEST)
	ldconfig -n $(LIBDEST)  # Might have to execute this in the dest?
	@echo "Install Complete."
	
	
$(LIB): $(libObj)
	@echo lib Makefile - archiving $(LIB)
#	@$(AR) r $(LIB) $(LIBOBJ)

build: $(OBJS)
	@echo "Linking" 
	$(CXX) -shared -Wl,-soname,$(LIB) -o $(LIB) \
	*.o -lc $(LIBS)
	@echo "Library Built."

cvEyeTracker.o: cvEyeTracker.c ransac_ellipse.o $(HEADDERS)
	$(CXX) $(CXXFLAGS) $(DEFINES) $(INCLUDES) -c cvEyeTracker.c 

remove_corneal_reflection.o: remove_corneal_reflection.c $(HEADDERS)
	$(CXX) $(CXXFLAGS) $(DEFINES) $(INCLUDES) -c remove_corneal_reflection.c 

ransac_ellipse.o: ransac_ellipse.cpp $(HEADDERS)
	$(CXX) $(CXXFLAGS) $(DEFINES) $(INCLUDES) -c ransac_ellipse.cpp

firewire_camera.o: firewire_camera.cpp $(HEADDERS)
	$(CXX) $(CXXFLAGS) $(DEFINES) $(INCLUDES) -c firewire_camera.cpp

svd.o: svd.c $(HEADDERS)
	$(CXX) $(CXXFLAGS) $(DEFINES) -c svd.c

timing.o: timing.c $(HEADDERS)
	$(CXX) $(CXXFLAGS) $(DEFINES) -c timing.c
	
colour_conversions.o: colour_conversions.c $(HEADERS)
	$(CXX) $(CXXFLAGS) $(DEFINES) -c colour_conversions.c

clean:
	rm -f *.o
	rm -f *~
	rm -f $(LIB)
	
