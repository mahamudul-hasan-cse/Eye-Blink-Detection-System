@echo off
echo ============================================================
echo 🎯 EYE BLINK DETECTION SYSTEM - EASY LAUNCHER
echo ============================================================
echo.
echo Activating virtual environment...
call .\venv\Scripts\activate.bat

echo.
echo Starting Eye Blink Detection System...
echo.
python working_blink_detector.py

echo.
echo Deactivating virtual environment...
call deactivate

echo.
echo Press any key to exit...
pause > nul
