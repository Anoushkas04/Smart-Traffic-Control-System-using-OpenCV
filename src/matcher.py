# src/matcher.py
import cv2
import numpy as np

class FeatureMatcher:
    def __init__(self, method="BF", cross_check=True):
        """
        method: "BF" for Brute Force, "FLANN" for FLANN-based matcher
        cross_check: only for BFMatcher
        """
        self.method = method
        self.cross_check = cross_check

        if self.method == "BF":
            self.matcher = cv2.BFMatcher(cv2.NORM_L2, crossCheck=self.cross_check)
        elif self.method == "FLANN":
            index_params = dict(algorithm=1, trees=5)  # KDTree for SIFT/SURF
            search_params = dict(checks=50)
            self.matcher = cv2.FlannBasedMatcher(index_params, search_params)
        else:
            raise ValueError("Unknown matcher method")

    def match(self, desc1, desc2, ratio_test=True):
        """
        Match descriptors between two sets of features.
        desc1: descriptors of detected ROI
        desc2: descriptors of template image
        Returns list of good matches
        """
        if desc1 is None or desc2 is None:
            return []

        if self.method == "BF":
            matches = self.matcher.match(desc1, desc2)
            matches = sorted(matches, key=lambda x: x.distance)
            return matches

        elif self.method == "FLANN":
            matches = self.matcher.knnMatch(desc1, desc2, k=2)
            good_matches = []
            if ratio_test:
                # Apply Lowe's ratio test
                for m, n in matches:
                    if m.distance < 0.75 * n.distance:
                        good_matches.append(m)
            else:
                good_matches = [m for m, n in matches]
            return good_matches