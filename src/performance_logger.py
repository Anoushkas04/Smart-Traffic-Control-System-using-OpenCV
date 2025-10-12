import time
import csv
import os

class PerformanceLogger:
    def __init__(self, log_file="performance_log.csv"):
        self.start_time = time.time()
        self.frame_count = 0
        self.total_vehicle_count = 0
        self.log_file = log_file

        # Prepare CSV
        if not os.path.exists(log_file):
            with open(log_file, mode='w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(["Timestamp", "FPS", "Avg Vehicle Count"])

    def update(self, vehicle_count):
        self.frame_count += 1
        self.total_vehicle_count += vehicle_count

    def log(self):
        elapsed = time.time() - self.start_time
        if elapsed == 0:
            return
        fps = self.frame_count / elapsed
        avg_vehicle_count = self.total_vehicle_count / max(self.frame_count, 1)

        with open(self.log_file, mode='a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([round(time.time(), 2), round(fps, 2), round(avg_vehicle_count, 2)])

        print(f"📊 FPS: {fps:.2f} | Avg Vehicles: {avg_vehicle_count:.2f}")

    def reset(self):
        self.start_time = time.time()
        self.frame_count = 0
        self.total_vehicle_count = 0