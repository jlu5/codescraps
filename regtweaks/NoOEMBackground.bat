@echo off

:checkPrivileges
NET FILE 1>NUL 2>NUL
if '%errorlevel%' EQU '0' goto elevated

echo This script requires administrator privileges.
pause
exit
:elevated
regedit NoOEMBackground.reg
move /-Y %windir%\system32\oobe\info %windir%\system32\oobe\info.bak