echo "Building all C/C++ examples"

g++ -Wall `pkg-config --cflags opencv` `pkg-config --libs opencv` -o webcamShow webcamShow.c
echo "Built webcam snapshot example"

g++ -O3 -Wall `pkg-config --cflags opencv` `pkg-config --libs opencv` -o VCP video.cxx videoCapturePlayer.cxx
echo "Built video capture example"

g++ -O3 -Wall `pkg-config --cflags opencv` `pkg-config --libs opencv` -o median median_opencv.cxx videoCapturePlayer.cxx
echo "Built median filter example"

g++ -O3 -Wall `pkg-config --cflags opencv` `pkg-config --libs opencv` -o background_subtract background_subtract_opencv.cxx videoCapturePlayer.cxx
echo "Built background subtraction example"

g++ -O3 -Wall `pkg-config --cflags opencv` `pkg-config --libs opencv` -o blur blur_opencv.cxx videoCapturePlayer.cxx
echo "Built blur example"

echo "All examples built"
