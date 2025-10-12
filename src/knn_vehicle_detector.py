# src/knn_vehicle_detector.py
import cv2
import numpy as np

class KNNVehicleDetector:
    def __init__(self, history=300, dist2Threshold=200.0):
        """
        Initializes the vehicle detector with a KNN background subtractor.
        """
        self.bg_subtractor = cv2.createBackgroundSubtractorKNN(history=history, dist2Threshold=dist2Threshold, detectShadows=True)

    def detect_vehicles(self, frame, roi_poly):
        """
        Detects vehicles within a specified region of interest (ROI).
        
        :param frame: The input video frame.
        :param roi_poly: A numpy array of points defining the polygon for the ROI.
        :return: A tuple containing the count of detected vehicles and a list of their bounding boxes.
        """
        # Create a mask for the ROI
        mask = np.zeros(frame.shape[:2], dtype="uint8")
        cv2.fillPoly(mask, [roi_poly], 255)
        
        # Apply the mask to the frame
        roi_frame = cv2.bitwise_and(frame, frame, mask=mask)

        # Apply the background subtractor to get the foreground mask
        fg_mask = self.bg_subtractor.apply(roi_frame)

        # Morphological operations to clean up the mask
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
        fg_mask = cv2.morphologyEx(fg_mask, cv2.MORPH_OPEN, kernel, iterations=3)
        fg_mask = cv2.dilate(fg_mask, kernel, iterations=3)

        # Find contours of the detected objects
        contours, _ = cv2.findContours(fg_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        vehicle_count = 0
        bounding_boxes = []
        for cnt in contours:
            # Filter out small contours
            if cv2.contourArea(cnt) > 500:
                x, y, w, h = cv2.boundingRect(cnt)
                bounding_boxes.append((x, y, x + w, y + h))
                vehicle_count += 1
                    
        return vehicle_count, bounding_boxes
