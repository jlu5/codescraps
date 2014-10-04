Dim max,min,rn,a
a=array("svchost.exe","winlogon.exe","lsass.exe","explorer.exe","iexplore.exe","taskhost.exe","smss.exe","System Idle Process","spoolsv.exe","wininit.exe","rundll32.exe","iexplorer.exe","rundll16.com","windowsdownloadFree.exe","Keygen.exe","Setup.exe","GoogleChromeFreeDownloader.exe","FirefoxBrowserFreeDownloader.exe", "VLCMediaPlayFreeDownloader.exe","wmplayer.exe","dllhost.exe","WINWORD.exe","AOLToolbarInstaller.exe","EXCEL.exe","agent.exe","_ISDEL.exe","anttiviruspro.exe","0.exe","qq.exe","chrome.exe","firefox.exe","winSecure.exe","wmiprvse.exe","csrss.exe")
Randomize
'Generate a random # for the 0x12345678 part and convert it to hex
rn=LCase(Hex(65535*Rnd) & Hex(65535*Rnd))
'Actual message box part: Chr(13) & Chr(10) = equivalent of \n
x=msgbox("The instruction at 0x" & rn & " referenced memory at 0x00000000. The memory could not be read." & Chr(13) & Chr(10) & Chr(13) & Chr(10) & "Click on OK to terminate the program" ,16+4096, a(Int(34*Rnd)) & " - Application Error")