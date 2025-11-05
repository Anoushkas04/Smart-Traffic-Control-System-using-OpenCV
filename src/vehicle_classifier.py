
import cv2
import joblib
import numpy as np
from skimage.feature import hog

class VehicleClassifier:
    def __init__(self, model_path='src/models/svm_classifier.pkl'):
        self.model = joblib.load(model_path)

    def classify(self, image):
        # Convert image to grayscale
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        # Resize image to the same size as the training images
        resized_image = cv2.resize(gray_image, (64, 64))

        # Extract HOG features
        hog_features = hog(resized_image, orientations=9, pixels_per_cell=(8, 8),
                           cells_per_block=(2, 2), transform_sqrt=True, block_norm="L2-Hys")

        # Reshape the features to be a single sample
        hog_features = hog_features.reshape(1, -1)

        # Predict the class and probability
        prediction = self.model.predict(hog_features)[0]
        probability = np.max(self.model.predict_proba(hog_features))
        return prediction, probability
