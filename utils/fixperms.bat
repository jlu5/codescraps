@echo off
REM Recursively reset NTFS permissions, because Windows always has trouble doing this.
takeown /f "." /r
icacls "." /reset /T