import random
from colorama import Fore, Style

class armor:
    DR = 0
    description = "Naked as the day you were born. You savage."
    weight = 1
    value = 5

cloth = armor()
cloth.name = "Rags"
cloth.desc = "Commoner's clothes. Woolen tunic, tattered robes, what-have-you."
cloth.weight = .5
cloth.value = 2
cloth.DR = 1

noArmor = armor()
noArmor.desc = "Naked as the day you were born. You savage."
noArmor.weight = 0
noArmor.value = 0
noArmor.DR = 0

class player:
    name = "Player"
    equippedArmor = "None"
    armorDesc = ""
    armorWgt = 0
    armorDR = 0
    ST = 10
    DX = 10
    IQ = 10
    HT = 10
    maxHP = ST
    tempHP = maxHP
    parry = 3 + (DX/2)

class baseNPC:
    name = "Mook"
    equippedArmor = "None"
    armorDesc = ""
    armorWgt = 0
    armorDR = 0
    ST = 10
    DX = 10
    IQ = 10
    HT = 10
    maxHP = ST
    tempHP = maxHP
    parry = 3 + (DX/2)

def equipArmor(char, armor):
    char.armorDesc = armor.desc
    char.armorWgt = armor.weight
    char.armorDR = armor.DR
    char.equippedArmor = armor.name

def unequipArmor(char):
    char.armorDesc = noArmor.desc
    char.armorWgt = noArmor.weight
    char.armorDR = noArmor.DR
    char.equippedArmor = noArmor.name

def roll(skill):
    y = 0
    i = 0
    result = ""
    attString = ""
    for i in range(3):
        x = random.randrange(1,7)
        if i == 0:
            attString += str(x)
        else:
            attString += ", " + str(x)
        y += x
        continue
    print(attString)
    print("Total = ", y)
    if y > skill:
        print(Fore.RED + "Test failed.")
        result = 1
    elif y == 4:
        print(Fore.GREEN + "Automatic Success!")
        result = 3
    elif y == 3:
        print(Fore.GREEN + "Critical Success!")
        result = 4
    elif y == 17:
        print(Fore.RED + "Automatic Failure")
        result = 1
    elif y == 18:
        print(Fore.RED + "Critical Failure!")
        result = 0
    else:
        print(Fore.GREEN + "Success!")
        result = 2
    print(Style.RESET_ALL)
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
    defence = 0
    dmg = 0
    if result == 2:
        print(f"{target.name} attempts to defend!")
        defence = roll(target.parry)
        if defence > 1:
            dmg = 0
            print(f"{target.name} fended off the attack!")
        else: dmg = rollDmg(1,-2)
    else:
        if result == 3:
            dmg = rollDmg(1,-2)
        elif result == 4:
            dmg = 4
            print("Total Damage = ", dmg)
        elif result == 1:
            print("Whiff! No damage dealt.")
        elif result == 0:
            print("""Eventually, we'll have a crit fail chart for this.
            For now, you just suck.""")
    target.tempHP -= dmg
    print(f"{target.name} has {target.tempHP} HP remaining.")

def gamestart():
    player.name = input("What is your name? ")
    print("""A drunken thug staggers from the shadows, shouting explitives.
        Swaying, he raises his fists, and you do the same.""")
    foe = baseNPC()
    gameloop(foe)

def gameloop(enemy):
    turn = 1
    while player.tempHP > 0 and enemy.tempHP > 0:
        if turn%2 == 1:
            if turn == 1:
                fight = input("Attack? (Y/N)")
            else:
                fight = input("Continue attacking? (Y/N) ")
            if fight == "Y" or fight == "y":
                attack(player.DX, enemy)
            else:
                print("You get away safely! (You coward.)")
                break
        else:
            attack(enemy.DX, player)
        if player.tempHP < 1:
            print("You collapse in the mud, beaten and ashamed.")
        elif enemy.tempHP < 1:
            print("Your foe crumples in a heap, and you stand victorious.")
        else:
            turn += 1
            print(f"Turn #{turn}")
