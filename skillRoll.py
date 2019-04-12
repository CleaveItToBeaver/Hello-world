import random
import json
from colorama import Fore, Style

class armor:
    DR = 0
    description = "Naked as the day you were born. You savage."
    weight = 0
    value = 0
    name = "lack of"
    ID = "Naked"

class mWep:
    TL = 0
    name = "Melee Weapon"
    dmgSrc = "sw"
    dmgMod = +2
    dmgType = "cut"
    cost = 50
    weight = 4
    ST = 11
    skill = "Axe/Mace"
    default = "DX"
    defaultMod = -5
    reach = 1
    handed = 1

cloth = armor()
cloth.name = "Cloth"
cloth.desc = "Commoner's clothes. Woolen tunic, tattered robes, what-have-you."
cloth.weight = 12
cloth.value = 150
cloth.DR = 1
cloth.ID = "Cloth"

noArmor = armor()
noArmor.name = "lack of"
noArmor.desc = "Naked as the day you were born. You savage."
noArmor.weight = 0
noArmor.value = 0
noArmor.DR = 0
noArmor.ID = "Naked"

club = mWep()
club.TL = 0
club.name = "Club"
club.dmgSrc = "Sw"
club.dmgMod = +2
club.cost = 50
club.weight = 4
club.ST = 11
club.skill = "Axe/Mace"
club.default = "DX"
club.defaultMod = -5
club.reach = 1
club.handed = 1

unarmed = mWep()
unarmed.TL = 0
unarmed.name = "Bare Hands"
unarmed.dmgSrc = "Thr"
unarmed.dmgMod = 0
unarmed.cost = 0
unarmed.weight = 0
unarmed.ST = 0
unarmed.skill = "Brawl"
unarmed.default = "DX"
unarmed.defaultMod = 0
unarmed.reach = 0
unarmed.handed = 1

class baseHuman(object):
    name = "Player"
    equippedArmor = noArmor
    equippedWeapon = unarmed
    ST = 10    
    DX = 10
    IQ = 10
    HT = 10
    tempHP = ST

    def __init__(self, DX = 10, HT = 10, IQ = 10, ST = 10):
        print("Init running")
        self.speed = (DX + HT)/4
        self.maxHP = ST
        self.tempHP = self.maxHP
        self.parry = 3 + (DX/2)
        
    @property
    def speed(self):
        print("Getter running")
        self._speed = (self.DX + self.HT)/4
        return(self._speed)

    @speed.setter
    def speed(self, value):
        print("Setter running")
        self._speed = (self.DX + self.HT) / 4

    @property
    def maxHP(self):
        self._maxHP = self.ST
        return(self._maxHP)

    @maxHP.setter
    def maxHP(self, value):
        self._maxHP = self.ST

    @property
    def parry(self):
        self._parry = 3 + (self.DX/2)
        return(self._parry)

    @parry.setter
    def parry(self, value):
        self._parry = 3 + (self.DX/2)

    Thr = 1, -2
    Sw = 1, 0

def equipArmor(target, ID):
    armorL = {}
    with open('armor.txt') as infile:
        armorL = json.load(infile)

    for x in armorL['armor']:
        if x["ID"] == str(ID):
            print(x)
            ID = armor()
            ID.name = x["name"]
            ID.desc = x["desc"]
            ID.weight = x["weight"]
            ID.value = x["value"]
            ID.DR = x["DR"]
            ID.ID = x["ID"]                
            target.equippedArmor = ID
        else: pass

	

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

    
def attack(char, skill, target):
    result = roll(skill)
    defence = 0
    dmg = 0
    dice = getattr(char, char.equippedWeapon.dmgSrc)
    if result == 2:
        print(f"{target.name} attempts to defend!")
        defence = roll(target.parry)
        if defence > 1:
            dmg = 0
            print(f"{target.name} fended off the attack!")
        else:
            dmg = rollDmg(dice[0], dice[1]+club.dmgMod)
            print(f"{char.name}'s {char.equippedWeapon.name} deals {dmg} damage!")
    else:
        if result == 3:
            dmg = rollDmg(dice[0], dice[1]+club.dmgMod)
            print(f"{char.name}'s {char.equippedWeapon.name} deals {dmg} damage!")
        elif result == 4:
            dmg = 4
            print(f"{char.name}'s {char.equippedWeapon.name} deals {dmg} damage!")
        elif result == 1:
            print("Whiff! No damage dealt.")
        elif result == 0:
            print("""Eventually, we'll have a crit fail chart for this.
            For now, you just suck.""")
    if dmg - target.equippedArmor.DR < 1 and dmg != 0:
        dmg = 0
        print(f"The attack fails to penetrate {target.name}'s {target.equippedArmor.DR} armor!")
    elif dmg == 0:
        pass    
    else:
        dmg -= target.equippedArmor.DR
        print(f"{target.name}'s {target.equippedArmor.name} armor soaks {target.equippedArmor.DR} points of damage!")
        target.tempHP -= dmg
    print(f"{target.name} has {target.tempHP} HP remaining.")

def start():
    PC = baseHuman()
    PC.name = input("What is your name? ")
    print("""A drunken thug staggers from the shadows, shouting explitives.
        Swaying, he raises his fists, and you do the same.""")
    foe = baseHuman()
    foe.name = "Faceless thug"
    PC.equippedWeapon = club
    PC.equippedArmor = cloth

    gameloop(PC, foe)

def gameloop(PC, enemy):
    turn = 1
    while PC.tempHP > 0 and enemy.tempHP > 0:
        print(f"Turn #{turn}")
        if turn%2 == 1:
            if turn == 1:
                fight = input("Attack? (Y/N)")
            else:
                fight = input("Continue attacking? (Y/N) ")
            if fight == "Y" or fight == "y":
                attack(PC, PC.DX, enemy)
            else:
                print("You get away safely! (You coward.)")
                break
        else:
            attack(enemy, enemy.DX, PC)
        if PC.tempHP < 1:
            print("You collapse in the mud, beaten and ashamed.")
        elif enemy.tempHP < 1:
            print("Your foe crumples in a heap, and you stand victorious.")
        else:
            turn += 1
            
test = baseHuman()
test.equippedArmor = cloth
test.equippedWeapon = club
#start()
