@echo off
title Aditi's Python Mentor - Stage 1
echo =======================================================
echo   Starting Aditi's Python & Tech Mentor (Stage 1)
echo =======================================================
echo.

set PYTHONUTF8=1
set PYTHONIOENCODING=utf-8

where py >nul 2>nul
if %errorlevel% equ 0 (
    py app.py
) else (
    python app.py
)

pause
