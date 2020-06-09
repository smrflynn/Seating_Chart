@echo off
echo Starting Python Package Installation

echo Checking for Python Updates
pause

python -m pip install --upgrade pip

echo Installing Packages
pause

pip install numpy
pip install matplotlib
pip install Pillow
pip install opencv-python
pip install json
pip install reportlab

pause