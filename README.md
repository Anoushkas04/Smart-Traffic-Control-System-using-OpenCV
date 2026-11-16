# Smart Traffic Control System using OpenCV

Adaptive signal control for a four-way intersection using classical computer vision. The system counts vehicles on the north-south and east-west approaches from a video feed, then gives green time to whichever direction is more congested, within safe minimum and maximum limits.

**Stack:** Python · OpenCV · scikit-learn (SVM) · scikit-image (HOG) · NumPy

## Pipeline

1. **Regions of interest:** a polygon mask for each approach, so each direction is counted separately.
2. **Motion detection:** KNN background subtraction, morphological opening and dilation, then contour extraction. Contours under a minimum area are discarded.
3. **Verification:** each candidate patch is resized to 64×64 and passed through HOG feature extraction into a linear SVM trained on vehicle and non-vehicle images (`train_svm_classifier.py`). Only patches classified as vehicles above a probability threshold count.
4. **Periodic full scan:** every 15 frames, a sliding window runs over the ROI with the same classifier. This catches vehicles that have stopped and blended into the background model.
5. **Non-maximum suppression:** merges overlapping boxes before counting.
6. **Signal control:** a state machine with phases `NS_GREEN → NS_YELLOW → ALL_RED → EW_GREEN → EW_YELLOW → ALL_RED`. A green phase ends early once the minimum green time has passed and the opposing approach has at least 5 more vehicles. Otherwise it ends at the maximum green time. Yellow and all-red clearance intervals are always respected.
7. **Output:** a live overlay with ROIs, detections, per-direction counts, current phase and time remaining, plus vehicle counts logged to `performance_log.csv`.

## Running

```bash
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
./run.sh                          # uses src/data/test_videos/sample6.mp4
./run.sh --video path/to/clip.mp4 # or a webcam index, e.g. --video 0
```

`src/generate_sample_video.py` builds a synthetic test clip, and `src/train_svm_classifier.py` retrains the classifier from `src/data/training/{vehicles,non_vehicles}`. The ROIs in `main.py` are placeholders sized to the frame and need adjusting for real footage.

## Notes

I tried a YOLO-based counter to replace background subtraction. It was rolled back after OpenCV compatibility issues, and the details are in [`improvement-plan.md`](improvement-plan.md). Proper object tracking (Kalman/SORT) is also still open; `tracker.py` is currently a stub.
