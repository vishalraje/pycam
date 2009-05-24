#!/usr/bin/python
from VideoCapturePlayer import *
import pygameFaceDetect
import edgeDetect

def process(surf):
    faces = pygameFaceDetect.getFaces(surf)
    surf = edgeDetect.edgeDetectionProcess(surf)
    if faces:
        pygameFaceDetect.drawFacesOnSurface(surf, faces)
    return surf

if __name__ == "__main__":
    vcp = VideoCapturePlayer(processFunction=process)
    vcp.main()
    pygame.quit()
    