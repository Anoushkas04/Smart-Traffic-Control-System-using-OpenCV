# src/tracker.py
class Tracker:
    def __init__(self):
        self.objects = []

    def update(self, detections):
        # For now, just return detections directly
        # Later, you can implement proper tracking (Kalman Filter, SORT, etc.)
        return detections
