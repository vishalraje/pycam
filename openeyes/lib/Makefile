#
# File:  Makefile (for cvEyeTrack library)
#

PREFIX = /usr/
#PREFIX = /usr/local/
#PREFIX = ./opt/

LIB = libCvEyeTrack.so

LIBDEST = $(PREFIX)lib/
INCDEST = $(PREFIX)include/

LIBHEADER = cvEyeTracker.h

EXAMPLE = tracker_example

CXX			=	g++
CXXFLAGS	=	-g -Wall -fPIC

#DEFINES= -O2
DEFINES="-D__MINGW__"

# -L/usr/local/lib
LIBDIRS		=	-L/usr/X11R6/lib -L/lib -L/usr/lib
LIBS		=	-lm -lcv -lcvaux -lhighgui -lcxcore
INCLUDES	=	-I/usr/include/opencv

OBJS 		= 	remove_corneal_reflection.o \
				ransac_ellipse.o \
				svd.o \
				timing.o \
				cvEyeTracker.o \
				cameraReaders/openEyesCameraReader.o \
				colour_conversions.o
			  	
			  	  
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
	
uninstall:
	@echo Removing libraries from system.
	rm -f $(LIBDEST)/$(LIB)
	rm -f $(INCDEST)/$(LIBHEADER)
	@echo "Uninstall Complete."

	
$(LIB): $(libObj)
	@echo lib Makefile - archiving $(LIB)
#	@$(AR) r $(LIB) $(LIBOBJ)

build: $(OBJS)
	@echo "Linking" 
	$(CXX) -shared -Wl,-soname,$(LIB) -o $(LIB) \
	$(OBJS) $(LIBS)
	@echo "Library Built."

#	*.o $(LIBS)

cvEyeTracker.o: cvEyeTracker.c ransac_ellipse.o 
	$(CXX) $(CXXFLAGS) $(DEFINES) $(INCLUDES) -c cvEyeTracker.c 

remove_corneal_reflection.o: remove_corneal_reflection.c 
	$(CXX) $(CXXFLAGS) $(DEFINES) $(INCLUDES) -c remove_corneal_reflection.c 

ransac_ellipse.o: ransac_ellipse.cpp 
	$(CXX) $(CXXFLAGS) $(DEFINES) $(INCLUDES) -c ransac_ellipse.cpp

svd.o: svd.c 
	$(CXX) $(CXXFLAGS) $(DEFINES) -c svd.c

timing.o: timing.c 
	$(CXX) $(CXXFLAGS) $(DEFINES) -c timing.c
	
colour_conversions.o: colour_conversions.c 
	$(CXX) $(CXXFLAGS) $(DEFINES) -c colour_conversions.c

cameraReaders/openEyesCameraReader.o:
	make -C cameraReaders firewire_target

clean:
	rm -f *.o
	rm -f *~
	rm -f $(LIB)
	@echo
	make -C cameraReaders purge 

	
