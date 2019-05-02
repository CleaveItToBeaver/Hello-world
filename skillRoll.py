import random
import json
from colorama import Fore, Style, init
init(convert=True)

gearL = {}
mobL = {}
#mobL - name, floor, stats, SM, weapon, armor
#Adjust attack function to use SM
mobT = []
#mobT - name, level, special loot[name, value], loot table
lootTabA = []
lootTabW = []
#Add claws as weapon, natural armor to armor table
lootTabT = []
#Add useful treasure + master loot table, magic items

class armor():
    DR = 0
    description = "Naked as the day you were born. You savage."
    weight = 0
    value = 0
    name = "lack of"
    ID = "Naked"

class mWep():
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
    shock = 0
    dead = 0
    defend = 1
    SM = 0

    def __init__(self, DX = 10, HT = 10, IQ = 10, ST = 10):
        #print("Init running")
        self.dead = 0
        self.dCheck = 0
        self.speed = (DX + HT)/4
        self.maxHP = ST
        self.tempHP = self.maxHP
        self.parry = 3 + int(DX/2)
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
        #print("Getter running")
        self._speed = (self.DX + self.HT)/4
        return(self._speed)

    @speed.setter
    def speed(self, value):
        #print("Setter running")
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

class playerClass(baseHuman):
    CP = 0
    cuP = 0
    SP = 0
    GP = 0
    EP = 0
    PP = 0
    inventory = []
    lost = 0
    pursued = 0
    floor = 1
    room = 0

def loadGear():
    gearL = {}
    with open('loot.txt') as infile:
        gearL = json.load(infile)
    infile.close()
    y = 0
    for x in gearL['armor']:
        y += 1
        print(y)
        aTup = (x['ID'], x['value'])
        lootTabA.append(aTup)
    for x in gearL['weapons']:
        y += 1
        print(y)
        aTup = (x['ID'], x['cost'])
        lootTabW.append(aTup)
    for x in gearL['treasure']:
        y += 1
        print(y)
        aTup = (x['name'], x['value'], x['tag'])
        lootTabT.append(aTup)
    return(gearL)

def loadMobs():
    mobL = {}
    with open('Mobs.txt') as infile:
        mobL = json.load(infile)
    infile.close()
    y = 0
    for x in mobL['mobs']:
        y += 1
        print(y)
        aTup = (x['ID'], x['floor'], x['spLoot'], x['lTab'])
        mobT.append(aTup)
    return(mobL)

def wanderingMonster(floor=1):
    select = []
    for x in mobL['mobs']:
        if x['floor'] == floor:
            select.append(x['ID'])
        else: pass
    mob = random.choice(select)
    ID = instMob(mob)
    return(ID)

def instMob(ID):
    for x in mobL['mobs']:
        if x["ID"] == str(ID):
            print(x)
            print("\n")
            ID = baseHuman()
            ID.name = x["name"]
            ID.desc = x["desc"]
            ID.ST = x["ST"]
            ID.DX = x["DX"]
            ID.IQ = x["IQ"]
            ID.HT = x["HT"]
            ID.floor = x["floor"]
            equipWeapon(ID, x['weapon'])               
            equipArmor(ID, x['armor'])
        else: pass
    return(ID)

def equipArmor(target, ID):

    for x in gearL['armor']:
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

def equipWeapon(target, ID):
    for x in gearL['weapons']:
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
#---------Loot Draw----------------
def lootArmor():
    loot = random.choices(lootTabA, [0, 35, 30, 15, 10, 5, 5])
    #lootTable, Weights per list item
    return loot[0][0]

def lootWeapon():
    loot = random.choices(lootTabW, [0, 35, 30, 15, 10, 5, 5])
    return loot[0][0]

def lootTreasure():
    loot = random.choices(lootTabT, [25, 25, 15, 15, 10, 4, 3, 3])
    return loot[0][0]

