# setup.py for compiling a cpp python extension with swig...
#
#  python setup.py build
#
# At the moment I have to link in the extra_objects... not sure if this is how it should be done?
#
# Brian Thorne 2009

import distutils
from os import system
from distutils.core import setup, Extension

testCommand = "print 'Testing import';import helloWorld;print('Imported helloWorld');import removeCornealReflection;print('Imported removeCornealReflection');import svd;print('Imported svd');import ransacEllipse;print('Imported ransacEllipse');import cvEyeTrack;print('Imported cvEyeTrack :-D');helloWorld.wait4in();"


print("Making the C/C++ objects first.")
# Read: disgusting hack...
system("""g++ -shared -I/usr/include/opencv -I/usr/include/python2.6 -L/usr/local/lib -L/usr/X11R6/lib -lm -lraw1394 -lcv -lcvaux -lhighgui -g -Wall -fPIC -c *.c *.cpp
""")

print('Running swig via distutils')

hackDIR = ""#"/home/brian/dev/swig/linkedLib/build/temp.linux-x86_64-2.6/"  # why is this needed like this? YUCK!

cvEyeExt = Extension(
    "_cvEyeTrack",
    sources = ["cvEyeTracker.i","cvEyeTracker.cpp"],
    swig_opts=["-c++"],
    extra_objects = [
        hackDIR + "svd.o",
        hackDIR + "ransac_ellipse.o",
        hackDIR + "remove_corneal_reflection.o" 
    ],
    library_dirs=['/usr/local/lib/opencv'],
    libraries=['cv','highgui','cvaux','cvaux'],
    include_dirs = ['/usr/local/include/opencv','/usr/include']
)

# Note the svd object is made from a C file, but ransac_ellipse is from C++
ransacExt = Extension( 
            "_ransacEllipse",
            sources = ["ransac_ellipse.i","ransac_ellipse.cpp"],
            extra_objects = [hackDIR + "svd.o"],
            swig_opts=["-c++"],
            library_dirs=['/usr/local/lib/opencv'],
            libraries=['cv','highgui','cvaux','cvaux'],
            include_dirs = ['/usr/local/include/opencv']
            )

sampleCpp = Extension(
            "_helloWorld",
            sources = ["HelloWorld.i","Hello World.cpp"],
            swig_opts=["-c++"],
            )

removeCornealRefl = Extension(
            "_removeCornealReflection",
            sources = ["remove_corneal_reflection.i","remove_corneal_reflection.cpp"],
            swig_opts=["-c++"],
            library_dirs=['/usr/local/lib/opencv'],
            libraries=['cv','highgui','cvaux','cvaux'],
            include_dirs = ['/usr/local/include/opencv']
            )
svd = Extension(
            "_svd",
            sources = ["svd.i","svd.c"],
            )
            
setup(
    name = "Brian's C++ Library wrapped up all nice for python",
    author = 'Brian Thorne',
    author_email = 'hardbyte@gmail.com',
    license='GPL v3 :: GNU General Public License', 
    version = "0.1",
    ext_modules = [
        sampleCpp,
        svd,
        removeCornealRefl,
        ransacExt,
        cvEyeExt,
        ]
    )
print('Build complete (Check for errors!)\nRunning test now:')
system('python -c "%s"' % testCommand)
