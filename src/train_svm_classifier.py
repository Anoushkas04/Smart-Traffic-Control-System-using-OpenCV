
import os
import cv2
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.metrics import classification_report
from skimage.feature import hog
import joblib

def load_images_from_folder(folder, label):
    images = []
    labels = []
    for filename in os.listdir(folder):
        img_path = os.path.join(folder, filename)
        img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
        if img is not None:
            images.append(img)
            labels.append(label)
    return images, labels

def extract_hog_features(images):
    hog_features = []
    for img in images:
        # Resize image to a fixed size
        img = cv2.resize(img, (64, 64))
        # Extract HOG features
        features = hog(img, orientations=9, pixels_per_cell=(8, 8),
                       cells_per_block=(2, 2), transform_sqrt=True, block_norm="L2-Hys")
        hog_features.append(features)
    return np.array(hog_features)

def main():
    # Define paths to the dataset
    vehicle_path = 'src/data/training/vehicles'
    non_vehicle_path = 'src/data/training/non_vehicles'

    # Load images and labels
    vehicle_images, vehicle_labels = load_images_from_folder(vehicle_path, 1)
    non_vehicle_images, non_vehicle_labels = load_images_from_folder(non_vehicle_path, 0)

    # Combine the datasets
    images = vehicle_images + non_vehicle_images
    labels = vehicle_labels + non_vehicle_labels

    # Extract HOG features
    features = extract_hog_features(images)

    # Split the data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(features, labels, test_size=0.2, random_state=42)

    # Train the SVM classifier
    print("Training SVM classifier...")
    clf = SVC(kernel='linear', probability=True, random_state=42)
    clf.fit(X_train, y_train)

    # Evaluate the classifier
    print("Evaluating classifier...")
    y_pred = clf.predict(X_test)
    print(classification_report(y_test, y_pred))

    # Save the trained model
    print("Saving model...")
    if not os.path.exists('src/models'):
        os.makedirs('src/models')
    joblib.dump(clf, 'src/models/svm_classifier.pkl')
    print("Model saved to src/models/svm_classifier.pkl")

if __name__ == '__main__':
    main()
