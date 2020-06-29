@echo off
echo Starting Python Package Installation

echo Checking for Python Updates

python -m pip install --upgrade pip
echo Installing Packages

pip install numpy
pip install matplotlib
pip install Pillow
pip install opencv-python
pip install reportlab

echo Updating Program
python update.py
echo COMPLETE
pause