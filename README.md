# Pothole Detection AI Web Application

A modern, user-friendly web application for detecting potholes in images and videos using YOLOv8 instance segmentation models.

## Features

- 🖼️ **Image Processing**: Upload and process images for pothole detection
- 🎥 **Video Processing**: Upload and process videos for pothole detection
- 🎯 **AI-Powered Detection**: Uses advanced YOLOv8 models for accurate detection
- 💾 **Download Results**: Download processed files with detection overlays
- 🎨 **Modern UI**: Beautiful, responsive design with drag-and-drop functionality
- 📱 **Mobile Friendly**: Works seamlessly on all devices

## Model Information

The application uses the `best_advanced.pt` YOLOv8 model, which provides:
- Instance segmentation capabilities
- High accuracy pothole detection
- Real-time processing capabilities

## Prerequisites

- Python 3.8 or higher
- CUDA-compatible GPU (recommended for faster processing)
- At least 4GB RAM

## Installation

1. **Clone or download the project files**

2. **Install Python dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Ensure your model files are in the correct location**:
   ```
   Model/
   ├── best_advanced.pt    # Main model file
   └── best.pt             # Alternative model file
   ```

## Usage

1. **Start the application**:
   ```bash
   python app.py
   ```

2. **Open your web browser** and navigate to:
   ```
   http://localhost:5000
   ```

3. **Upload your file**:
   - Drag and drop an image or video file onto the upload area
   - Or click "Browse Files" to select a file manually
   - Supported formats: JPG, PNG, MP4, AVI, MOV, MKV

4. **Process the file**:
   - Click "Process File" to start AI detection
   - Wait for processing to complete (processing time depends on file size)

5. **Download results**:
   - Preview the processed file with detection overlays
   - Click "Download Processed File" to save the result
   - Use "Process Another File" to start over

## File Size Limits

- Maximum file size: 100MB
- For best performance, keep files under 50MB
- Video processing may take longer for larger files

## Supported File Formats

### Images
- JPG/JPEG
- PNG
- GIF
- BMP

### Videos
- MP4
- AVI
- MOV
- MKV

## Technical Details

### Backend
- **Framework**: Flask (Python)
- **AI Model**: YOLOv8 with custom training
- **Image Processing**: OpenCV
- **File Handling**: Secure file uploads with unique naming

### Frontend
- **HTML5**: Semantic markup with accessibility features
- **CSS3**: Modern styling with gradients and animations
- **JavaScript**: ES6+ with async/await for smooth UX
- **Responsive Design**: Mobile-first approach

### Processing Pipeline
1. File validation and security checks
2. Model loading and inference
3. Detection overlay generation
4. Output file creation
5. Download link generation

## Performance Tips

1. **Use GPU acceleration** if available for faster processing
2. **Optimize video files** before upload (compress if possible)
3. **Close other applications** to free up system resources
4. **Use SSD storage** for faster file I/O operations

## Troubleshooting

### Common Issues

1. **Model not loading**:
   - Ensure `best_advanced.pt` exists in the `Model/` folder
   - Check file permissions

2. **Processing errors**:
   - Verify file format is supported
   - Check file size limits
   - Ensure sufficient disk space

3. **Slow processing**:
   - Check if GPU is being utilized
   - Close unnecessary applications
   - Consider reducing video resolution

### Error Messages

- **"Could not read image/video"**: File format not supported or corrupted
- **"Processing failed"**: Check console logs for detailed error information
- **"File too large"**: Reduce file size or compress before upload

## Development

### Project Structure
```
Pothole Project/
├── app.py                 # Flask application
├── requirements.txt       # Python dependencies
├── README.md             # This file
├── Model/                # AI model files
│   ├── best_advanced.pt
│   └── best.pt
├── static/               # Frontend assets
│   ├── style.css
│   └── script.js
├── templates/            # HTML templates
│   └── index.html
├── uploads/              # Temporary upload storage
└── outputs/              # Processed file storage
```

### Customization

- **Model Selection**: Change `model_path` in `app.py` to use different models
- **Styling**: Modify `static/style.css` for custom appearance
- **Functionality**: Extend `static/script.js` for additional features

## Security Features

- File type validation
- Secure filename handling
- File size limits
- Temporary file cleanup
- Input sanitization

## License

This project is for educational and research purposes. Please ensure you have proper permissions for any models or datasets used.

## Support

For issues or questions:
1. Check the troubleshooting section above
2. Review console logs for error details
3. Ensure all dependencies are properly installed
4. Verify model files are in the correct location

## Future Enhancements

- Batch processing capabilities
- Real-time video streaming
- Multiple model support
- Advanced analytics dashboard
- API endpoints for integration
- Cloud deployment options
