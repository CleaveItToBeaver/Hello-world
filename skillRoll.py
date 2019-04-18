import random
import json
from colorama import Fore, Style, init
init(convert=True)

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

noArmor = armor()
noArmor.name = "lack of"
noArmor.desc = "Naked as the day you were born. You savage."
noArmor.weight = 0
noArmor.value = 0
noArmor.DR = 0
noArmor.ID = "Naked"

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

class baseHuman():
    name = "Player"
    equippedArmor = noArmor
    equippedWeapon = unarmed
    ST = 10    
    DX = 10
    IQ = 10
    HT = 10
    Thr = [1, -2]
    Sw = [1, 0]
    CP = 0
    SP = 0
    shock = 0

    def __init__(self, DX = 10, HT = 10, IQ = 10, ST = 10):
        print("Init running")
        self.speed = (DX + HT)/4
        self.maxHP = ST
        self.tempHP = self.maxHP
        self.parry = 3 + (DX/2)
        self.setDmg()
        self.move = int(self.speed)

    def setDmg(self):
        stL = {}
        with open('stTable.txt') as infile:
            stL = json.load(infile)

        for x in stL['dmgTable']:
            if x["ST"] == self.ST:
                #print(x)
                self.Thr[0] = x["thrDice"]
                self.Thr[1] = x["thrMod"]
                self.Sw[0] = x["swDice"]
                self.Sw[1] = x["swMod"]
        infile.close()
        
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

    @property
    def move(self):
        self._move = int(self.speed)
        return(self._move)

    @move.setter
    def move(self, value):
        self._move = int(self.speed)


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
    infile.close()

def equipWeapon(target, ID):
    weaponL = {}
    with open('weapons.txt') as infile:
        weaponL = json.load(infile)

    for x in weaponL['weapons']:
        if x["ID"] == str(ID):
            print(x)
            ID = mWep()
            ID.name = x["name"]
            ID.TL = x["TL"]
            ID.dmgSrc = x["dmgSrc"]
            ID.dmgMod = x["dmgMod"]
            ID.dmgType = x["dmgType"]
            ID.cost = x["cost"]
            ID.weight = x["weight"]
            ID.ST = x["ST"]
            ID.skill = x["skill"]
            ID.default = x["default"]
            ID.defaultMod = x["defaultMod"]
            ID.reach = x["reach"]
            ID.handed = x["handed"]
            ID.ID = x["ID"]
            target.equippedWeapon = ID
        else: pass
    infile.close()
    

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
    print(f"Rolling against a skill of {skill}")
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
    mod = skill - char.shock
    if char.shock > 0:
        print(f"{char.name} attacks with -{char.shock} shock!")
    result = roll(mod)
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
            dmg = rollDmg(dice[0], dice[1]+char.equippedWeapon.dmgMod)
            print(f"{char.name}'s {char.equippedWeapon.name} deals {dmg} damage!")
    else:
        if result == 3:
            dmg = rollDmg(dice[0], dice[1]+char.equippedWeapon.dmgMod)
            print(f"{char.name}'s {char.equippedWeapon.name} deals {dmg} damage!")
        elif result == 4:
            dmg = (dice[0]*6) + (dice[1]+char.equippedWeapon.dmgMod)
            print(f"{char.name}'s {char.equippedWeapon.name} deals {dmg} damage!")
        elif result == 1:
            print("Whiff! No damage dealt.")
        elif result == 0:
            print("""Eventually, we'll have a crit fail chart for this.
            For now, you just suck.""")
    if dmg - target.equippedArmor.DR < 1 and dmg != 0:
        dmg = 0
        print(f"The attack fails to penetrate {target.name}'s ({target.equippedArmor.DR} DR) {target.equippedArmor.name} armor!")
    elif dmg == 0:
        pass    
    else:
        dmg -= target.equippedArmor.DR
        print(f"{target.name}'s {target.equippedArmor.name} armor soaks {target.equippedArmor.DR} points of damage!")
        if char.equippedWeapon.dmgType == "pi-":
            dmg -= int(dmg/2)
            if dmg == 0: dmg = 1
            print(f"The small piercing weapon deals half damage after DR... ({dmg})")
        elif char.equippedWeapon.dmgType == "cut" or char.equippedWeapon.dmgType == "pi+":
            dmg += int(dmg/2)
            print(f"Cutting and large piercing attacks deal 50% more damage after DR! ({dmg})")
        elif char.equippedWeapon.dmgType == "imp":
            dmg += dmg
            print(f"Impaling weapons deal double damage after DR! ({dmg})")
        else:
            pass
        target.tempHP -= dmg
        if dmg > 4:
            target.shock = 4
        else:
            target.shock = dmg
    print(f"{target.name} has {target.tempHP} HP remaining.")
    char.shock = 0

def start():
    PC = baseHuman()
    foe = baseHuman()
    victory = 1
    foe.name = "Faceless thug"
    equipWeapon(PC, "rapier")
    print(f"Equipping {PC.name}'s Weapon")
    equipArmor(PC, "Plate")
    print(f"Equipping {PC.name}'s Armor")
    equipWeapon(foe, "Axe")
    print(f"Equipping {foe.name}'s Weapon")
    equipArmor(foe, "Leather")
    print(f"Equipping {foe.name}'s armor")
    PC.name = input("What is your name? ")
    print(f"""A drunken thug staggers from the shadows, shouting explitives.
        Swaying, he raises his {foe.equippedWeapon.name}, and you ready your {PC.equippedWeapon.name}.""")
    while victory == 1:
        foe.tempHP = foe.maxHP
        victory = gameloop(PC, foe)

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
            return(0)
        elif enemy.tempHP < 1:
            print("Your foe crumples in a heap, and you stand victorious.")
            fight = input("Face a new combatant? (Y/N)")
            if fight == "Y" or fight == "y":
                return(1)
            else:
                print("You retire to your chambers to rest and recouperate.")
                return(0)
        else:
            turn += 1
            
test = baseHuman()
equipArmor(test, "Cloth")
equipWeapon(test, "poleaxe")
#test.equippedArmor = cloth
#test.equippedWeapon = club
start()
