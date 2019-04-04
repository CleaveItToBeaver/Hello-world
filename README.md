# Hello-world
A testbed for the very basics

def roll(skill):
	y = 0
	i = 0
	for i in range(3):
		x = random.randrange(1,7)
		print(x)
		y += x
		continue
	print("Total = ", y)
	if y > skill:
		print("Test failed.")
	else if y = 4:
		print("Automatic Success!")
	else if y = 3:
		print("Critical Success!")
	else:
		print("Success!")
