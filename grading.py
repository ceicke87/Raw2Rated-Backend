from fastapi import UploadFile
from ultralytics import YOLO
from PIL import Image
import numpy as np
import io

model = YOLO("raw2rated_centering_model.pt")

def calculate_centering_score(detections, image_width):
    if not detections:
        return 0.0
    box = detections[0].xywh[0]
    center_x = box[0]
    offset = abs(center_x - image_width / 2)
    offset_ratio = offset / (image_width / 2)
    return round(10 - (offset_ratio * 10), 2)

async def grade_card(file: UploadFile):
    image_bytes = await file.read()
    image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
    image_np = np.array(image)
    results = model(image_np)
    detections = results[0].boxes
    image_width = image.size[0]
    centering_score = calculate_centering_score(detections, image_width)
    return {
        "centering": centering_score,
        "final_grade": round(centering_score, 2),
        "cert_id": "GRD-000125"
    }