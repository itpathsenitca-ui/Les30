import cv2

tv = cv2.VideoCapture(
    "https://edge55.dc.beltelecom.by/ngtrk/_definst_/smil:belarus1.smil/chunklist_w_b1460000_sleng.m3u8"
)
while True:
    ret, frame = tv.read()
    frame = cv2.resize(frame, (640, 360))
    cv2.imshow("frame", frame)
    cv2.waitKey(1000 // 30)
