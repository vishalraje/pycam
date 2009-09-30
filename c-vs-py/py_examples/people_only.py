"""
My plan was to draw just detected faces - nothing else.
Still got to implement this.
"""
from objectDetect import ObjectDetector
from back_sub_opencv import threshold_image
from VideoCapturePlayer import VideoCapturePlayer as VCP
from opencv.cv import cvPoint, cvRectangle, CV_RGB

face_detector = ObjectDetector("face")

def illuminate_faces(image):
    changed_image = threshold_image(image)
    faces = face_detector.detectObject(image)
    for face in faces:
        print( "Oject found at (x,y) = (%i,%i)" % (face.x*face_detector.image_scale,face.y*face_detector.image_scale) )
        pt1 = cvPoint(  int(face.x*face_detector.image_scale), int(face.y*face_detector.image_scale) )
        pt2 = cvPoint(  int((face.x*face_detector.image_scale + face.width*face_detector.image_scale)), 
                        int((face.y*face_detector.image_scale + face.height*face_detector.image_scale)) )
        cvRectangle( changed_image, pt1, pt2, CV_RGB(255,0,0), 3, 8, 0 )
    return changed_image

VCP(illuminate_faces).main()
