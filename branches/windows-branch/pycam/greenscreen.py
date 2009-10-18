# Derived from Nirav Patel's Pygame Camera Tutorial

import pygame
from VideoCapturePlayer import VideoCapturePlayer

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
        pygame.transform.threshold(dest, snapshot, (0,255,0),(30,30,30),(0,0,0),1,self.background)
		#(0,0,0), (100,100,100,0) ,(255,255,255), 1, self.background,False)   
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
