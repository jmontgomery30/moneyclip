@echo off
REM Change directory to the location of main.py
cd /Volumes/X10_Pro/AI_CLIPING/workspace-blank

REM Activate the virtual environment
call venv\Scripts\activate

REM Run the main.py program in verbose mode
python -m trace --trace main.py
