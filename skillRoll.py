import random

class player:
    name = "Player"
    ST = 10
    DX = 10
    IQ = 10
    HT = 10
    maxHP = ST
    tempHP = maxHP

class baseNPC:
    name = "mook"
    ST = 10
    DX = 10
    IQ = 10
    HT = 10
    maxHP = ST
    tempHP = maxHP

def roll(skill):
    y = 0
    i = 0
    result = ""
    for i in range(3):
        x = random.randrange(1,7)
        print(x)
        y += x
        continue
    print("Total = ", y)
    if y > skill:
        print("Test failed.")
        result = 1
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
    return total

    
def attack(skill, target):
    result = roll(skill)
    dmg = 0
    if result == 2:
        dmg = rollDmg(1,-2)
    elif result == 3:
        dmg = 4
        print("Total Damage = ", dmg)
    elif result == 1:
        print("Whiff! No damage dealt.")
    elif result == 0:
        print("""Eventually, we'll have a crit fail chart for this.
        For now, you just suck.""")
    target.tempHP -= dmg
    print(f"{target.name} has {target.tempHP} HP remaining.")
