@echo off
start "HopeLocal" /D "C:\projects\HopeLocal" "C:\Python27\pythonw.exe" app_server.py
start "HopeLocal" /D "C:\projects\HopeLocal" "C:\Python27\pythonw.exe" front_server.py
start "HopeLocal" /D "C:\projects\HopeLocal" "C:\Python27\pythonw.exe" https_server.py
