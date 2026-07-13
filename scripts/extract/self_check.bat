@echo off
rem =========================================================================
rem self_check.bat - Self-check 1-click cho nguoi trich xuat (Gate G1 so bo)
rem CACH DUNG: keo-tha 1 hay nhieu file qtcn-seed .json vao file .bat nay,
rem            hoac:  self_check.bat seed1.json [seed2.json ...]
rem Sensor phai RE de chay thuong xuyen - day la cong cu GIUP nguoi trich
rem tu kiem truoc khi nop, khong chi la cong cu bat loi (WX-QT-EXTRACT-SENSOR-01).
rem =========================================================================
chcp 65001 >nul
setlocal enabledelayedexpansion

if "%~1"=="" (
    echo Keo-tha file qtcn-seed .json vao file .bat nay de tu kiem tra.
    pause
    exit /b 3
)

set FAILED=0
for %%F in (%*) do (
    echo.
    echo ======== KIEM TRA: %%~nxF ========
    python "%~dp0validate_qtcn_seed.py" --seed "%%~F"
    if errorlevel 2 set FAILED=1
)

echo.
if "%FAILED%"=="1" (
    echo *** CO SEED BI GATE G1 CHAN - sua truoc khi nop. Chi tiet: *.validation.json ***
) else (
    echo Tat ca seed dat. Neu phat hanh lo: can them kiem cheo 2 nguon ^(--cross --release^).
)
pause
