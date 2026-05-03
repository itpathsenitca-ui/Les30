import cv2
from utils.createSetting import range
while True:
        img1 = cv2.imread("./img/photo_5447115728428405764_y.jpg")
        img2 = cv2.imread("./img/photo_5447115728428405765_y.jpg")
        hsv1 = cv2.cvtColor(img1, cv2.COLOR_BGR2HSV)
        hsv2 = cv2.cvtColor(img2, cv2.COLOR_BGR2HSV)
        lower, upper = range()
        mask1 = cv2.inRange(hsv1,lower, upper)
        mask2 = cv2.inRange(hsv2, lower, upper)
        cv2.imshow('mask1', mask1)
        cv2.imshow('mask2', mask2)
        cv2.waitKey(0)