def drawLoot(char, iT, level=1):
    if iT == 'armor':
        item = lootArmor()
        index = [i for i, v in enumerate(lootTabA) if v[0] == item].pop()
        char.inventory.append([lootTabA[index], 1])
    elif iT == 'weapon':
        item = lootWeapon()
        index = [i for i, v in enumerate(lootTabW) if v[0] == item].pop()
        char.inventory.append([lootTabW[index], 1])
    elif iT == 'treasure':
        item = lootTreasure()
        index = [i for i, v in enumerate(lootTabT) if v[0] == item].pop()
        if lootTabT[index][0] == "CP":
            char.cuP += 1000*level
            print(f"Gained {1000*level} copper pieces!")
        elif lootTabT[index][0] == "SP":
            char.SP += 1000*level
            print(f"Gained {1000*level} silver pieces!")
        elif lootTabT[index][0] == "EP":
            char.EP += 750*level
            print(f"Gained {750*level} electrum pieces!")
        elif lootTabT[index][0] == "GP":
            char.GP += 250*level
            print(f"Gained {250*level} gold pieces!")
        elif lootTabT[index][0] == "PP":
            char.PP += 100*level
            print(f"Gained {100*level} platinum pieces!")
        else:
            item = lootTabT[index][0]
            if item == "Gems":
                y = 0
                for i in range(level):
                    x = random.randrange(1,5)
                    y += x
            elif item == "Jewelery":
                y = level
            else: y = 1
            print(f"Found {y} {lootTabT[index][0]}!")
            dupe = 0
            for i in char.inventory:
                if i[0][0] == item:
                    i[1] += y
                    dupe = 1
                else:
                    pass
            if dupe == 0:
                char.inventory.append([lootTabT[index], y])
            #else: char.inventory.append([lootTabT[index], 1])
           
#---------Loot End-----------------
#---------Debug Functions----------
def massLoot():
	i = 0
	while i < 10:
		drawLoot(test, 'treasure')
		i += 1
#---------End Debug Functions------
            
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

    
def attack(char, skill, target, dType="N"):
    result = 0
    mod = skill - char.shock
    if char.shock > 0:
        print(f"\n{char.name} attacks with -{char.shock} shock!")
    else:
        print(f"\n{char.name} attacks!")
    result = roll(mod)
    print(f"Result: {result}")
    defence = 0
    dmg = 0
    tempdice = getattr(char, char.equippedWeapon.dmgSrc)
    dice = []
    dice.extend(tempdice)
    print(dice)
    if dType == "s" or dType == "S":
        if dice[0] > 2:
            dice[1] += dice[0]
        else:
            dice[1] += 2
    else:
        pass
    print(dice)
    if result == 2 and target.defend > 0:
        print(f"\n{target.name} attempts to defend!")
        if target.defend == 1:
            defence = roll(target.parry)
        elif target.defend == 2:
            defence = roll(target.parry+2)
        if defence > 1:
            dmg = 0
            print(f"{target.name} fended off the attack!")
        else:
            dmg = rollDmg(dice[0], dice[1]+char.equippedWeapon.dmgMod)
            print(f"{char.name}'s {char.equippedWeapon.name} deals {dmg} damage!")
    elif result == 2 and target.defend == 0:
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
    if target.tempHP <= (target.maxHP*-5):
        target.dead = 1
        print(f"{target.name} dies from extreme damage.")
    elif target.tempHP <= 0 and abs(int(target.tempHP/target.maxHP)) > target.dCheck:
        target.dCheck = abs(int(target.tempHP/target.maxHP))
        print(f"{target.name} makes a Death Check at -{target.dCheck}:")
        survival = roll(target.HT-target.dCheck)
        if survival < 2:
            target.dead = 1
            print(f"{target.name} succumbs to their wounds and perishes.")
    print(Fore.YELLOW + f"{target.name} has {target.tempHP} HP.")
    print(Style.RESET_ALL)

