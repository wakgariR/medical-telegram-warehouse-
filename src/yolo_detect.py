import os
import pandas as pd
from ultralytics import YOLO

# Path to your images downloaded in Task 1
IMAGE_DIR = "data/raw/images"
OUTPUT_CSV = "data/processed/yolo_results.csv"

# Load YOLOv8 nano model
model = YOLO("yolov8n.pt")

results_list = []

# Iterate over all images
for img_file in os.listdir(IMAGE_DIR):
    if img_file.lower().endswith((".jpg", ".jpeg", ".png")):
        img_path = os.path.join(IMAGE_DIR, img_file)
        results = model(img_path)[0]  # first result per image

        # Loop over detections
        for obj in results.boxes.data.tolist():  # xyxy, conf, cls
            x1, y1, x2, y2, conf, cls = obj
            cls_name = model.names[int(cls)]
            results_list.append({
                "image_file": img_file,
                "detected_object": cls_name,
                "confidence_score": conf
            })

# Save to CSV
df = pd.DataFrame(results_list)
os.makedirs(os.path.dirname(OUTPUT_CSV), exist_ok=True)
df.to_csv(OUTPUT_CSV, index=False)
print(f"YOLO detection results saved to {OUTPUT_CSV}")
