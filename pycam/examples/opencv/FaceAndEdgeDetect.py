#!/usr/bin/python
from pycam import VideoCapturePlayer
from pycam import pygameFaceDetect
from pycam.filters import outlineEdges

def process(surf):
    faces = pygameFaceDetect.getFaces(surf)
    surf = outlineEdges(surf)
    if faces:
        pygameFaceDetect.drawFacesOnSurface(surf, faces)
    return surf

if __name__ == "__main__":
    vcp = VideoCapturePlayer(processFunction=process)
    vcp.main()
    pygame.quit()
    
