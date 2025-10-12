# # src/calibrate.py
# import cv2
# import numpy as np
# import glob

# class CameraCalibrator:
#     def __init__(self, chessboard_size=(9,6), square_size=1.0):
#         self.chessboard_size = chessboard_size
#         self.square_size = square_size
#         self.objpoints = []
#         self.imgpoints = []
#         self.mtx = None
#         self.dist = None

#     def calibrate(self, images_path="data/chessboard/*.jpg"):
#         objp = np.zeros((self.chessboard_size[0]*self.chessboard_size[1],3), np.float32)
#         objp[:,:2] = np.mgrid[0:self.chessboard_size[0],0:self.chessboard_size[1]].T.reshape(-1,2)

#         images = glob.glob(images_path)
#         for fname in images:
#             img = cv2.imread(fname)
#             gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
#             ret, corners = cv2.findChessboardCorners(gray, self.chessboard_size, None)
#             if ret:
#                 self.objpoints.append(objp)
#                 self.imgpoints.append(corners)

#         ret, self.mtx, self.dist, _, _ = cv2.calibrateCamera(
#             self.objpoints, self.imgpoints, gray.shape[::-1], None, None)
#         return ret, self.mtx, self.dist

#     def undistort(self, frame):
#         if self.mtx is None or self.dist is None:
#             return frame
#         return cv2.undistort(frame, self.mtx, self.dist, None, self.mtx)

# src/calibrate.py
import cv2
import numpy as np
import glob

class CameraCalibrator:
    def __init__(self, chessboard_size=(9,6), square_size=1.0):
        self.chessboard_size = chessboard_size
        self.square_size = square_size
        self.objpoints = []
        self.imgpoints = []
        self.mtx = None
        self.dist = None

    def calibrate(self, images_path="data/chessboard/*.jpg"):
        objp = np.zeros((self.chessboard_size[0]*self.chessboard_size[1],3), np.float32)
        objp[:,:2] = np.mgrid[0:self.chessboard_size[0],0:self.chessboard_size[1]].T.reshape(-1,2)

        images = glob.glob(images_path)
        for fname in images:
            img = cv2.imread(fname)
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            ret, corners = cv2.findChessboardCorners(gray, self.chessboard_size, None)
            if ret:
                self.objpoints.append(objp)
                self.imgpoints.append(corners)

        ret, self.mtx, self.dist, _, _ = cv2.calibrateCamera(
            self.objpoints, self.imgpoints, gray.shape[::-1], None, None)
        return ret, self.mtx, self.dist

    def undistort(self, frame):
        if self.mtx is None or self.dist is None:
            return frame
        return cv2.undistort(frame, self.mtx, self.dist, None, self.mtx)