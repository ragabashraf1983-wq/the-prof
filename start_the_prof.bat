@echo off
setlocal EnableExtensions
cd /d "%~dp0"
title The Prof Launcher

set LOG_FILE=%~dp0the_prof_startup.log

call :log ========================================
call :log The Prof launcher started
call :log Working directory: %CD%
call :log ========================================

echo.
echo Starting The Prof...
echo A startup log will be written to:
echo %LOG_FILE%
echo.

if not exist requirements.txt (
    echo ERROR: requirements.txt was not found.
    call :log ERROR: requirements.txt missing
    goto :fail
)

if not exist main.py (
    echo ERROR: main.py was not found.
    call :log ERROR: main.py missing
    goto :fail
)

set PYTHON_CMD=
set PYTHON_EXE=

if exist ".venv\Scripts\python.exe" (
    set PYTHON_EXE=.venv\Scripts\python.exe
    set PYTHON_CMD=".venv\Scripts\python.exe"
    call :log Found existing virtual environment Python: .venv\Scripts\python.exe
)

if "%PYTHON_CMD%"=="" (
    where py >nul 2>nul
    if %errorlevel%==0 (
        set PYTHON_CMD=py -3
        call :log Found launcher: py -3
    ) else (
        where python >nul 2>nul
        if %errorlevel%==0 (
            set PYTHON_CMD=python
            call :log Found launcher: python
        )
    )
)

if "%PYTHON_CMD%"=="" (
    echo ERROR: Python 3 was not found.
    echo Please install Python 3.11+ from https://www.python.org/downloads/windows/
    echo and make sure the installer adds Python to PATH.
    call :log ERROR: No Python launcher found
    goto :fail
)

if "%PYTHON_EXE%"=="" (
    echo Creating local virtual environment...
    call :log Creating local virtual environment
    call %PYTHON_CMD% -m venv .venv >> "%LOG_FILE%" 2>&1
    if not exist ".venv\Scripts\python.exe" (
        echo ERROR: Failed to create virtual environment.
        call :log ERROR: virtual environment creation failed
        goto :fail
    )
    set PYTHON_EXE=.venv\Scripts\python.exe
)

echo Installing or verifying dependencies...
call :log Upgrading pip
call "%PYTHON_EXE%" -m pip install --upgrade pip >> "%LOG_FILE%" 2>&1
if errorlevel 1 (
    echo ERROR: pip upgrade failed.
    call :log ERROR: pip upgrade failed
    goto :fail
)

call :log Installing requirements
call "%PYTHON_EXE%" -m pip install -r requirements.txt >> "%LOG_FILE%" 2>&1
if errorlevel 1 (
    echo ERROR: dependency installation failed.
    call :log ERROR: pip install -r requirements.txt failed
    goto :fail
)

echo Launching The Prof UI...
call :log Launching application
call "%PYTHON_EXE%" main.py >> "%LOG_FILE%" 2>&1
set APP_EXIT=%errorlevel%
call :log Application exited with code %APP_EXIT%

if not "%APP_EXIT%"=="0" (
    echo.
    echo The Prof closed with exit code %APP_EXIT%.
    echo Please open this log file and send me the last 50 lines:
    echo %LOG_FILE%
    goto :fail
)

goto :end

:log
echo [%date% %time%] %*>> "%LOG_FILE%"
goto :eof

:fail
echo.
echo Startup failed.
echo Check the log file:
echo %LOG_FILE%
echo.
pause
exit /b 1

:end
endlocal
exit /b 0
