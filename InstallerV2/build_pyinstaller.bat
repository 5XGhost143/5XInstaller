@echo off
pyinstaller --onefile --noconsole --icon=ico\installer.ico main.py
copy ico\installer.ico dist\installer.ico
pause
