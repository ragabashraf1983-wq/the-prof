@echo off
setlocal
cd /d %~dp0

where py >nul 2>nul
if %errorlevel%==0 (
    set PY=py -3
) else (
    set PY=python
)

%PY% -m pip install --upgrade pip
%PY% -m pip install -r requirements.txt pyinstaller

%PY% -m PyInstaller ^
    --noconfirm ^
    --clean ^
    --windowed ^
    --name TheProf ^
    --add-data "the_prof;the_prof" ^
    --add-data "TheProf_logo.png;." ^
    --add-data "docs;docs" ^
    --add-data "brain;brain" ^
    main.py

if exist dist\TheProf\TheProf.exe (
    echo Built dist\TheProf\TheProf.exe
) else (
    echo EXE build did not produce the expected file.
    exit /b 1
)
endlocal
