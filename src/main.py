# import cv2
# import time
# from detector import TrafficLightDetector
# from calibrate import CameraCalibrator
# from tracker import Tracker
# from utils import load_templates, draw_detections
# from signal_controller import SignalController
# from traffic_density import TrafficDensityEstimator
# from performance_logger import PerformanceLogger  # ✅ NEW

# def main():
#     # 1️⃣ Video input (use test video or webcam)
#     cap = cv2.VideoCapture("/Users/raman/Projects/Labs/cvLab/traffic-control/data/test_videos/sample1.mp4")  # change as needed

#     if not cap.isOpened():
#         print("❌ Cannot open camera/video")
#         return

#     # 2️⃣ Load templates for signal detection
#     templates = load_templates("data/templates")
    
#     # 3️⃣ Initialize all modules
#     detector = TrafficLightDetector(templates=templates)
#     tracker = Tracker()
#     calibrator = CameraCalibrator()  # optional
#     controller = SignalController(min_green=5, yellow_time=2, red_time=5)
#     density_estimator = TrafficDensityEstimator()
#     logger = PerformanceLogger("performance_log.csv")  # ✅ NEW

#     prev_time = time.time()

#     print("✅ Smart Traffic Control System Initialized")

#     while True:
#         ret, frame = cap.read()
#         if not ret:
#             break

#         # Optional: undistort
#         # frame = calibrator.undistort(frame)

#         # ---- Step 1: Density-based congestion detection ----
#         vehicle_count, hog_density, density_frame = density_estimator.estimate_density(frame)

#         # ---- Step 2: Traffic light detection (template-based) ----
#         detections = detector.detect(frame)
#         tracked = tracker.update(detections)

#         # ---- Step 3: Compute time delta ----
#         curr_time = time.time()
#         dt = curr_time - prev_time
#         prev_time = curr_time

#         # ---- Step 4: Update traffic signal based on congestion ----
#         signal = controller.update(vehicle_count, dt=dt)

#         # ---- Step 5: Overlay traffic light simulation ----
#         cv2.rectangle(density_frame, (10, 10), (60, 140), (50, 50, 50), -1)
#         colors = {"RED": (0, 0, 255), "YELLOW": (0, 255, 255), "GREEN": (0, 255, 0)}
#         y_positions = {"RED": 20, "YELLOW": 70, "GREEN": 120}

#         for light in ["RED", "YELLOW", "GREEN"]:
#             color = colors[light] if signal == light else (100, 100, 100)
#             cv2.circle(density_frame, (35, y_positions[light]), 20, color, -1)

#         # ---- Step 6: Display analytics ----
#         cv2.putText(density_frame, f"Vehicles: {vehicle_count}", (10, 170),
#                     cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
#         cv2.putText(density_frame, f"HOG Density: {hog_density:.3f}", (10, 200),
#                     cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
#         cv2.putText(density_frame, f"Signal: {signal}", (10, 230),
#                     cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 0), 2)

#         # ---- Step 7: Log performance ---- ✅ NEW
#         logger.update(vehicle_count)
#         # Log every ~5 seconds (non-strict)
#         if int(time.time()) % 5 == 0:
#             logger.log()

#         # ---- Step 8: Show live output ----
#         cv2.imshow("Smart Traffic Control System", density_frame)

#         if cv2.waitKey(1) & 0xFF == ord('q'):
#             break

#     # ---- Step 9: Wrap up ----
#     logger.log()  # Final log
#     cap.release()
#     cv2.destroyAllWindows()
#     print("🏁 Processing complete. Logs saved to performance_log.csv")

# if __name__ == "__main__":
#     main()


# src/main.py
import cv2
import time
from detector import TrafficLightDetector
from calibrate import CameraCalibrator
from tracker import Tracker
from utils import load_templates, draw_detections
from signal_controller import SignalController
from traffic_density import TrafficDensityEstimator
from performance_logger import PerformanceLogger  # Optional, for logging analytics

def main():
    # 1️⃣ Video input (use test video or webcam)
    cap = cv2.VideoCapture("/Users/raman/Projects/Labs/cvLab/traffic-control/data/test_videos/sample1.mp4")  # Update path if needed

    if not cap.isOpened():
        print("❌ Cannot open camera/video")
        return

    # 2️⃣ Load templates for traffic light detection
    templates = load_templates("../data/templates")  # relative to src/

    # 3️⃣ Initialize all modules
    detector = TrafficLightDetector(templates=templates)
    tracker = Tracker()
    calibrator = CameraCalibrator()  # optional: load precomputed calibration
    controller = SignalController(base_green=5, yellow_time=2, base_red=5)
    density_estimator = TrafficDensityEstimator()
    logger = PerformanceLogger("performance_log.csv")  # Optional logging

    prev_time = time.time()
    print("✅ Smart Traffic Control System Initialized")

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Optional: undistort frame if using calibration
        # frame = calibrator.undistort(frame)

        # ---- Step 1: Density-based congestion detection ----
        vehicle_count, hog_density, density_frame = density_estimator.estimate_density(frame)

        # ---- Step 2: Traffic light detection (template-based) ----
        detections = detector.detect(frame)
        tracked = tracker.update(detections)

        # ---- Step 3: Compute time delta ----
        curr_time = time.time()
        dt = curr_time - prev_time
        prev_time = curr_time

        # ---- Step 4: Update traffic signal dynamically based on congestion ----
        signal, time_left = controller.update(vehicle_count, dt=dt)
        print(f"Signal: {signal}, Vehicles: {vehicle_count}, Time left: {time_left:.1f}s")


        # ---- Step 5: Overlay traffic light simulation ----
        cv2.rectangle(density_frame, (10, 10), (60, 140), (50, 50, 50), -1)
        colors = {"RED": (0, 0, 255), "YELLOW": (0, 255, 255), "GREEN": (0, 255, 0)}
        y_positions = {"RED": 20, "YELLOW": 70, "GREEN": 120}

        for light in ["RED", "YELLOW", "GREEN"]:
            color = colors[light] if signal == light else (100, 100, 100)
            cv2.circle(density_frame, (35, y_positions[light]), 20, color, -1)

        # ---- Step 6: Display analytics ----
        cv2.putText(density_frame, f"Vehicles: {vehicle_count}", (10, 170),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
        cv2.putText(density_frame, f"HOG Density: {hog_density:.3f}", (10, 200),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
        cv2.putText(density_frame, f"Signal: {signal}", (10, 230),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 0), 2)
        cv2.putText(density_frame, f"Time left: {max(0, time_left):.1f}s", (10, 260),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)

        # ---- Step 7: Log performance ----
        logger.update(vehicle_count)
        # Optional: log every few seconds
        if int(time.time()) % 5 == 0:
            logger.log()

        # ---- Step 8: Show live output ----
        cv2.imshow("Smart Traffic Control System", density_frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # ---- Step 9: Wrap up ----
    logger.log()  # final log save
    cap.release()
    cv2.destroyAllWindows()
    print("🏁 Processing complete. Logs saved to performance_log.csv")


if __name__ == "__main__":
    main()
