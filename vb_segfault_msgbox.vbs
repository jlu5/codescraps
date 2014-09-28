Dim max,min,rn,a,b
a=array("svchost.exe","winlogon.exe","lsass.exe","explorer.exe","iexplore.exe","taskhost.exe","smss.exe")
Randomize
'Generate a random # for the 0x12345678 part and convert it to hex
b = a(Int(7*Rnd))
rn=LCase(Hex(65535*Rnd) & Hex(65535*Rnd))
'Actual message box part: Chr(13) & Chr(10) = equivalent of \n
x=msgbox("The instruction at 0x" & rn & " referenced memory at 0x00000000. The memory could not be read." & Chr(13) & Chr(10) & Chr(13) & Chr(10) & "Click on OK to terminate the program" ,16+4096, b & " - Application Error")