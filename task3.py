import cv2
import pickle
from cvzone.FaceDetectionModule import FaceDetector

recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read('trained_model_persons.yml')

with open('labels.pickle', 'rb') as f:
    label_map = pickle.load(f)


TARGET_SIZE = (200, 200)
CONFIDENCE_THRESHOLD = 80
cap = cv2.VideoCapture(0)

detector = FaceDetector(minDetectionCon=0.7)  # минимальная уверенность детекции
while True:
    success, img = cap.read()
    img, bboxs = detector.findFaces(img)  # draw=False, чтобы не рисовать рамки автоматом

    if bboxs:
        for bbox in bboxs:
            x, y, w, h = bbox['bbox']
            x, y = max(0, x), max(0, y)
            w, h = min(w, img.shape[1] - x), min(h, img.shape[0] - y)

            face_img = img[y:y+h, x:x+w]

            gray = cv2.cvtColor(face_img, cv2.COLOR_BGR2GRAY)
            gray = cv2.equalizeHist(gray)
            face_resized = cv2.resize(gray, TARGET_SIZE)

            label, confidence = recognizer.predict(face_resized)

            if confidence < CONFIDENCE_THRESHOLD:
                name = label_map.get(label, "Unknown")
                box_color = (0, 255, 0)  # зелёный для своих
            else:
                name = "Unknown"
                box_color = (0, 0, 255)  # красный для чужих

            # Рисуем рамку и имя
            cv2.rectangle(img, (x, y), (x+w, y+h), box_color, 2)
            cv2.putText(img, f"{name} ({confidence:.1f})", (x, y-10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, box_color, 2)

    cv2.imshow("Real-time Face Recognition", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()