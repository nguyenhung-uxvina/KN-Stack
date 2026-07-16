@echo off
REM ==== WX CAD PIPELINE — mở phần mềm điều khiển tổng thể ====
REM Bấm đúp file này. Cần Python (có Tkinter) trong PATH.
chcp 65001 >nul
python "%~dp0app\wx_pipeline_gui.py"
if errorlevel 1 (
  echo.
  echo [!] Khong mo duoc. Kiem tra: da cai Python chua? go lenh:  python --version
  pause
)
