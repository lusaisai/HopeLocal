@echo off

set title="HopeLocal"
set dir=%~dp0
set python="C:\Python27\pythonw.exe"

start %title% /D %dir% %python% front_server.py
start %title% /D %dir% %python% https_server.py
start %title% /D %dir% %python% app_server.py
