@echo off

set title="HopeLocal"
set dir="C:\projects\HopeLocal"
set pythonw="C:\Python27\pythonw.exe"

start %title% /D %dir% %pythonw% front_server.py
start %title% /D %dir% %pythonw% https_server.py
start %title% /D %dir% %pythonw% app_server.py http
start %title% /D %dir% %pythonw% app_server.py https
