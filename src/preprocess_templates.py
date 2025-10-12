import cv2
import os

RAW_DIR = os.path.expanduser("~/Projects/Labs/cvLab/traffic-control/data/raw_templates/images")
OUT_DIR = os.path.expanduser("~/Projects/Labs/cvLab/traffic-control/data/templates")

os.makedirs(OUT_DIR, exist_ok=True)

def preprocess_image(img_path, save_path, size=(200, 200)):
    img = cv2.imread(img_path)
    if img is None:
        print(f"⚠️ Skipping {img_path}, could not read.")
        return

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    resized = cv2.resize(gray, size, interpolation=cv2.INTER_AREA)
    cv2.imwrite(save_path, resized)
    print(f"✅ Saved {save_path}")

def main():
    for filename in os.listdir(RAW_DIR):
        if filename.lower().endswith((".jpg", ".jpeg", ".png")):
            in_path = os.path.join(RAW_DIR, filename)
            out_name = filename.replace("_raw", "")
            out_path = os.path.join(OUT_DIR, out_name)
            preprocess_image(in_path, out_path)

if __name__ == "__main__":
    main()