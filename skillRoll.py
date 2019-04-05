import random

def roll(skill):
    y = 0
    i = 0
    for i in range(3):
        x = random.randrange(1,7)
        print(x)
        y += x
        continue
    print("Total = ", y)
    if y > skill: print("Test failed.")
    elif y == 4:
        print("Automatic Success!")
    elif y == 3:
        print("Critical Success!")
    elif y == 17:
        print("Automatic Failure")
    elif y == 18:
        print("Critical Failure!")
    else:
        print("Success!")
