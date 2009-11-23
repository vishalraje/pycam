
==== Overview ====

This folder contains files for reading images from the camera. There is a single interface defined by openEyesCameraReader.h, but different libararies can supply the .o files for this interface. 

At the moment these are two possible interfaces,
	+ firewireCamera.cpp	
	+ opencvCamera.cpp

These can be compiled to openEyesCameraReader.o, by building **ONE** of the make targets,
	+ make firewire_target
	+ make opencv_target



==== firewire_target Notes ====

This is the original camera-interface that originally came with OpenEyes, and should only works on Linux. To work, it needs the libdc1394 and libraw1394 libraries installed on your system (IEEE1394 = Firewire). To test if you can read frames using this library install the program coriander and try and read images from a firewire camera.



==== opencv_target Notes ====

This was added by Brian Thorn, but I (R Ramsay) don't know exactly its specifics. It uses OpenCV to read images. I haven't tested this on Windows, but in Linux it could read from UVC-V4L devices but not firewire ones.



==== TODO ====

+ Remove refereces to Firewire/1394/IEEE/etc... from opencvCamera.cpp and openEyesCameraReader.h
+ Get Brian to update/flesh out "opencv_target Notes".
+ Have Brian to update/flesh add any extra notes here, including on possible windows porting.



