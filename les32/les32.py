import cv2
cv2.namedWindow('setting')
def noth(x):
    pass
cv2.createTrackbar("Hmin","setting",0,255,noth)
cv2.createTrackbar("Smin","setting",0,255,noth)
cv2.createTrackbar("Vmin","setting",0,255,noth)
cv2.createTrackbar("Hmax","setting",0,255,noth)
cv2.createTrackbar("Smax","setting",0,255,noth)
cv2.createTrackbar("Vmax","setting",0,255,noth)
def range():
    return  (cv2.getTrackbarPos("Hmin","setting"),
                cv2.getTrackbarPos("Smin","setting"),
                cv2.getTrackbarPos("Vmin", "setting"),)
(cv2.getTrackbarPos("Hmax","setting"),
                cv2.getTrackbarPos("Smax","setting"),
                cv2.getTrackbarPos("Vmax", "setting"),)