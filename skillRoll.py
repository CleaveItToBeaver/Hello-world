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
        result = 2
    elif y == 3:
        print("Critical Success!")
        result = 3
    elif y == 17:
        print("Automatic Failure")
        result = 1
    elif y == 18:
        print("Critical Failure!")
        result = 0
    else:
        print("Success!")
        result = 2
    return result

def rollDmg(dice, modifier):
    y = 0
    i = 0
    for i in range(dice):
        x = random.randrange(1,7)
        print(x)
        y += x
        continue
    print("Modifier: ", modifier)
    if (y+modifier) < 1:
        total = 1
    else:
        total = y + modifier
    print("Total Damage = ", total)

    
def attack(skill):
    result = roll(skill)
    if result == 2:
        rollDmg(1,-2)
    elif result == 3:
        print("Total Damage = ", 4)
    elif result == 1:
        print("Whiff! No damage dealt.")
    elif result == 0:
        print("Eventually, we'll have a crit fail chart for this.", \
                "For now, you just suck.")
        
