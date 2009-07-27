# Derived from Nirav Patel's Pygame Camera Tutorial

# When the color desired is in the middle box, click the mouse to start thresholding.

import pygame
from VideoCapturePlayer import VideoCapturePlayer

class Thresholder():
    def __init__(self):
        self.calibrated = False
        
    def calibrate(self, snapshot):
        """
        Draws a rectangle in the middle of the screen, the average colour of which is 
        drawn in the top left hand corner in a solid box. Once the desired colour is 
        placed in the middle, click the mouse to "lock" the colour into the thresholder.
        """
        dest = snapshot.copy()
        # draw a rectangle on the screen
        location = ((snapshot.get_width()/2)-25, (snapshot.get_height()/2)-25, 50, 50)
        crect = pygame.draw.rect(dest, (0,255,0), location, 2)
        
        # get the colour in that rect
        self.ccolor = pygame.transform.average_color(snapshot,crect)
        
        # fill upper left corner with that color
        pygame.draw.rect(dest,self.ccolor,(0,0,50,50),0)
        
        # check to see if mouse has been pressed, if so use current color
        if pygame.event.peek(pygame.MOUSEBUTTONDOWN):
            self.calibrated = True
        return dest
    
    def threshold(self, snapshot):
        dest = snapshot.copy()
        print pygame.transform.threshold(dest, snapshot, self.ccolor, (30,30,30) ,(0,0,0),1)   
        return dest #self.dest

    def process(self, snapshot):
        if not self.calibrated:
            return self.calibrate(snapshot)
        else:
            return self.threshold(snapshot)

if __name__ == "__main__":
    thresholder = Thresholder()
    
    vcp = VideoCapturePlayer(processFunction=thresholder.process)
    vcp.main()
