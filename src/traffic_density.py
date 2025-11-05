# src/traffic_density.py
import cv2
import numpy as np
from vehicle_detector import VehicleDetector

class TrafficDensityEstimator:
    def __init__(self):
        # Initialize the vehicle detector
        self.vehicle_detector = VehicleDetector()

    def estimate_density(self, frame, roi):
        """
        Estimates vehicle density within a specific region of interest (ROI).
        
        :param frame: The input video frame.
        :param roi: A numpy array of points defining the polygon for the ROI.
        :return: A tuple containing the vehicle count and a list of their contours.
        """
        vehicle_count, contours = self.vehicle_detector.detect_vehicles(frame, roi)
        return vehicle_count, contours
