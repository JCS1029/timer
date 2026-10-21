@echo off
setlocal EnableExtensions
cd /d "%~dp0"
title Timer setup

echo.
echo Timer setup
echo.

if not exist "%~dp0requirements.txt" (
    echo requirements.txt was not found next to setup.bat.
    goto :fail
)

set "PY_EXE="
set "PY_OK="
set "PYTHON_EXE="
set "PY_MANAGER="
for /d %%D in ("%LocalAppData%\Microsoft\WindowsApps\PythonSoftwareFoundation.PythonManager*") do set "PY_MANAGER=1"

call :resolve_py
if defined PY_OK (
    echo Python is already installed.
    goto :install_packages
)

call :resolve_direct_python
if defined PYTHON_EXE (
    echo Python is already installed.
    goto :install_packages
)

echo Python 3.10 or newer is required and was not found.
echo Downloading the official Python 3.13.16 installer...
echo.
call :download_python
if errorlevel 1 goto :fail
call :install_python
if errorlevel 1 goto :fail

set "PY_EXE="
set "PY_OK="
set "PYTHON_EXE="
call :resolve_py
if not defined PY_OK call :resolve_direct_python
if not defined PY_OK if not defined PYTHON_EXE (
    echo Python was installed, but this window cannot see it yet.
    echo Close this window, then run setup.bat again.
    goto :fail
)

:install_packages
if not defined PYTHON_EXE call :resolve_python_exe
if not defined PYTHON_EXE (
    echo Could not find the Python program that timer.bat will use.
    goto :fail
)

echo.
echo Using this Python:
"%PYTHON_EXE%" -c "import sys; print(sys.executable); print(sys.version)"
if errorlevel 1 goto :fail

echo.
echo Updating pip...
"%PYTHON_EXE%" -m pip install --upgrade pip
if errorlevel 1 echo Pip could not be updated. Continuing with the installed pip.

echo.
echo Installing packages from requirements.txt...
"%PYTHON_EXE%" -m pip install -r "%~dp0requirements.txt"
if errorlevel 1 (
    echo.
    echo Retrying the install into the current user account...
    "%PYTHON_EXE%" -m pip install --user -r "%~dp0requirements.txt"
    if errorlevel 1 goto :fail
)

echo.
echo Checking tkinter, ttkbootstrap, and playsound3...
"%PYTHON_EXE%" -c "import tkinter, ttkbootstrap, playsound3"
if errorlevel 1 (
    echo The packages installed, but Python could not import them.
    goto :fail
)

echo.
echo Setup finished. Run timer.bat to start the timer.
if not exist "%~dp0quack.mp3" (
    echo.
    echo quack.mp3 is not in this folder. The window will still open.
    echo The sound at the end of a countdown needs that file next to timer.bat.
)
goto :success

:fail
echo.
echo Setup did not finish. Fix the problem above, then run setup.bat again.
echo.
pause
exit /b 1

:success
echo.
pause
exit /b 0

:resolve_py
set "PY_EXE="
set "PY_OK="
for /f "delims=" %%P in ('where py 2^>nul') do (
    if not defined PY_OK call :consider_py "%%P"
)
if defined PY_OK exit /b 0
call :consider_py "%LocalAppData%\Programs\Python\Launcher\py.exe"
if defined PY_OK exit /b 0
call :consider_py "%SystemRoot%\py.exe"
if defined PY_OK exit /b 0
if defined PY_MANAGER call :consider_py "%LocalAppData%\Microsoft\WindowsApps\py.exe"
exit /b 0

:consider_py
if not exist "%~1" exit /b 0
echo %~1 | find /I "\WindowsApps\" >nul
if not errorlevel 1 if not defined PY_MANAGER exit /b 0
"%~1" -3 -c "import sys; raise SystemExit(0 if sys.version_info >= (3, 10) else 1)" >nul 2>&1
if errorlevel 1 exit /b 0
set "PY_EXE=%~1"
set "PY_OK=1"
exit /b 0

:resolve_python_exe
set "PYTHON_EXE="
set "PY_PATH_FILE=%TEMP%\timer-python-path.txt"
if exist "%PY_PATH_FILE%" del /f /q "%PY_PATH_FILE%" >nul 2>&1
if not defined PY_EXE exit /b 0
"%PY_EXE%" -3 -c "import sys; print(sys.executable)" > "%PY_PATH_FILE%" 2>nul
if exist "%PY_PATH_FILE%" set /p PYTHON_EXE=<"%PY_PATH_FILE%"
if exist "%PY_PATH_FILE%" del /f /q "%PY_PATH_FILE%" >nul 2>&1
if defined PYTHON_EXE if exist "%PYTHON_EXE%" exit /b 0
set "PYTHON_EXE="
exit /b 0

