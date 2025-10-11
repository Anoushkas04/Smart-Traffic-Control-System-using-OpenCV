# src/traffic_density.py
import cv2
import numpy as np

class TrafficDensityEstimator:
    def __init__(self):
        # Background subtractor for motion detection
        self.bg_subtractor = cv2.createBackgroundSubtractorMOG2(history=300, varThreshold=50, detectShadows=True)

    def estimate_density(self, frame, roi):
        """
        Estimates vehicle density within a specific region of interest (ROI).
        
        :param frame: The input video frame.
        :param roi: A numpy array of points defining the polygon for the ROI.
        :return: A tuple containing the vehicle count and a list of valid contours.
        """
        # Create a mask for the ROI
        mask = np.zeros(frame.shape[:2], dtype="uint8")
        cv2.fillPoly(mask, [roi], 255)
        
        # Apply the mask to focus on the ROI
        roi_frame = cv2.bitwise_and(frame, frame, mask=mask)

        # Convert to grayscale and apply blur
        gray = cv2.cvtColor(roi_frame, cv2.COLOR_BGR2GRAY)
        gray_blur = cv2.GaussianBlur(gray, (5, 5), 0)

        # ---- Step 1: Background subtraction on the ROI ----
        fg_mask = self.bg_subtractor.apply(gray_blur)

        # Morphological operations to clean noise
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
        fg_mask = cv2.morphologyEx(fg_mask, cv2.MORPH_OPEN, kernel)
        fg_mask = cv2.morphologyEx(fg_mask, cv2.MORPH_DILATE, kernel)

        # ---- Step 2: Contour Detection within the ROI ----
        contours, _ = cv2.findContours(fg_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        vehicle_count = 0
        valid_contours = []
        for cnt in contours:
            area = cv2.contourArea(cnt)
            if area > 600:  # Filter out small noise blobs
                vehicle_count += 1
                valid_contours.append(cnt)

        return vehicle_count, valid_contours