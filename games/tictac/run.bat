@echo off

REM Helper launcher script for Windows systems.
where /q python
if ERRORLEVEL 1 (
    echo Error: Python not found. You can download this from https://www.python.org/downloads/ ^(make sure it's added in the PATH^).
    exit /b
) else (
    python ttt.py %*
)

pause