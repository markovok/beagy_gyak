from imutils.video import VideoStream
from pyzbar import pyzbar
import time
import cv2

vs = VideoStream().start()
time.sleep(2.0)

while True:
    frame = vs.read()


    barcodes = pyzbar.decode(frame)

    for barcode in barcodes:

        (x, y, w, h) = barcode.rect
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)


        bar_data = barcode.data.decode("utf-8")
        bar_type = barcode.type

        text = "{} ({})".format(bar_data, bar_type)
        cv2.putText(frame, text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

    cv2.imshow("Barcode & QR Scanner", frame)


    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
        break


cv2.destroyAllWindows()
vs.stop()