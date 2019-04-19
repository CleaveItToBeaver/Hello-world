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
    dCheck = 0

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
        return(self._speed)

    @property
    def maxHP(self):
        self._maxHP = self.ST
        return(self._maxHP)

    @maxHP.setter
    def maxHP(self, value):
        self._maxHP = self.ST
        return(self._maxHP)

    @property
    def parry(self):
        self._parry = 3 + (self.DX/2)
        return(self._parry)

    @parry.setter
    def parry(self, value):
        self._parry = 3 + (self.DX/2)
        return(self._parry)

    @property
    def move(self):
        if self.tempHP < (self.maxHP/3):
            self._move = int(self.speed/2)
        else:
            self._move = int(self.speed)
        return(self._move)

    @move.setter
    def move(self, value):
        if self.tempHP < (self.maxHP/3):
            self._move = int(self.speed/2)
        else:
            self._move = int(self.speed)
        return(self._move)


def equipArmor(target, ID):
    armorL = {}
    with open('armor.txt') as infile:
        armorL = json.load(infile)

    for x in armorL['armor']:
        if x["ID"] == str(ID):
            print(x)
            print("\n")
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
            print("\n")
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
        if target.tempHP <= 0 and abs(int(target.tempHP/target.maxHP)) > dCheck:
            dCheck = abs(int(target.tempHP/target.maxHP))
            roll(target.HT)
    print(Fore.YELLOW + f"{target.name} has {target.tempHP} HP.")
    char.shock = 0
    print(Style.RESET_ALL)

def start():
    PC = baseHuman()
    foe = baseHuman()
    status = 1
    #Status 1 for arena, 2 for town, 3 for dungeon, 4 for menu. 0 ends the game.
    
    foe.name = "Faceless thug"
    print(f"Equipping {PC.name}'s Weapon")
    equipWeapon(PC, "rapier")
    print(f"Equipping {PC.name}'s Armor")
    equipArmor(PC, "Plate")
    print(f"Equipping {foe.name}'s Weapon")
    equipWeapon(foe, "Axe")
    print(f"Equipping {foe.name}'s armor")
    equipArmor(foe, "Leather")
    
    PC.name = input("What is your name? ")
    PC.SP += 3200
    PC.CP += 15
    
    while status != 0:
        print(Style.RESET_ALL)
        destination = input("""\nWhere will you go? Into the [d]ungeons,
to fight in the [a]rena, into [t]own, or [q]uit? """)
        if destination == "a" or destination == "A":
            status = 1
            print("""\nYou decend into a large circular fighting ring, set into the
ground and walled with upright sharpened posts. There is a heavy
wooden portculis across from you, which opens slowly to reveal a
darkened tunnel beyond.\n""")
            print(f"""A drunken thug staggers from the shadows, shouting explitives.
Swaying, he raises his {foe.equippedWeapon.name}, and you ready your
{PC.equippedWeapon.name}.\n""")
            while status == 1:
                foe.tempHP = foe.maxHP
                status = combatloop(PC, foe)

        elif destination == "t" or destination == "T":
            status = 2
            while status == 2:
                status = townloop(PC)

        elif destination == "d" or destination == "D":
            status = 3
            while status == 3:
                status = dungeonloop(PC)
                
        elif destination == "q" or destination == "Q":
            print("You retire for the time being.")
            status = 0

def combatloop(PC, enemy):
    turn = 1
    while PC.tempHP > 0 and enemy.tempHP > 0:
        print(Fore.CYAN + Style.DIM + f"Turn #{turn}")
        print(Style.RESET_ALL)
        if turn%2 == 1:
            if PC.tempHP < 0:
                saveMod = abs(int(PC.tempHP/PC.maxHP))
                save = roll(PC.HT-saveMod) #
                if save < 2:
                    print("""You succumb to your wounds and lose consciousness.
You collapse in the mud, beaten and ashamed. """)
                    return(0)
            if turn == 1:
                fight = input("Attack? (Y/N)")
            else:
                fight = input("Continue attacking? (Y/N) ")
            if fight == "Y" or fight == "y":
                attack(PC, PC.DX, enemy)
            else:
                print("You get away safely! (You coward.)")
                return(0)
        else:
            if enemy.tempHP > 0:
                attack(enemy, enemy.DX, PC)
            else:
                reward = random.randrange(20, 100)
                print(f"""Your foe crumples in a heap, and you stand 
victorious. You are awarded {reward} silver pieces for your triumph.\n""")
                PC.SP += reward
                print(f"You now have {PC.SP} silver pieces.")
                fight = input("You have {PC.tempHP} HP remaining. Face a new combatant? (Y/N)")
                if fight == "Y" or fight == "y":
                    return(1)
                else:
                    opt = input("[Q]uit, or [r]eturn from the arena? ")
                    if opt == "r" or opt == "R":
                        print("You leave the arena.")
                        return(4)
                    else:
                        print("You retire to your chambers to rest and recouperate.")
                        return(0)
        else:
            turn += 1

