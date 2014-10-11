#!/usr/bin/env lua
math.randomseed(os.time())
math.random(); math.random(); math.random()

print("Let's play HiLo! Pick a number between 1 to 100.")
hiloN = math.random(1, 100)
hiloT = 0
while true do
hiloG = tonumber((io.read()))
hiloT = hiloT + 1
	if (hiloG) < (hiloN) then print("Higher!")
	elseif (hiloG) > (hiloN) then print("Lower!")
	else print("You got it! The number is "..hiloN..", and it took "..hiloT.." tries to find it.")
		break
	end
end

