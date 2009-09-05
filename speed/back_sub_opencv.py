#!/usr/bin/env python

from VideoCapturePlayer import VideoCapturePlayer as VCP

from opencv import cv


def threshold_image(image, n=[]):
    """Record the first 5 images
    """
    if len(n) < 5:
        # n[4] will be our background
        # First capture a few images
        n.append(cv.cvCloneMat(image))
        if len(n) == 5:
            # last time here 
            # could do averaging here.
            pass
        return image
        
    original = n[4]
    differenceImage  = cv.cvCloneMat( image )
    cv.cvAbsDiff( image, original, differenceImage )
    
    cv.cvThreshold( differenceImage, differenceImage, 32, 255, cv.CV_THRESH_BINARY )
    cv.cvSmooth(differenceImage, differenceImage, cv.CV_MEDIAN, 15)
   
    
    temp  = cv.cvCloneMat( image)
    cv.cvSetZero(temp)
    
    cv.cvAnd(differenceImage,image, temp)

    from IPython.Shell import IPShellEmbed 
    IPShellEmbed()()
    
    # Need to do this faster...
    """for row_n in xrange(image.rows):
        for col_n in xrange(image.cols):
            if differenceImage[row_n,col_n][0] > 0 or differenceImage[row_n,col_n][1] > 0 or differenceImage[row_n,col_n][2] > 0:
                temp[row_n,col_n] = image[row_n,col_n]
    """
    #from IPython.Shell import IPShellEmbed
    #ipshell = IPShellEmbed()
    #ipshell()
    return temp

if __name__ == "__main__":
    title = "Background Subtraction Output"
    VCP(threshold_image, title).main()
