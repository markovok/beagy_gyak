from imutils.video import VideoStream
import numpy as np
import imutils
import time
import cv2

model_path = "/home/sutoj/embedded/mobilenet.onnx"
conf_limit = 0.25

CLASSES = {
    1: "person", 2: "bicycle", 3: "car", 4: "motorcycle", 5: "airplane",
    6: "bus", 7: "train", 8: "truck", 9: "boat", 10: "traffic light",
    11: "fire hydrant", 13: "stop sign", 14: "parking meter", 15: "bench",
    16: "bird", 17: "cat", 18: "dog", 19: "horse", 20: "sheep",
    21: "cow", 22: "elephant", 23: "bear", 24: "zebra", 25: "giraffe",
    27: "backpack", 28: "umbrella", 31: "handbag", 32: "tie", 33: "suitcase",
    34: "frisbee", 35: "skis", 36: "snowboard", 37: "sports ball", 38: "kite",
    39: "baseball bat", 40: "baseball glove", 41: "skateboard", 42: "surfboard",
    43: "tennis racket", 44: "bottle", 46: "wine glass", 47: "cup", 48: "fork",
    49: "knife", 50: "spoon", 51: "bowl", 52: "banana", 53: "apple",
    54: "sandwich", 55: "orange", 56: "broccoli", 57: "carrot", 58: "hot dog",
    59: "pizza", 60: "donut", 61: "cake", 62: "chair", 63: "couch",
    64: "potted plant", 65: "bed", 67: "dining table", 70: "toilet", 72: "tv",
    73: "laptop", 74: "mouse", 75: "remote", 76: "keyboard", 77: "cell phone",
    78: "microwave", 79: "oven", 80: "toaster", 81: "sink", 82: "refrigerator",
    84: "book", 85: "clock", 86: "vase", 87: "scissors", 88: "teddy bear",
    89: "hair drier", 90: "toothbrush",
}

COLORS = np.random.uniform(0, 255, size=(max(CLASSES.keys()) + 1, 3))

net = cv2.dnn.readNetFromONNX(model_path)
output_names = net.getUnconnectedOutLayersNames()

vs = VideoStream().start()
time.sleep(2.0)

prev_time = time.time()

while True:
    frame = vs.read()
    if frame is None:
        break

    frame = imutils.resize(frame, width=800)
    (h, w) = frame.shape[:2]

    rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    input_tensor = np.expand_dims(rgb_image.astype(np.uint8), axis=0)

    net.setInput(input_tensor)
    output_values = net.forward(output_names)

    scores = output_values[2][0]
    class_ids = output_values[1][0]
    boxes = output_values[0][0]

    for i in range(len(scores)):
        confidence = scores[i]
        if confidence > conf_limit:
            idx = int(class_ids[i])
            ymin, xmin, ymax, xmax = boxes[i]

            startX = int(xmin * w)
            startY = int(ymin * h)
            endX = int(xmax * w)
            endY = int(ymax * h)

            label = "{}: {:.2f}%".format(CLASSES.get(idx, "Unknown"), confidence * 100)

            cv2.rectangle(frame, (startX, startY), (endX, endY), COLORS[idx], 2)
            y = startY - 15 if startY - 15 > 15 else startY + 15
            cv2.putText(frame, label, (startX, y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, COLORS[idx], 2)

    curr_time = time.time()
    fps = 1 / (curr_time - prev_time)
    prev_time = curr_time

    cv2.putText(frame, "FPS: {:.2f}".format(fps), (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

    cv2.imshow("Object Detection Stream", frame)

    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
        break

cv2.destroyAllWindows()
vs.stop()