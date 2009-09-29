#log# Automatic Logger file. *** THIS MUST BE THE FIRST LINE ***
#log# DO NOT CHANGE THIS LINE OR THE TWO BELOW
#log# opts = Struct({'__allownew': True, 'logfile': 'ipython-logs/VidCapTest.py'})
#log# args = []
#log# It is safe to make manual edits below here.
#log#-----------------------------------------------------------------------
_ip.system("ls -F ")
_ip.magic("pwd ")
import camera
cam = camera.Camera('pygame')
im = cam.get_image()
camera.list_cameras()
camera.size
#?camera.list_cameras
camera.list_cameras()
im = cam.get_image()
#?im = cam.get_image?
#?cam.get_image?
cam.imageType
cam.imageType == "pygame"
a = camera.hg.cvQueryFrame(cam.capture)
a
#?a
a = camera.hg.cvQueryFrame(cam.capture)
cam.capture
#?cam.capture
cam = camera.Camera('pygame')
cam
a = [2]
a.si
len(a)
a
not a
