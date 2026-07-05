@echo off
setlocal
cd /d %~dp0

where py >nul 2>nul
if %errorlevel%==0 (
    py -3 scripts\package_portable_zip.py
) else (
    python scripts\package_portable_zip.py
)

if exist dist\the-prof-portable.zip (
    echo Created dist\the-prof-portable.zip
) else (
    echo Failed to create portable ZIP package.
    exit /b 1
)
endlocal
