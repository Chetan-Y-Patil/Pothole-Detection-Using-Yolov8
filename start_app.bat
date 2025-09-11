@echo off
echo Starting Pothole Detection AI Web Application...
echo.
echo Installing dependencies...
pip install -r requirements.txt
echo.
echo Starting the application...
echo.
echo The web app will be available at: http://localhost:5000
echo Press Ctrl+C to stop the application
echo.
python app.py
pause
