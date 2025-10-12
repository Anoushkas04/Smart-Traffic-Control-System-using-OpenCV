# src/vehicle_detector.py
import cv2
from ultralytics import YOLO
import numpy as np

class VehicleDetector:
    def __init__(self, model_path='yolov8n.pt'):
        """
        Initializes the vehicle detector with a YOLO model.
        
        :param model_path: Path to the pre-trained YOLO model file.
        """
        self.model = YOLO(model_path)
        # Define the classes for vehicles we want to detect
        self.vehicle_classes = [2, 3, 5, 7]  # car, motorcycle, bus, truck

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

        # Perform inference on the ROI
        results = self.model(roi_frame, verbose=False)
        
        vehicle_count = 0
        bounding_boxes = []
        
        for result in results:
            for box in result.boxes:
                # Check if the detected object is a vehicle
                if box.cls in self.vehicle_classes:
                    x1, y1, x2, y2 = map(int, box.xyxy[0])
                    bounding_boxes.append((x1, y1, x2, y2))
                    vehicle_count += 1
                    
        return vehicle_count, bounding_boxes

    def draw_boxes(self, frame, bounding_boxes):
        """
        Draws bounding boxes on the frame.
        
        :param frame: The frame to draw on.
        :param bounding_boxes: A list of bounding boxes to draw.
        :return: The frame with bounding boxes drawn.
        """
        for (x1, y1, x2, y2) in bounding_boxes:
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
        return frame