:resolve_direct_python
set "PYTHON_EXE="
if exist "%LocalAppData%\Python\bin\python.exe" (
    "%LocalAppData%\Python\bin\python.exe" -c "import sys; raise SystemExit(0 if sys.version_info >= (3, 10) else 1)" >nul 2>&1
    if not errorlevel 1 set "PYTHON_EXE=%LocalAppData%\Python\bin\python.exe"
)
if defined PYTHON_EXE exit /b 0
for /d %%D in ("%LocalAppData%\Python\pythoncore-*") do (
    if not defined PYTHON_EXE if exist "%%D\python.exe" (
        "%%D\python.exe" -c "import sys; raise SystemExit(0 if sys.version_info >= (3, 10) else 1)" >nul 2>&1
        if not errorlevel 1 set "PYTHON_EXE=%%D\python.exe"
    )
)
if defined PYTHON_EXE exit /b 0
for /d %%D in ("%LocalAppData%\Programs\Python\Python3*") do (
    if not defined PYTHON_EXE if exist "%%D\python.exe" (
        "%%D\python.exe" -c "import sys; raise SystemExit(0 if sys.version_info >= (3, 10) else 1)" >nul 2>&1
        if not errorlevel 1 set "PYTHON_EXE=%%D\python.exe"
    )
)
exit /b 0

:download_python
set "PY_VER=3.13.16"
set "PY_TAG=amd64"
if /I "%PROCESSOR_ARCHITECTURE%"=="ARM64" set "PY_TAG=arm64"
if /I "%PROCESSOR_ARCHITEW6432%"=="ARM64" set "PY_TAG=arm64"
if /I "%PROCESSOR_ARCHITECTURE%"=="x86" if not defined PROCESSOR_ARCHITEW6432 set "PY_TAG=win32"
if /I "%PY_TAG%"=="win32" (
    set "PY_FILE=python-%PY_VER%.exe"
) else (
    set "PY_FILE=python-%PY_VER%-%PY_TAG%.exe"
)
set "PY_URL=https://www.python.org/ftp/python/%PY_VER%/%PY_FILE%"
set "PY_SETUP=%TEMP%\%PY_FILE%"
echo %PY_URL%
echo.
if exist "%PY_SETUP%" del /f /q "%PY_SETUP%"

where curl.exe >nul 2>&1
if errorlevel 1 (
    powershell -NoProfile -ExecutionPolicy Bypass -Command "try { [Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12; Invoke-WebRequest -Uri '%PY_URL%' -OutFile '%PY_SETUP%' -UseBasicParsing; exit 0 } catch { Write-Host $_.Exception.Message; exit 1 }"
) else (
    curl.exe -L --fail --retry 3 --retry-delay 2 -o "%PY_SETUP%" "%PY_URL%"
)
if errorlevel 1 (
    echo The Python download failed. Check the internet connection and run setup.bat again.
    exit /b 1
)
if not exist "%PY_SETUP%" (
    echo The Python installer file is missing after the download.
    exit /b 1
)
for %%A in ("%PY_SETUP%") do set "PY_SETUP_SIZE=%%~zA"
if %PY_SETUP_SIZE% LSS 1000000 (
    echo The downloaded installer is incomplete.
    exit /b 1
)
exit /b 0

:install_python
echo.
echo Installing Python. This can take a minute...
"%PY_SETUP%" /quiet InstallAllUsers=0 PrependPath=1 Include_launcher=1 Include_pip=1 Include_tcltk=1 Include_test=0 AssociateFiles=0 Shortcuts=0 /log "%TEMP%\timer-python-install.log"
set "INSTALL_EXIT=%ERRORLEVEL%"
if "%INSTALL_EXIT%"=="0" goto :install_python_ok
if "%INSTALL_EXIT%"=="3010" goto :install_python_ok
echo The Python installer exited with code %INSTALL_EXIT%.
echo Details are in %TEMP%\timer-python-install.log
exit /b 1

:install_python_ok
del /f /q "%PY_SETUP%" >nul 2>&1
exit /b 0
