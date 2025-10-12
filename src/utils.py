# src/utils.py
import os
import cv2
from features import FeatureExtractor

def load_templates(path="data/templates", method="SIFT"):
    """
    Load preprocessed template images and compute features.
    Returns list of (keypoints, descriptors).
    """
    extractor = FeatureExtractor(method=method)
    templates = []
    for fname in os.listdir(path):
        img = cv2.imread(os.path.join(path, fname), cv2.IMREAD_GRAYSCALE)
        if img is None:
            continue
        kp, desc = extractor.detect_and_compute(img)
        templates.append((kp, desc))
    return templates

def draw_detections(frame, detections):
    """
    Draw bounding boxes for detected traffic lights or vehicles.
    """
    for (x, y, w, h, color, *_ ) in detections:
        cv2.rectangle(frame, (x, y), (x+w, y+h), color, 2)
    return frame