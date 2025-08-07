@echo off
echo ============================================================
echo 🎯 SIMPLE EYE BLINK DETECTION - EASY LAUNCHER
echo ============================================================
echo.
echo Activating virtual environment...
call .\venv\Scripts\activate.bat

echo.
echo Starting Simple Blink Detection (No Enter key simulation)...
echo.
python simple_blink_detector.py

echo.
echo Deactivating virtual environment...
call deactivate

echo.
echo Press any key to exit...
pause > nul