def start():
    
    PC = playerClass()
    foe = baseHuman()
    status = 1
    #Status 1 for arena, 2 for town, 3 for dungeon, 4 for menu. 0 ends the game.

    #Prime enemy
    foe.name = "Faceless thug"
    print(f"Equipping {foe.name}'s armor")
    rArmor = random.choice(gearL['armor'])
    equipArmor(foe, rArmor['ID'])
    
    print(f"Equipping {foe.name}'s Weapon")
    rWeap = random.choice(gearL['weapons'])
    equipWeapon(foe, rWeap['ID'])
    
    #Prime Player
    PC.name = input("What is your name? ")
    PC.SP += 3200
    PC.CP += 15
    print(f"Equipping {PC.name}'s Weapon")
    equipWeapon(PC, "rapier")
    print(f"Equipping {PC.name}'s Armor")
    equipArmor(PC, "Plate")
    
    while status != 0:
        print(Style.RESET_ALL)
        PC.SP += (PC.cuP*.1) + (PC.EP/2) + (PC.GP*10) + (PC.PP*50)
        PC.cuP = 0
        PC.EP = 0
        PC.GP = 0
        PC.PP = 0
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
                foe.dead = 0
                state = combatloop(PC, foe)
                if state > 0:
                    status = victory(PC, 'arena')
                else: status = 0

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
    while PC.dead == 0 and enemy.dead == 0:
        print(Fore.CYAN + Style.DIM + f"Turn #{turn}")
        print(Style.RESET_ALL)
        if turn%2 == 1:
            PC.defend = 1
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
                attType = input("""\n[N]ormal attack, [A]ll-Out Attack (no defence),
All-Out [D]efend, or [R]eady an item? """)
                if attType == "n" or attType == "N":
                    attack(PC, PC.DX, enemy)
                elif attType == "A" or attType == "a":
                    PC.defend = 0
                    aoa = input("""\n[D]etermined (+4 to hit);
Dou[b]le (2 attacks with weapon that doesn't need to be readied,
or dual wielded weapons);
[S]trong (+2 dmg or +1/die, whichever is better) """)
                    if aoa == "D" or aoa == "d":
                        attack(PC, PC.DX+4, enemy)
                    elif aoa == "b" or aoa == "B":
                        attack(PC, PC.DX, enemy)
                        attack(PC, PC.DX, enemy)
                    elif aoa == "s" or aoa == "S":
                        attack(PC, PC.DX, enemy, aoa)
                elif attType == "d" or attType == "D":
                    PC.defend = 2
                elif attType == "r" or attType == "R":
                    print("Currently does nothing. ")
                    
            else:
                print("You get away safely! (You coward.)")
                return(0)
            PC.shock = 0
        else:
            enemy.defend = 1
            if enemy.tempHP < 0:
                saveMod = abs(int(enemy.tempHP/enemy.maxHP))
                print(f"{enemy.name} makes a Death Check at -{saveMod}:")
                save = roll(enemy.HT-saveMod) 
                if save < 2:
                    print("""Your foe crumples in a heap, and you stand 
victorious. """)
                    enemy.dead = 1
            if enemy.dead == 0:
                AT = random.randrange(1, 50)
                if AT < 30:
                    attack(enemy, enemy.DX, PC)
                else:
                    print(f"{enemy.name} drops their guard and delivers a precise strike!")
                    attack(enemy, enemy.DX+4, PC)
                    enemy.defend = 0
            enemy.shock = 0                    
        if enemy.dead == 1:
            #state = victory(PC)
            #print(state)
            return(1)
        elif PC.dead == 1:
            return(0)
        else:
            turn += 1

def victory(PC, loc, enemy='none'):
    if loc == 'arena':
        reward = random.randrange(20, 100)
        print(f"""You are awarded {reward} silver pieces for your triumph.\n""")
        PC.SP += reward
        print(f"You now have {PC.SP} silver pieces.")
        fight = input(f"You have {PC.tempHP} HP remaining. Face a new combatant? (Y/N)")
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

def townloop(PC):
    print(Style.RESET_ALL)
    opt = input("""Town is under construction. Pay for [h]ealing; [T]rain Stats;
Buy [C]P;  [S]ell loot; Press [r] to return. """)
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
    elif opt == "s" or opt == "S":
        ask = input("Sell vendor [t]rash?")
        if ask == "t" or ask == "T":
            total = 0
            for i in PC.inventory:
                if i[0][2] == "trash":
                    total = (i[1] * i[0][1])
                    PC.SP += int(total)
                    print(f"Gained {total} SP for {i[1]}x {i[0][0]}.")
                    i.pop()
                else:
                    pass
            print(f"You now have {PC.SP} SP.")

#--------Dungeon Rooms-----------        
def sidePassage(PC, ex):
    if ex%2 == 1:
            passage = "There is a glint in the passage."
    else: passage = ""
    c = input(f"Side Passage. {passage} [C]ontinue past it, or [t]ake the passage?")
    if c == "t" or c == "T":
        if passage != "":
            t = random.randrange(1, 21)
            if t < 3: print("Wandering monster.")
            elif t > 2 and t < 5: print("Trap!")
            elif t > 4 and t < 7: print("Valuable item!")
            else: print("Just a reflection from a shallow puddle.")
        else: print("You take the passage without incident.")
    elif c == "c" or c == "C": print("You continue forward safely.")

def passage(PC):
    print("The passage continues straight for 60 feet.")
    if PC.lost > 0:
        print("You feel like you're wandering in circles.")
        PC.room = random.randrange(1, 11)

