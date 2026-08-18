import cv2
import numpy as np
import os
import random

def create_sample_traffic_video(output_path="src/data/test_videos/sample6.mp4", width=640, height=480, fps=25, duration_sec=15):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))
    
    # Load some vehicle patches
    vehicle_dir = "src/data/training/vehicles"
    vehicle_files = [os.path.join(vehicle_dir, f) for f in os.listdir(vehicle_dir) if f.endswith(('.png', '.jpg'))] if os.path.exists(vehicle_dir) else []
    
    # Preload patches
    patches = []
    for f in vehicle_files[:10]:
        img = cv2.imread(f)
        if img is not None:
            patches.append(cv2.resize(img, (60, 60)))
            
    if not patches:
        # Fallback dummy patch
        dummy = np.zeros((60, 60, 3), dtype=np.uint8)
        dummy[:, :] = (0, 0, 200)
        patches.append(dummy)

    # Active cars in NS (vertical) and EW (horizontal)
    cars = []
    total_frames = fps * duration_sec

    for frame_idx in range(total_frames):
        # Background: 4-way intersection road
        frame = np.full((height, width, 3), 40, dtype=np.uint8)
        
        # Draw roads (gray)
        cv2.rectangle(frame, (width // 2 - 90, 0), (width // 2 + 90, height), (70, 70, 70), -1)
        cv2.rectangle(frame, (0, height // 2 - 80), (width, height // 2 + 80), (70, 70, 70), -1)
        
        # Lane markings
        cv2.line(frame, (width // 2, 0), (width // 2, height // 2 - 80), (255, 255, 255), 2)
        cv2.line(frame, (width // 2, height // 2 + 80), (width // 2, height), (255, 255, 255), 2)
        cv2.line(frame, (0, height // 2), (width // 2 - 90, height // 2), (255, 255, 255), 2)
        cv2.line(frame, (width // 2 + 90, height // 2), (width, height // 2), (255, 255, 255), 2)

        # Spawn cars periodically
        if frame_idx % 25 == 0:
            # North to South car
            cars.append({'dir': 'NS', 'x': width // 2 - 50, 'y': -60, 'vy': random.randint(3, 6), 'vx': 0, 'patch': random.choice(patches)})
        if frame_idx % 35 == 0:
            # South to North car
            cars.append({'dir': 'SN', 'x': width // 2 + 10, 'y': height + 10, 'vy': -random.randint(3, 6), 'vx': 0, 'patch': random.choice(patches)})
        if frame_idx % 30 == 0:
            # West to East car
            cars.append({'dir': 'WE', 'x': -60, 'y': height // 2 + 10, 'vx': random.randint(3, 6), 'vy': 0, 'patch': random.choice(patches)})
        if frame_idx % 40 == 0:
            # East to West car
            cars.append({'dir': 'EW', 'x': width + 10, 'y': height // 2 - 50, 'vx': -random.randint(3, 6), 'vy': 0, 'patch': random.choice(patches)})

        # Update and render cars
        active_cars = []
        for c in cars:
            c['x'] += c['vx']
            c['y'] += c['vy']
            
            x, y = int(c['x']), int(c['y'])
            ph, pw = c['patch'].shape[:2]
            
            if -80 < x < width + 80 and -80 < y < height + 80:
                active_cars.append(c)
                # Paste patch with boundary check
                x1, x2 = max(0, x), min(width, x + pw)
                y1, y2 = max(0, y), min(height, y + ph)
                
                px1 = x1 - x
                px2 = px1 + (x2 - x1)
                py1 = y1 - y
                py2 = py1 + (y2 - y1)
                
                if x2 > x1 and y2 > y1:
                    frame[y1:y2, x1:x2] = c['patch'][py1:py2, px1:px2]

        cars = active_cars
        out.write(frame)

    out.release()
    print(f"✅ Generated sample video at {output_path}")

if __name__ == "__main__":
    create_sample_traffic_video()
