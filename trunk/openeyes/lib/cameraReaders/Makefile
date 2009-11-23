# This creates a openEyesCameraReader.o file from one of the targets in this dir.
# All files have the same .h interface.

.PHONY: default firewire_target opencv_target clean purge

default: firewire_target 


# Compiler settings.

CXX			=	g++
CXXFLAGS	=	-g -Wall

#DEFINES= -O2
DEFINES=

#-L/usr/local/lib
LIBDIRS		=	-L/usr/lib
LIBS		=	-lm -ldc1394_control -lraw1394 -lcv -lcvaux -lhighgui
INCLUDES	=	-I.. -I/usr/include/opencv -I/usr/include/dc1394 



# Build instructions.

opencv_target:
	@echo ---- openEyesCameraReader.o: Making opencv version ----
	$(CXX) $(CXXFLAGS) $(DEFINES) $(INCLUDES) -o openEyesCameraReader.o -c opencvCamera.cpp 

firewire_target: 
	@echo ---- openEyesCameraReader.o: Making Firewire version ----
	$(CXX) $(CXXFLAGS) $(DEFINES) $(INCLUDES) -o openEyesCameraReader.o -c firewireCamera.cpp


clean:
	rm -f *.o 

purge: clean
	rm -f *~ 





