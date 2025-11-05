# src/vehicle_detector.py

import cv2
import numpy as np
from vehicle_classifier import VehicleClassifier

def sliding_window(image, step_size, window_size):
    for y in range(0, image.shape[0] - window_size[1], step_size):
        for x in range(0, image.shape[1] - window_size[0], step_size):
            yield (x, y, image[y:y + window_size[1], x:x + window_size[0]])

def non_max_suppression(boxes, overlap_thresh):
    if len(boxes) == 0:
        return []

    if boxes.dtype.kind == "i":
        boxes = boxes.astype("float")

    pick = []
    x1 = boxes[:, 0]
    y1 = boxes[:, 1]
    x2 = boxes[:, 2]
    y2 = boxes[:, 3]

    area = (x2 - x1 + 1) * (y2 - y1 + 1)
    idxs = np.argsort(y2)

    while len(idxs) > 0:
        last = len(idxs) - 1
        i = idxs[last]
        pick.append(i)

        xx1 = np.maximum(x1[i], x1[idxs[:last]])
        yy1 = np.maximum(y1[i], y1[idxs[:last]])
        xx2 = np.minimum(x2[i], x2[idxs[:last]])
        yy2 = np.minimum(y2[i], y2[idxs[:last]])

        w = np.maximum(0, xx2 - xx1 + 1)
        h = np.maximum(0, yy2 - yy1 + 1)

        overlap = (w * h) / area[idxs[:last]]

        idxs = np.delete(idxs, np.concatenate(([last], np.where(overlap > overlap_thresh)[0])))

    return boxes[pick].astype("int")

class VehicleDetector:
    def __init__(self, history=300, dist2Threshold=200.0, probability_threshold=0.7, 
                 window_size=(64, 64), step_size=32, full_scan_interval=15):
        self.bg_subtractor = cv2.createBackgroundSubtractorKNN(history=history, dist2Threshold=dist2Threshold, detectShadows=True)
        self.classifier = VehicleClassifier()
        self.probability_threshold = probability_threshold
        self.window_size = window_size
        self.step_size = step_size
        self.full_scan_interval = full_scan_interval
        self.frame_count = 0

    def detect_vehicles(self, frame, roi_poly):
        self.frame_count += 1
        all_detections = []

        # --- Fast motion-based detection (every frame) ---
        mask = np.zeros(frame.shape[:2], dtype="uint8")
        cv2.fillPoly(mask, [roi_poly], 255)
        roi_frame = cv2.bitwise_and(frame, frame, mask=mask)
        fg_mask = self.bg_subtractor.apply(roi_frame)
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
        fg_mask = cv2.morphologyEx(fg_mask, cv2.MORPH_OPEN, kernel, iterations=3)
        fg_mask = cv2.dilate(fg_mask, kernel, iterations=3)
        contours, _ = cv2.findContours(fg_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        for cnt in contours:
            if cv2.contourArea(cnt) > 500:
                x, y, w, h = cv2.boundingRect(cnt)
                vehicle_patch = frame[y:y+h, x:x+w]
                if vehicle_patch.shape[0] > 0 and vehicle_patch.shape[1] > 0:
                    prediction, probability = self.classifier.classify(vehicle_patch)
                    if (prediction == 1 or prediction == 2) and probability > self.probability_threshold:
                        all_detections.append((x, y, x + w, y + h))

        # --- Slow sliding window detection (every N frames) ---
        if self.frame_count % self.full_scan_interval == 0:
            roi_x, roi_y, roi_w, roi_h = cv2.boundingRect(roi_poly)
            roi = frame[roi_y:roi_y + roi_h, roi_x:roi_x + roi_w]

            for (x, y, window) in sliding_window(roi, self.step_size, self.window_size):
                if window.shape[0] != self.window_size[1] or window.shape[1] != self.window_size[0]:
                    continue

                prediction, probability = self.classifier.classify(window)

                if (prediction == 1 or prediction == 2) and probability > self.probability_threshold:
                    all_detections.append((x + roi_x, y + roi_y, x + roi_x + self.window_size[0], y + roi_y + self.window_size[1]))

        # --- Non-Maximum Suppression ---
        bounding_boxes = non_max_suppression(np.array(all_detections), 0.3)
        vehicle_count = len(bounding_boxes)

        return vehicle_count, bounding_boxes
