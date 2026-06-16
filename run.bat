@echo off
cd /d "%~dp0"
set PYTHONPATH=%cd%
..\aMONI\.venv\Scripts\python.exe -m streamlit run app.py