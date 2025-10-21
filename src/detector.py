
# src/detector.py
import cv2
import numpy as np
from features import FeatureExtractor
from matcher import FeatureMatcher

class TrafficLightDetector:
    def __init__(self, templates=None):
        """
        templates: list of tuples (template_image, keypoints, descriptors)
        """
        self.colors = {
            "red": ((0, 100, 100), (10, 255, 255)),
            "yellow": ((20, 100, 100), (30, 255, 255)),
            "green": ((40, 50, 50), (90, 255, 255))
        }

        self.feature_extractor = FeatureExtractor(method="SIFT")
        self.matcher = FeatureMatcher(method="BF")
        self.templates = templates if templates is not None else []

    def detect(self, frame):
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        detections = []

        for color_name, (lower, upper) in self.colors.items():
            mask = cv2.inRange(hsv, np.array(lower), np.array(upper))
            contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
            
            for cnt in contours:
                area = cv2.contourArea(cnt)
                if area > 50:
                    x, y, w, h = cv2.boundingRect(cnt)
                    roi = frame[y:y+h, x:x+w]
                    gray_roi = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)

                    # --- FEATURE EXTRACTION ---
                    keypoints, descriptors = self.feature_extractor.detect_and_compute(gray_roi)

                    # --- FEATURE MATCHING WITH TEMPLATES ---
                    is_valid = False
                    for temp_kp, temp_desc in self.templates:
                        matches = self.matcher.match(descriptors, temp_desc)
                        if len(matches) > 5:  # threshold for confident match
                            is_valid = True
                            break

                    if not is_valid:
                        continue  # skip this ROI if it doesn't match any template

                    # --- OPTIONAL: draw keypoints ---
                    # roi_with_kp = self.feature_extractor.draw_keypoints(roi, keypoints)
                    # frame[y:y+h, x:x+w] = roi_with_kp

                    # --- SET BGR COLOR FOR DISPLAY ---
                    if color_name == "red":
                        bgr = (0, 0, 255)
                    elif color_name == "yellow":
                        bgr = (0, 255, 255)
                    else:
                        bgr = (0, 255, 0)

                    detections.append((x, y, w, h, bgr, keypoints, descriptors))

        return detections
