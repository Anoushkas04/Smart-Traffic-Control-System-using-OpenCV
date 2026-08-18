# src/main.py
import os
import sys
import argparse
import cv2
import time
import numpy as np
from signal_controller import SignalController
from traffic_density import TrafficDensityEstimator
from performance_logger import PerformanceLogger

def main():
    parser = argparse.ArgumentParser(description="Smart Traffic Control System")
    parser.add_argument("--video", type=str, default=None, help="Path to input video file or webcam index (0, 1, etc.)")
    args = parser.parse_args()

    # 1️⃣ Resolve video source
    if args.video is not None:
        video_src = int(args.video) if args.video.isdigit() else args.video
    else:
        # Check standard relative locations
        candidate_paths = [
            'data/test_videos/sample6.mp4',
            'src/data/test_videos/sample6.mp4',
            os.path.join(os.path.dirname(__file__), 'data', 'test_videos', 'sample6.mp4')
        ]
        video_src = None
        for p in candidate_paths:
            if os.path.exists(p):
                video_src = p
                break
        if video_src is None:
            video_src = 0  # Fallback to webcam

    print(f"🎥 Loading video source: {video_src}")
    cap = cv2.VideoCapture(video_src)

    if not cap.isOpened():
        print(f"❌ Cannot open camera/video: {video_src}")
        return

    # 2️⃣ Get frame dimensions to define ROIs
    ret, frame = cap.read()
    if not ret:
        print("❌ Cannot read video stream.")
        return
    frame_height, frame_width, _ = frame.shape
    cap.set(cv2.CAP_PROP_POS_FRAMES, 0)  # Rewind video

    # 3️⃣ Define placeholder ROIs (MUST BE ADJUSTED FOR THE SPECIFIC VIDEO)
    roi_ns = np.array([
        (frame_width // 2 - 80, 0), (frame_width // 2 + 80, 0),
        (frame_width // 2 + 80, frame_height), (frame_width // 2 - 80, frame_height)
    ], np.int32)

    roi_ew = np.array([
        (0, frame_height // 2 - 70), (frame_width, frame_height // 2 - 70),
        (frame_width, frame_height // 2 + 70), (0, frame_height // 2 + 70)
    ], np.int32)

    rois = {'ns': roi_ns, 'ew': roi_ew}

    # 4️⃣ Initialize modules
    controller = SignalController(min_green_time=5, max_green_time=10, yellow_time=2, all_red_time=1)
    density_estimator = TrafficDensityEstimator()
    logger = PerformanceLogger("performance_log.csv")

    prev_time = time.time()
    print("✅ Smart Traffic Control System Initialized")

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        output_frame = frame.copy()
        densities = {}

        # ---- Step 1: Density detection for each ROI ----
        for name, roi_poly in rois.items():
            cv2.polylines(output_frame, [roi_poly], isClosed=True, color=(255, 255, 0), thickness=2)
            vehicle_count, bounding_boxes = density_estimator.estimate_density(frame, roi_poly)
            densities[name] = vehicle_count
            for box in bounding_boxes:
                x1, y1, x2, y2 = box
                cv2.rectangle(output_frame, (x1, y1), (x2, y2), (0, 255, 0), 2)

        # ---- Step 2: Compute time delta ----
        curr_time = time.time()
        dt = curr_time - prev_time
        prev_time = curr_time

        # ---- Step 3: Update traffic signal based on congestion ----
        signal_states = controller.update(densities, dt)
        print(f"Phase: {controller.state}, NS Vehicles: {densities.get('ns', 0)}, EW Vehicles: {densities.get('ew', 0)}")

        # ---- Step 4: Overlay traffic light simulation ----
        signal_positions = {
            'north': (frame_width // 2, 40),
            'south': (frame_width // 2, frame_height - 40),
            'east': (frame_width - 40, frame_height // 2),
            'west': (40, frame_height // 2)
        }
        color_map = {"RED": (0, 0, 255), "YELLOW": (0, 255, 255), "GREEN": (0, 255, 0)}

        for direction, position in signal_positions.items():
            color_name = signal_states.get(direction, 'RED')
            cv2.circle(output_frame, position, 20, color_map[color_name], -1)

        # ---- Step 5: Display analytics ----
        cv2.putText(output_frame, f"NS Vehicles: {densities.get('ns', 0)}", (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        cv2.putText(output_frame, f"EW Vehicles: {densities.get('ew', 0)}", (10, 60),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        cv2.putText(output_frame, f"Phase: {controller.state}", (10, 90),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 0), 2)
        cv2.putText(output_frame, f"Time in Phase: {controller.time_in_state:.1f}s", (10, 120),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)

        # Calculate and display time remaining in phase
        time_remaining = 0
        if controller.state == controller.NS_GREEN or controller.state == controller.EW_GREEN:
            time_remaining = controller.max_green_time - controller.time_in_state
        elif controller.state == controller.NS_YELLOW or controller.state == controller.EW_YELLOW:
            time_remaining = controller.yellow_time - controller.time_in_state
        elif controller.state == controller.ALL_RED:
            time_remaining = controller.all_red_time - controller.time_in_state
        
        cv2.putText(output_frame, f"Time Left: {max(0, time_remaining):.1f}s", (10, 150),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)

        # ---- Step 6: Log performance ----
        total_vehicles = sum(densities.values())
        logger.update(total_vehicles)
        if int(time.time()) % 5 == 0:
            logger.log()

        # ---- Step 7: Show live output ----
        cv2.imshow("Smart Traffic Control System", output_frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # ---- Step 8: Wrap up ----
    logger.log()
    cap.release()
    cv2.destroyAllWindows()
    print("🏁 Processing complete. Logs saved to performance_log.csv")

if __name__ == "__main__":
    main()