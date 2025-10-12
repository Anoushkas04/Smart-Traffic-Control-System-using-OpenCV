# Traffic Control System Improvement Plan

This document outlines the plan to refactor the traffic control system to address key logical flaws.

## To Do

### 3. Improve Vehicle Counting to Include Stopped Cars
- [ ] **Replace Background Subtraction:** The current method of using background subtraction is flawed as it ignores stationary vehicles. It will be replaced with a proper object detection model.
- [ ] **Integrate Object Detection Model:**
    - Use a pre-trained model (like YOLO) to detect vehicles (cars, trucks, buses) in the frame.
    - The `estimate_density` function will be updated to use this model for counting. This provides a much more accurate count of all vehicles, moving or stationary.
> **Note:** Attempted to implement with YOLO but encountered persistent OpenCV errors. Rolling back to the background subtraction method for now to ensure the rest of the system is functional.

## Done

### 1. Redesign for Multi-Signal Intersection Management
- [x] **Define Intersection Structure:** Modeled a 4-way intersection with two conflicting phases (North-South and East-West).
- [x] **Update `SignalController`:**
    - Modified the controller to manage the state of the entire intersection (e.g., which phase is green).
    - The `update` method now accepts density data for all approaches.
    - Implemented logic to switch phases based on demand, ensuring minimum green times and safe transitions.

### 2. Implement Region of Interest (ROI) for Density Calculation
- [x] **Define ROIs:** In `main.py`, defined placeholder polygonal ROIs for each of the 4 incoming lanes.
- [x] **Isolate ROIs:** The main loop now processes each ROI separately to get a vehicle count per lane.
- [x] **Modify `TrafficDensityEstimator`:** Updated the `estimate_density` method to operate within a given ROI mask instead of the full frame.
