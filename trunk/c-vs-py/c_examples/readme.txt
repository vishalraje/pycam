This directory holds all the C/C++ examples used comparing OpenCV from Python or C.
OpenCV will need to be setup with development headers on the path.

Most examples can be individually compiled with a single line:

g++ -O3 -Wall `pkg-config --cflags opencv` `pkg-config --libs opencv` -o median median_opencv.cxx videoCapturePlayer.cxx

Or compile them all at once by running:
./buildall.sh

Brian Thorne 2009 <brian.thorne@hitlabnz.org>
