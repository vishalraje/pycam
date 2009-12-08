"""
This pygame module implements a menu interface where the user selects an
option by placing their hand over a certain box.
This is an early prototype for the open allure dialog system a collaborative
project between John Graves of Auckland University of Technology 
and Brian Thorne of HitLabNZ, University of Canterbury.

@author Brian Thorne <brian.thorne@hitlabnz.org>
"""
import pygame
from pycam import VideoCapturePlayer

class VisionDS():
    def __init__(self):
        self.calibrated = False
        self.bgs = []
        self.frames = 0
        
    def calibrate(self, snapshot):
        """
        Capture a bunch of background images and average them out.
        We take 50 frames (approx 5 seconds worth) and just discard - 
        this is to allow the camera to adjust to the light levels before
        we store the background.
        
        We require that the top third or so is empty and ideally has
        a static background.
        
        So we will show the webcam image, overlaid with instructions and an
        outline of a person.
        """
        if self.frames < 80:
            
            if self.frames > 50 and len(self.bgs) < 10:
                self.bgs.append(snapshot)
        else:
            # Average them out to remove noise, and save as background
            self.background = pygame.transform.average_surfaces(self.bgs)
            self.calibrated = True
        self.frames += 1
        
    
    def threshold(self, snapshot):
        dest = snapshot.copy()
        dest.fill((255,255,255))    # Make a black background
        threshold_value = 10        # How close to the existing colour must each point be?
        pygame.transform.threshold(dest, snapshot, (0,0,0), [threshold_value]*3 ,(255,255,255),1, self.background)
        # Median filter would be good here to remove salt + pepper noise...  
        
        return dest #self.dest

    def process(self, snapshot):
        if not self.calibrated:
            return self.calibrate(snapshot)
        else:
            return self.threshold(snapshot)

if __name__ == "__main__":
    ds = VisionDS()
    
    vcp = VideoCapturePlayer(processFunction=ds.process)
    vcp.main()
