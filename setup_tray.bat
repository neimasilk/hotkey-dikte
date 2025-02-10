@echo off
reg add "HKCU\Software\Microsoft\Windows\CurrentVersion\Explorer\Advanced" /v "EnableAutoTray" /t REG_DWORD /d 0 /f
taskkill /f /im explorer.exe
start explorer.exe 