def townloop(PC):
    print(Style.RESET_ALL)
    opt = input("""Town is under construction. Pay for [h]ealing; [T]rain Stats;
Buy [C]P;  Press [r] to return. """)
    if opt == "r" or opt == "R": return(4)
    elif opt == "t" or opt == "T":
        stat = input("\nRaise a stat? [ST]/10CP [DX]/20CP [IQ]/20CP [HT]/10CP [B]ack ")
        if stat == "b" or stat == "B":
            return(2)
        elif stat == "ST" or stat == "st":
            if (PC.CP - 10) >= 0:
                PC.CP -= 10
                PC.ST += 1
                PC.setDmg()
                print(Fore.GREEN + f"""Your ST is now {PC.ST}! You have {PC.CP} CP remaining.\n""")
                return(2)
            else:
                deficit = abs(PC.CP-10)
                print(f"Sorry, you need {deficit} more CP to advance this stat.")
                return(2)
        elif stat == "DX" or stat == "dx":
            if (PC.CP - 20) >= 0:
                PC.CP -= 20
                PC.DX += 1
                print(Fore.GREEN + f"""Your DX is now {PC.DX}! You have {PC.CP} CP remaining.\n""")
                return(2)
            else:
                deficit = abs(PC.CP-20)
                print(f"Sorry, you need {deficit} more CP to advance this stat.")
                return(2)
        elif stat == "IQ" or stat == "iq":
            if (PC.CP - 20) >= 0:
                PC.CP -= 20
                PC.IQ += 1
                print(Fore.GREEN + f"""Your IQ is now {PC.IQ}! You have {PC.CP} CP remaining.\n""")
                return(2)
            else:
                deficit = abs(PC.CP-20)
                print(f"Sorry, you need {deficit} more CP to advance this stat.")
                return(2)
        elif stat == "HT" or stat == "ht":
            if (PC.CP - 10) >= 0:
                PC.CP -= 10
                PC.HT += 1
                print(Fore.GREEN + f"""Your HT is now {PC.HT}! You have {PC.CP} CP remaining.\n""")
                return(2)
            else:
                deficit = abs(PC.CP-10)
                print(Fore.RED + f"Sorry, you need {deficit} more CP to advance this stat.")
                return(2)
        else:
            print("Enter a valid menu option. ")
            return(2)
    elif opt == "C" or opt == "c":
        buy = input(f"""\nCP (character points) can be purchased for 1000 silver pieces each. You 
currently have {PC.SP} silver pieces.\n Enter an amount to purchase,or go [b]ack. """)
        if (buy.isdigit()):
            buy = int(buy)
            if (PC.SP - (buy*1000)) >= 0:
                PC.SP -= (buy*1000)
                PC.CP += buy
                print(Fore.YELLOW + f"""You now have {PC.CP} CP! You have {PC.SP}
SP remaining.\n""")
                return(2)
            else:
                deficit = abs(PC.SP-(buy*1000))
                print(Fore.RED + f"You require {deficit} more silver.")
                return(2)
        elif buy == "b" or buy == "B":
            return(2)
    elif opt == "h" or opt =="H":
        print("\nA local cleric performs healing spells in exchange for a generous tithe. (10SP/1HP)")
        heal = input("Enter the number of HP to restore, [F] to heal to max, or go [b]ack. ")
        if (heal.isdigit()):
            heal = int(heal)
            if (PC.maxHP - PC.tempHP) >= heal:
                if PC.SP - (heal*10) >= 0:
                    PC.SP -= (heal*10)
                    PC.tempHP += heal
                    print(Fore.GREEN + f"Restored {heal} HP. You now have {PC.tempHP} HP remaining.")
                    return(2)
                else:
                    deficit = abs(PC.SP - (heal*10))
                    print(Fore.RED + "You can't afford that much healing! You need {deficit} more SP.")
                    return(2)
            elif PC.tempHP == PC.maxHP:
                tithe = input("""You don't need any healing, but the Church gladly accepts donations.
Enter an amount to tithe, or go [b]ack. """)
                if (tithe.isdigit()):
                    tithe = int(tithe)
                    PC.SP -= abs(tithe)
                    print("\nThe Church thanks you for your generosity.")
                    return(2)
                elif tithe == "b" or tithe == "B":
                    return(2)
            elif (PC.maxHP - PC.tempHP) < heal:
                heal = PC.maxHP - PC.tempHP
                if PC.SP - (heal*10) >= 0:
                    PC.SP -= (heal*10)
                    PC.tempHP += heal
                    print(Fore.GREEN + f"Restored {heal} HP. You now have {PC.tempHP} HP remaining.")
                    return(2)
        elif heal == "f" or heal == "F":
                heal = PC.maxHP - PC.tempHP
                if PC.SP - (heal*10) >= 0:
                    PC.SP -= (heal*10)
                    PC.tempHP += heal
                    print(Fore.GREEN + f"Restored {heal} HP. You now have {PC.tempHP} HP remaining.")
                    return(2)

                
def dungeonloop(PC):
    print(Style.RESET_ALL)
    opt = input("Dungeon under construction. Press [r] to return.")
    if opt == "r" or opt == "R": return(4)
            
test = baseHuman()
equipArmor(test, "Cloth")
equipWeapon(test, "poleaxe")
#test.equippedArmor = cloth
#test.equippedWeapon = club
#start()
