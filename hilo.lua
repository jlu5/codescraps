math.randomseed(os.time())
math.random(); math.random(); math.random()

print("Welcome to the HiLo game! Guess a number between 1 to 100.")
hiloN = math.random(1, 100)
hiloT = 0
while true do
hiloG = tonumber((io.read()))
hiloT = hiloT + 1
	if (hiloG) < (hiloN) then print("Higher!")
	elseif (hiloG) > (hiloN) then print("Lower!")
	else print("You got it! The number is "..hiloN..", and it took "..hiloT.." tries to guess it.")
		break
	end
end

