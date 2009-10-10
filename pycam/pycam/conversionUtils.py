try:
    from opencv import adaptors
except ImportError:
    import adaptors


from pygame import surfarray


def surf2CV(surf):
    """Given a surface, convert to an opencv format (cvMat)
    """
    numpyImage = surfarray.array3d(surf)
    cvImage = adaptors.NumPy2Ipl(numpyImage.transpose(1,0,2))
    return cvImage

def cv2SurfArray(cvMat):
    """Given an open cvMat convert it to a pygame surface pixelArray
    Should be able to call blit_array directly on this.
    """
    numpyImage = adaptors.Ipl2NumPy(cvMat)
    return numpyImage.transpose(1,0,2)

"""
These decorators could pass on other function args...
something like: *args=None, **argd=None

"""

class numpyFromSurf(object):
    """This decorator can be used to wrap a function that takes 
    and returns a numpy array into one that takes and retuns a
    pygame surface.
    """
    def __init__(self, f):
        self.f = f  
    
    def __call__(self, imageSurface):
        # Convert surface to ndarray - could also directly acess pixels...
        np_image = surfarray.array3d(imageSurface)
        
        # Call the original function
        np_image_filtered = self.f(np_image)
        
        # Convert back to surface
        return surfarray.make_surface(np_image_filtered)
        


class numpyFromOpenCV(object):
    """This decorator can be used to wrap a function that takes 
    and returns a numpy array into one that takes and retuns an
    opencv CvMat.
    """
    def __init__(self, f):
        self.f = f    

    def __call__(self, image):
        # Convert CvMat to ndarray
        np_image = adaptors.Ipl2NumPy(image)
        
        # Call the original function
        np_image_filtered = self.f(np_image)
        
        # Convert back to CvMat
        return adaptors.NumPy2Ipl(np_image_filtered)

