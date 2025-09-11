from ultralytics import YOLO
import cv2
import numpy as np

# Load a model
model = YOLO("best_advanced.pt")
class_names = model.names

# Specify the input path (either an image or video)
#input_path = r"C:\Users\Vishakha\Downloads\VID20241229145937.mp4"  # replace with your file path
#input_path = r"C:\Users\Vishakha\Downloads\VID20241229144845.mp4"
input_path = r"D:\yolov8-roadpothole-detection-main\yolov8-roadpothole-detection-main\Pothol road video.mp4"
# Check if input is a video
if input_path.lower().endswith(('.mp4', '.avi', '.mov', '.mkv')):
    cap = cv2.VideoCapture(input_path)
    if not cap.isOpened():
        print("Error: Could not open video.")
        exit()

    count = 0
    while True:
        ret, img = cap.read()
        if not ret or img is None:
            print("End of video or frame not read properly.")
            break

        # Optional: remove frame skipping to debug with all frames
        count += 1
        if count % 3 != 0:
            continue

        img = cv2.resize(img, (1020, 500))
        h, w, _ = img.shape
        results = model.predict(img)

        for r in results:
            boxes = r.boxes
            masks = r.masks

        if masks is not None:
            masks = masks.data.cpu()
            for seg, box in zip(masks.data.cpu().numpy(), boxes):
                seg = cv2.resize(seg, (w, h))
                contours, _ = cv2.findContours((seg).astype(np.uint8), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

                for contour in contours:
                    d = int(box.cls)
                    c = class_names[d]
                    x, y, x1, y1 = cv2.boundingRect(contour)
                    cv2.polylines(img, [contour], True, color=(0, 0, 255), thickness=2)
                    cv2.rectangle(img, (x, y), (x1 + x, y1 + y), (255, 0, 0), 2)

        cv2.imshow('img', img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
else:
    # Process a single image
    img = cv2.imread(input_path)
    if img is None:
        print("Error: Could not read image.")
        exit()

    img = cv2.resize(img, (1020, 500))
    h, w, _ = img.shape
    results = model.predict(img)

    for r in results:
        boxes = r.boxes
        masks = r.masks

    if masks is not None:
        masks = masks.data.cpu()
        for seg, box in zip(masks.data.cpu().numpy(), boxes):
            seg = cv2.resize(seg, (w, h))
            contours, _ = cv2.findContours((seg).astype(np.uint8), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

            for contour in contours:
                d = int(box.cls)
                c = class_names[d]
                x, y, x1, y1 = cv2.boundingRect(contour)
                #cv2.polylines(img, [contour], True, color=(0, 0, 255), thickness=2)
                cv2.rectangle(img, (x, y), (x1 + x, y1 + y), (255, 0, 0), 2)

    cv2.imshow('img', img)
    cv2.waitKey(0)

cv2.destroyAllWindows()
