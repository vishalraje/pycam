#!/usr/bin/env python

from VideoCapturePlayer import VideoCapturePlayer as VCP

from opencv import cv


def threshold_image(image, n=[]):
    """Record the first 5 images to get a background, then diff current frame with the last saved frame.
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
    
    """The threshold value determines the amount of "Change" required 
    before something will show up"""
    thresholdValue = 50     # 32 
    cv.cvThreshold( differenceImage, differenceImage, thresholdValue, 255, cv.CV_THRESH_BINARY )
    
    # Convert to one channel
    gray = cv.cvCreateImage( cv.cvGetSize(differenceImage), 8, 1 )
    cv.cvCvtColor( differenceImage, gray, cv.CV_BGR2GRAY )   
    
    # Use median filter to remove salt and pepper noise.
    cv.cvSmooth(gray, gray, cv.CV_MEDIAN, 15)
    
    # Dilate and the threshold image
    # It adds a border to the object.
    #cv.cvDilate(gray,gray, None, 9)
    
    # Add a bit of Blur to the threshold mask
    cv.cvSmooth(gray, gray, cv.CV_GAUSSIAN, 5)
    
    result  = cv.cvCloneMat( image)
    cv.cvSetZero(result)
    
    cv.cvAnd(image,image, result, gray)
    return result

if __name__ == "__main__":
    title = "Background Subtraction Output"
    VCP(threshold_image, title).main()
