# src/features.py
import cv2

class FeatureExtractor:
    def __init__(self, method="SIFT"):
        """
        method: "SIFT" or "ORB"
        """
        self.method = method.upper()
        if self.method == "SIFT":
            if hasattr(cv2, 'SIFT_create'):
                self.extractor = cv2.SIFT_create()
            else:
                raise ValueError("Your OpenCV version does not support SIFT")
        elif self.method == "ORB":
            self.extractor = cv2.ORB_create()
        else:
            raise ValueError("Unsupported method. Use 'SIFT' or 'ORB'")

    def detect_and_compute(self, image):
        """
        image: grayscale image
        returns: keypoints and descriptors
        """
        keypoints, descriptors = self.extractor.detectAndCompute(image, None)
        return keypoints, descriptors

    def draw_keypoints(self, image, keypoints):
        """
        Draw keypoints on image for visualization
        """
        return cv2.drawKeypoints(image, keypoints, None, flags=cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
