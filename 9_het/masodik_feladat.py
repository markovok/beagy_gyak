import cv2
import time
import numpy as np
import imutils
from imutils.video import VideoStream

video_path = None
buffsize = 64
indx = 0

yellow_range = [(20, 100, 100), (30, 255, 255)]
path = np.zeros((buffsize, 2), dtype='int')

if video_path is None:
    vs = VideoStream().start()
    time.sleep(2)
else:
    vs = cv2.VideoCapture(video_path)

while True:
    frame = vs.read()
    frame = frame if video_path is None else frame[1]

    if frame is None:
        break

    frame = imutils.resize(frame, width=500)
    blur = cv2.GaussianBlur(frame, (9, 9), 0)
    hsv = cv2.cvtColor(blur, cv2.COLOR_BGR2HSV)

    mask = cv2.inRange(hsv, yellow_range[0], yellow_range[1])
    mask = cv2.erode(mask, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)

    cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)

    if len(cnts) > 0:
        cnt = max(cnts, key=cv2.contourArea)
        ((x, y), radius) = cv2.minEnclosingCircle(cnt)

        M = cv2.moments(cnt)
        if M["m00"] != 0:
            center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))

            if radius > 10:
                cv2.circle(frame, (int(x), int(y)), int(radius), (0, 255, 255), 2)
                cv2.circle(frame, center, 5, (0, 0, 255), -1)

            if indx < buffsize:
                path[indx] = (center[0], center[1])
                indx += 1
            else:
                path[0:indx - 1] = path[1:indx]
                path[indx - 1] = (center[0], center[1])

    for i in range(len(path)):
        if path[i][0] == 0 and path[i][1] == 0:
            continue

        radius = int(np.sqrt(len(path) / float(i + 1)) * 2.5)
        cv2.circle(frame, (path[i][0], path[i][1]), radius, (255, 0, 0), -1)

    cv2.imshow("Yellow Object Tracking", frame)
    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
        break