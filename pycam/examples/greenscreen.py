# Derived from Nirav Patel's Pygame Camera Tutorial

import pygame
from pycam import VideoCapturePlayer

class GreenScreen():
    def __init__(self):
        self.calibrated = False
        self.bgs = []
        
    def calibrate(self, snapshot):
        """
        Capture a bunch of background images and average them out.
        """
        if len(self.bgs) < 10:
            self.bgs.append(snapshot)
        else:
            # Average them out to remove noise, and save as background
            self.background = pygame.transform.average_surfaces(self.bgs)
            self.calibrated = True 
        
    
    def threshold(self, snapshot):
        dest = snapshot.copy()
        dest.fill((255,255,255))    # Make a black background
        threshold_value = 10        # How close to the existing color must each point be?
        pygame.transform.threshold(dest, snapshot, (0,0,0), [threshold_value]*3 ,(255,255,255),1, self.background)
        # Median filter would be good here to remove salt + pepper noise...  
        
        return dest #self.dest

    def process(self, snapshot):
        if not self.calibrated:
            return self.calibrate(snapshot)
        else:
            return self.threshold(snapshot)

if __name__ == "__main__":
    greenScreen = GreenScreen()
    
    vcp = VideoCapturePlayer(processFunction=greenScreen.process)
    vcp.main()
