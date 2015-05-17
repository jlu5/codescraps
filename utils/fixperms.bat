@echo off
REM Recursively reset NTFS permissions, because Windows always has trouble doing this.

set DIR=%1
takeown /f %DIR% /r
icacls %DIR% /reset /T