def door(PC):
    c = input("A locked door. [F]orce it, or [c]ontinue onward?")
    if c == "c" or c == "C": print("You continue forward safely.")
    elif c == "f" or c == "F":
        force = 0
        bail = 0
        while force < 2 and bail < 1:
            force = roll(PC.ST)
            if force > 1:
                print("You successfully breach the door.")
                chamber(PC)
            else:
                c = input("The door sticks tight. [T]ry again, or [c]ontinue past?")
                if c == "c" or c == "C":
                    bail = 1
                    print("You continue forward safely.")
                elif c == "t" or c == "T":
                    bail = 0

def chamber(PC):
    print("Chamber/room.")
    contents = random.randrange(1, 21)
    if contents < 13:
        print("This room is bare and its contents picked over.")
        #loot useful stuff? chance
    elif contents > 12 and contents < 15:
        print("Wandering Monster")
    elif contents > 14 and contents < 18:
        print("Treasure and monster!")
        #monster stuff
        drawLoot(PC, "treasure", PC.floor)
    elif contents == 18:
        print("Treasure!")
        drawLoot(PC, "treasure", PC.floor)
    elif contents == 19:
        print("Stairs!")
    elif contents == 20:
        print("Tricks and traps.")

def passageTurn(PC, ex):
    if ex%2 == 1:
            passage = "There is a glint in the passage."
    else: passage = ""
    c = input(f"The passage turns. {passage} [C]ontinue past it, or [b]acktrack?")
    if c == "c" or c == "C":
        if passage != "":
            t = random.randrange(1, 21)
            if t < 3: print("Wandering monster.")
            elif t > 2 and t < 5: print("Trap!")
            elif t > 4 and t < 7: print("Valuable item!")
            else: print("Just a reflection from a shallow puddle.")
        else: print("You take the passage without incident.")
    elif c == "b" or c == "B":
        backtrack = roll(PC.IQ-PC.room)
        if backtrack > 1:
            print("You make your way back.")
            PC.room = 1
        else:
            print("Uh oh, this doesn't look right... You're lost.")
            PC.lost = 1
#--------End Dungeon Rooms--------

def explore(PC):
    ex = 0
    ex = random.randrange(1, 21)
    if PC.lost > 0: PC.room -= 1
    if PC.lost > 0 and PC.room == 0:
        print("This area looks familiar. You regain your bearings.")
        PC.lost = 0
        PC.room = 1
        
    if ex > 0 and ex < 3:
        passage(PC)
            
    elif ex > 2 and ex < 8:
        sidePassage(PC, ex)
                  
    elif ex > 7 and ex < 11:
        door(PC)        
        
    elif ex > 10 and ex < 14:
        chamber(PC)
        
    elif ex > 13 and ex < 17:
        passageTurn(PC, ex)
        
    elif ex == 17:
        back = input("Dead end. Gotta [b]acktrack.")
        if back == "b" or back == "B":
            backtrack = roll(PC.IQ-PC.room)
            if backtrack > 1:
                print("You make your way back.")
                PC.room = 1
            else:
                print("Uh oh, this doesn't look right... You're lost.")
                PC.lost = 1
                
    elif ex == 18:
        c = input("Stairs. [T]ake the stairs, or [c]ontinue past?")
        if c == "C" or c == "c":
            print("You move past without incident.")
            #useful loot chance?
        elif c == "t" or c == "T":
            print("You take the stairs.")
            #Determine floor change + direction - need the poster
            
    elif ex == 19:
        print("Wandering monster!")
        foe = wanderingMonster()
        combatloop(PC, foe)
        #Need monsters, WM function
    elif ex == 20:
        print("Tricks or traps.")
        #Need the poster
    else:
        print("Oops! Rolled out of range.")
                
def dungeonloop(PC):
    print(Style.RESET_ALL)
    PC.floor = 1
    PC.room = 0
    if PC.lost == 0:
        opt = input("Dungeon under construction. [E]xplore the dungeon! Test [l]ooting. Press [r] to return.")
    else:
        opt = input("[E]xplore randomly, hoping to find your way back. ")
        
    if opt == "r" or opt == "R": return(4)
    elif opt == "l" or opt == "L":
        drawLoot(PC, "treasure")
        return(3)
    elif opt == "e" or opt == "E":
        explore(PC)
        PC.room += 1
        return(3)
    
    

gearL = loadGear()
mobL = loadMobs()

test = playerClass()
rArmor = random.choice(gearL['armor'])
equipArmor(test, rArmor['ID'])
rWeap = random.choice(gearL['weapons'])
equipWeapon(test, rWeap['ID'])

#foe = wanderingMonster()

#start()
