#!/usr/bin/env python3
"""
Startup script for Pothole Detection AI Web Application
"""

import subprocess
import sys
import os

def install_requirements():
    """Install required packages"""
    print("Installing required packages...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Dependencies installed successfully!")
    except subprocess.CalledProcessError:
        print("❌ Failed to install dependencies. Please install manually:")
        print("   pip install -r requirements.txt")
        return False
    return True

def check_model_files():
    """Check if model files exist"""
    model_dir = "Model"
    required_model = "best_advanced.pt"
    
    if not os.path.exists(model_dir):
        print(f"❌ Model directory '{model_dir}' not found!")
        return False
    
    model_path = os.path.join(model_dir, required_model)
    if not os.path.exists(model_path):
        print(f"❌ Required model file '{required_model}' not found in {model_dir}/")
        print("   Please ensure your model files are in the correct location.")
        return False
    
    print(f"✅ Model file found: {model_path}")
    return True

def start_app():
    """Start the Flask application"""
    print("\n🚀 Starting Pothole Detection AI Web Application...")
    print("   The web app will be available at: http://localhost:5000")
    print("   Press Ctrl+C to stop the application\n")
    
    try:
        subprocess.run([sys.executable, "app.py"])
    except KeyboardInterrupt:
        print("\n\n👋 Application stopped by user.")
    except Exception as e:
        print(f"\n❌ Error starting application: {e}")

def main():
    """Main function"""
    print("=" * 60)
    print("    Pothole Detection AI Web Application")
    print("=" * 60)
    
    # Check Python version
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required!")
        sys.exit(1)
    
    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor} detected")
    
    # Check model files
    if not check_model_files():
        sys.exit(1)
    
    # Install requirements
    if not install_requirements():
        sys.exit(1)
    
    # Start application
    start_app()

if __name__ == "__main__":
    main()
