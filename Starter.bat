@echo off
setlocal

:: Change directory to the script location
cd /d "%~dp0"

:: Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Python is not installed. Downloading and installing Python...
    :: Download Python installer
    powershell -Command "Invoke-WebRequest -Uri https://www.python.org/ftp/python/3.10.4/python-3.10.4-amd64.exe -OutFile python-installer.exe"

    :: Install Python silently
    start /wait python-installer.exe /quiet InstallAllUsers=1 PrependPath=1
    del python-installer.exe
) else (
    echo Python is already installed.
)

:: Install Pygame
python -m pip install pygame

:: Install ctypes
python -m pip install ctypes

:: Create a temporary VBScript to run the Python script as admin
echo Set UAC = CreateObject^("Shell.Application"^) > run_as_admin.vbs
echo UAC.ShellExecute "cmd.exe", "/c cd /d ^"""%~dp0contents^""" ^&^& python Main.py", "", "runas", 1 >> run_as_admin.vbs

:: Run the Python script as admin
cscript run_as_admin.vbs
del run_as_admin.vbs

endlocal
