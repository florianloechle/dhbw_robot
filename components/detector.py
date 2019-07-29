import numpy
import time
import cv2
import os
import imutils
import sys
import math
from shared.utils import get_random_colors


class NeuralNetworkDetector():

    # dnn image size
    dnn_size = 64

    # confidence level for a detection
    confidence = 0.75
    threshold = 0.25

    # read labels from file and save in array
    labels = open(
        './yolov3/64_v6/animal.names').read().strip().split("\n")

    # path to yolo weigths
    weightsPath = 'yolov3/64_v6/yolov3-tiny_62100.weights'

    # path to yolo config
    configPath = 'yolov3/64_v6/animal.cfg'

    def __init__(self, camera, debug=False):

        self.camera = camera
        self.isDebugMode = debug
        self.net = cv2.dnn.readNetFromDarknet(
            self.configPath, self.weightsPath)
        self.layer_names = [self.net.getLayerNames()[i[0] - 1]
                            for i in self.net.getUnconnectedOutLayers()]

        # create window to show current frame
        if self.isDebugMode:
            cv2.namedWindow(self.__class__.__name__)
            cv2.moveWindow(self.__class__.__name__, 10, 10)

    def detect(self, target):
        frame = self.camera.get_frame()
        if frame is None:
            return
        height, width = frame.shape[:2]
        # Crop from {x, y, w, h } => {0, 0, 300, 400}
        frame = frame[int(height / 4):int(height * 0.75),
                      int(width / 4):int(width * 0.75)]
        found = False

        # construct a blob from the input frame and then perform a forward
        # pass of the YOLO object detector, giving us our bounding boxes
        # and associated probabilities
        blob = cv2.dnn.blobFromImage(
            frame, 1 / 255.0, (self.dnn_size, self.dnn_size), swapRB=True, crop=False)
        self.net.setInput(blob)

        # most CPU intensive part! processing image with DNN
        layerOutputs = self.net.forward(self.layer_names)

        # initialize our lists of detected bounding boxes, confidences, and class IDs, respectively
        boxes = []
        confidences = []
        classIDs = []

        # loop over each of the layer outputs
        for output in layerOutputs:
            # loop over each of the detections
            for detection in output:
                # extract the class ID and confidence (i.e., probability) of the current object detection
                scores = detection[5:]
                classID = numpy.argmax(scores)
                confidence = scores[classID]

                # filter out weak predictions by ensuring the detected
                # probability is greater than the minimum probability
                if confidence > self.confidence:

                    if self.isDebugMode:
                        # scale the bounding box coordinates back relative to
                        # the size of the image, keeping in mind that YOLO
                        # actually returns the center (x, y)-coordinates of
                        # the bounding box followed by the boxes' width and
                        # height
                        (H, W) = frame.shape[:2]
                        box = detection[0:4] * numpy.array([W, H, W, H])
                        (centerX, centerY, width, height) = box.astype("int")

                        # use the center (x, y)-coordinates to derive the top
                        # and and left corner of the bounding box
                        x = int(centerX - (width / 2))
                        y = int(centerY - (height / 2))

                        # update our list of bounding box coordinates,
                        # confidences, and class IDs
                        boxes.append([x, y, int(width), int(height)])

                    confidences.append(float(confidence))
                    classIDs.append(classID)

        if len(classIDs) > 0:
            if target == self.labels[classIDs[0]]:
                found = True

        if self.isDebugMode:
            # apply non-maxima suppression to suppress weak, overlapping
            # bounding boxes
            idxs = cv2.dnn.NMSBoxes(
                boxes, confidences, self.confidence, self.threshold)
            self.show_debug_window(frame, idxs, (classIDs, confidences, boxes))

        return found

    def show_debug_window(self, frame, idxs, results):
        classIDs, confidences, boxes = results
        # ensure at least one detection exists
        if len(idxs) > 0:
            # loop over the indexes we are keeping
            for i in idxs.flatten():
                # extract the bounding box coordinates
                (x, y) = (boxes[i][0], boxes[i][1])
                (w, h) = (boxes[i][2], boxes[i][3])

                # draw a bounding box rectangle and label on the frame
                cv2.rectangle(frame, (x, y), (x + w, y + h), [0, 255, 0], 8)
                text = "{}: {:.4f}".format(
                    self.labels[classIDs[i]], confidences[i])
                cv2.putText(frame, text, (x, y - 5),
                            cv2.FONT_HERSHEY_SIMPLEX, 1.3, [0, 255, 0], 4)

        #frame = imutils.resize(frame, height=640, width=480)
        cv2.imshow(self.__class__.__name__, frame)
        cv2.waitKey(1)
