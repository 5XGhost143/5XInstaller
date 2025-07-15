@echo off
pyinstaller --onefile --noconsole --icon=ico\installer.ico main.py
xcopy ico dist\ico /E /I /Y
pause
