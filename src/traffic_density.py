# src/traffic_density.py
import cv2
import numpy as np

class TrafficDensityEstimator:
    def __init__(self):
        # Initialize HOG Descriptor
        self.hog = cv2.HOGDescriptor()
        # Background subtractor for motion detection
        self.bg_subtractor = cv2.createBackgroundSubtractorMOG2(history=300, varThreshold=50, detectShadows=True)

    def compute_hog_density(self, gray_frame):
        """
        Computes HOG-based gradient density to detect areas with high vehicle presence.
        Returns a density map and mean gradient magnitude.
        """
        # Resize for performance
        resized = cv2.resize(gray_frame, (128, 128))
        hog_features = self.hog.compute(resized)

        # Use mean gradient magnitude as density indicator
        hog_density = np.mean(hog_features)
        return hog_density

    def estimate_density(self, frame):
        """
        Combines HOG-based feature density and contour-based motion detection.
        Returns vehicle count, density value, and annotated frame.
        """
        # Convert to grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray_blur = cv2.GaussianBlur(gray, (5, 5), 0)

        # ---- Step 1: Background subtraction ----
        fg_mask = self.bg_subtractor.apply(gray_blur)

        # Morphological operations to clean noise
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
        fg_mask = cv2.morphologyEx(fg_mask, cv2.MORPH_OPEN, kernel)
        fg_mask = cv2.morphologyEx(fg_mask, cv2.MORPH_DILATE, kernel)

        # ---- Step 2: Contour Detection ----
        contours, _ = cv2.findContours(fg_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        vehicle_count = 0
        for cnt in contours:
            area = cv2.contourArea(cnt)
            if area > 600:  # Filter out small noise blobs
                vehicle_count += 1
                x, y, w, h = cv2.boundingRect(cnt)
                cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 255, 0), 2)

        # ---- Step 3: HOG Feature Density ----
        hog_density = self.compute_hog_density(gray)

        # Annotate frame
        cv2.putText(frame, f"HOG Density: {hog_density:.3f}", (20, 60),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
        cv2.putText(frame, f"Vehicles: {vehicle_count}", (20, 90),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

        return vehicle_count, hog_density, frame
