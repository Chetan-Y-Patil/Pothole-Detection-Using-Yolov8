from flask import Flask, render_template, request, jsonify, send_file
import os
import cv2
import numpy as np
from ultralytics import YOLO
import tempfile
import uuid
from werkzeug.utils import secure_filename
import json

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['OUTPUT_FOLDER'] = 'outputs'
app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024  # 100MB max file size

# Create directories if they don't exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['OUTPUT_FOLDER'], exist_ok=True)

# Load the model (using best_advanced.pt as it seems more comprehensive)
model_path = os.path.join('Model', 'best_advanced.pt')
model = YOLO(model_path)
class_names = model.names

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'bmp', 'mp4', 'avi', 'mov', 'mkv'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def process_image(image_path, output_path):
    """Process a single image for pothole detection"""
    try:
        img = cv2.imread(image_path)
        if img is None:
            return False, "Could not read image"
        
        # Resize image for processing
        img = cv2.resize(img, (1020, 500))
        h, w, _ = img.shape
        
        # Run prediction
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
                        # Draw bounding box
                        cv2.rectangle(img, (x, y), (x1 + x, y1 + y), (255, 0, 0), 2)
                        # Add label
                        cv2.putText(img, c, (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 0, 0), 2)
        
        # Save processed image
        cv2.imwrite(output_path, img)
        return True, "Image processed successfully"
        
    except Exception as e:
        return False, str(e)

def process_video(video_path, output_path):
    """Process a video for pothole detection"""
    try:
        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            return False, "Could not open video"
        
        # Get video properties
        fps = int(cap.get(cv2.CAP_PROP_FPS))
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        
        # Create video writer
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(output_path, fourcc, fps, (1020, 500))
        
        frame_count = 0
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            
            # Process every 3rd frame for performance
            frame_count += 1
            if frame_count % 3 != 0:
                continue
            
            # Resize frame
            frame = cv2.resize(frame, (1020, 500))
            h, w, _ = frame.shape
            
            # Run prediction
            results = model.predict(frame)
            
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
                            # Draw bounding box
                            cv2.rectangle(frame, (x, y), (x1 + x, y1 + y), (255, 0, 0), 2)
                            # Add label
                            cv2.putText(frame, c, (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 0, 0), 2)
            
            out.write(frame)
        
        cap.release()
        out.release()
        return True, "Video processed successfully"
        
    except Exception as e:
        return False, str(e)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    if file and allowed_file(file.filename):
        # Generate unique filename
        filename = secure_filename(file.filename)
        unique_id = str(uuid.uuid4())
        file_ext = filename.rsplit('.', 1)[1].lower()
        
        # Save uploaded file
        upload_path = os.path.join(app.config['UPLOAD_FOLDER'], f"{unique_id}_{filename}")
        file.save(upload_path)
        
        # Determine output path
        if file_ext in ['mp4', 'avi', 'mov', 'mkv']:
            output_filename = f"processed_{unique_id}.mp4"
            output_path = os.path.join(app.config['OUTPUT_FOLDER'], output_filename)
            success, message = process_video(upload_path, output_path)
        else:
            output_filename = f"processed_{unique_id}.{file_ext}"
            output_path = os.path.join(app.config['OUTPUT_FOLDER'], output_filename)
            success, message = process_image(upload_path, output_path)
        
        if success:
            return jsonify({
                'success': True,
                'message': message,
                'output_file': output_filename,
                'file_type': 'video' if file_ext in ['mp4', 'avi', 'mov', 'mkv'] else 'image'
            })
        else:
            return jsonify({'error': message}), 500
    
    return jsonify({'error': 'Invalid file type'}), 400

@app.route('/download/<filename>')
def download_file(filename):
    try:
        return send_file(
            os.path.join(app.config['OUTPUT_FOLDER'], filename),
            as_attachment=True,
            download_name=filename
        )
    except Exception as e:
        return jsonify({'error': str(e)}), 404

@app.route('/model-info')
def model_info():
    return jsonify({
        'model_name': 'YOLOv8 Pothole Detection',
        'model_path': model_path,
        'class_names': class_names,
        'model_type': 'Instance Segmentation'
    })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
