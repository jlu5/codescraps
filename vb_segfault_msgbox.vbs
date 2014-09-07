Dim max,min,rn
max=2147483647 'max number allowed for CLng
min=1
Randomize
'Generate a random # for the 0x12345678 part and convert it to hex
rn=(CLng((max-min+1)*Rnd+min))
rn=LCase(Hex(rn))
'Actual message box part: Chr(13) & Chr(10) = equivalent of \n
x=msgbox("The instruction at 0x" & rn & " referenced memory at 0x00000000. The memory could not be read." & Chr(13) & Chr(10) & Chr(13) & Chr(10) & "Click on OK to terminate the program" ,16+4096, "svchost.exe - Application Error")