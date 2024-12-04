@echo off
echo Searching for Python...
for %%i in (python.exe) do set PYTHON_PATH=%%~$PATH:i

REM finding...
if "%PYTHON_PATH%"=="" (
    echo Python wurde nicht gefunden. Bitte stellen Sie sicher, dass Python installiert ist und im PATH liegt.
    exit /b 1
)

echo Installing Python packages...
pip install keyboard
echo Install successfull

echo looking for path...
set SCRIPT_DIR=%~dp0

echo start...
cd /d %SCRIPT_DIR%
%PYTHON_PATH% main.py
