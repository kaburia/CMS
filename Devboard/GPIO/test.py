import cv2

cap = cv2.VideoCapture(cv2.CAP_V4L2)

while True:
    try:
        ret, frame = cap.read()

        cv2.imshow('Frame', frame)
    except KeyboardInterrupt:
        break