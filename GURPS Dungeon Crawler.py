import random
import json
from colorama import Fore, Style, init
init(convert=True)

gearL = {}
mobL = {}
#mobL - name, floor, stats, SM, weapon, armor
mobT = []
#mobT - name, level, special loot[name, value], loot table
lootTabA = []
lootTabW = []
lootTabT = []
#Add useful treasure + master loot table, magic items
skillL = {}
#skillL - Skills: name, attribute, diff, level, value
#   Costs: Difficulty (E-VH), default
skT = []
#skT - Name, level, value


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
    Skills = {}
    skillDefault = -5

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
        with open('stTable.json') as infile:
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
    with open('loot.json') as infile:
        gearL = json.load(infile)
    infile.close()
    y = 0
    for x in gearL['armor']:
        y += 1
        print(y)
        aTup = (x['ID'], x['value'], 'armor')
        lootTabA.append(aTup)
    for x in gearL['weapons']:
        y += 1
        print(y)
        aTup = (x['ID'], x['cost'], 'weapon')
        lootTabW.append(aTup)
    for x in gearL['treasure']:
        y += 1
        print(y)
        aTup = (x['name'], x['value'], x['tag'])
        lootTabT.append(aTup)
    return(gearL)

def loadSkills():
    skL = {}
    with open('Skills.json') as infile:
        skL = json.load(infile)
    infile.close()
    y = 0
    for x in skL['Skills']:
        y += 1
        print(y)
        aTup = (x['Name'], x['Attribute'], x['Level'], x['Value'])
        skT.append(aTup)
    return(skL)

def loadMobs():
    mobL = {}
    with open('Mobs.json') as infile:
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
    #Temp - if there's no entry for that floor, just spawn a rat
    if select == []:
        select = ['Rat']
    mob = random.choice(select)
    ID = instMob(mob)
    return(ID)

def instMob(ID):
    for x in mobL['mobs']:
        if x["ID"] == str(ID):
            ID = baseHuman()
            ID.name = x["name"]
            ID.desc = x["desc"]
            ID.SM = x['SM']
            print(ID.desc)
            ID.ST = x["ST"]
            ID.DX = x["DX"]
            ID.IQ = x["IQ"]
            ID.HT = x["HT"]
            ID.floor = x["floor"]
            equipWeapon(ID, x['weapon'])               
            equipArmor(ID, x['armor'])
            ID.setDmg()
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
    loot = random.choices(lootTabA, [0, 0, 35, 30, 15, 10, 5, 5])
    #lootTable, Weights per list item
    return loot[0][0]

def lootWeapon():
    loot = random.choices(lootTabW, [0, 0, 0, 20, 20, 15, 10, 5, 5, 25])
    return loot[0][0]

def lootTreasure():
    loot = random.choices(lootTabT, [25, 25, 15, 15, 10, 4, 3, 3, 0, 0])
    return loot[0][0]

def drawLoot(char, iT, level=1, item=""):
    if iT == 'armor':
        if item == '': item = lootArmor()
        index = [i for i, v in enumerate(lootTabA) if v[0] == item].pop()
        char.inventory.append([lootTabA[index], 1])
        print(Fore.YELLOW +f"Found a {lootTabA[index][0]}!")
    elif iT == 'weapon':
        if item == '': item = lootWeapon()
        index = [i for i, v in enumerate(lootTabW) if v[0] == item].pop()
        char.inventory.append([lootTabW[index], 1])
        print(Fore.YELLOW +f"Found a {lootTabW[index][0]}!")
    elif iT == 'treasure':
        item = lootTreasure()
        index = [i for i, v in enumerate(lootTabT) if v[0] == item].pop()
        if lootTabT[index][0] == "CP":
            char.cuP += 1000*level
            print(Fore.YELLOW +f"Gained {1000*level} copper pieces!")
        elif lootTabT[index][0] == "SP":
            char.SP += 1000*level
            print(Fore.YELLOW +f"Gained {1000*level} silver pieces!")
        elif lootTabT[index][0] == "EP":
            char.EP += 750*level
            print(Fore.YELLOW +f"Gained {750*level} electrum pieces!")
        elif lootTabT[index][0] == "GP":
            char.GP += 250*level
            print(Fore.YELLOW +f"Gained {250*level} gold pieces!")
        elif lootTabT[index][0] == "PP":
            char.PP += 100*level
            print(Fore.YELLOW +f"Gained {100*level} platinum pieces!")
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
            addLoot(index, y, char)
            #else: char.inventory.append([lootTabT[index], 1])
    print(Style.RESET_ALL)

def addLoot(index, qty, char):
    dupe = 0
    item = lootTabT[index][0]
    for i in char.inventory:
        if i[0][0] == item:
            i[1] += qty
            dupe = 1
        else:
            pass
    if dupe == 0:
        char.inventory.append([lootTabT[index], qty])
    print(Fore.YELLOW +f"Gained {qty} {lootTabT[index][0]}!")
    print(Style.RESET_ALL)
           
#---------Loot End-----------------
#---------Debug Functions----------
def massLoot():
	i = 0
	while i < 10:
		drawLoot(test, 'treasure')
		i += 1
#---------End Debug Functions------

def contest(charskill, foeskill):
    t1 = roll(charskill)
    t2 = roll(foeskill)
    if t1[0] > 1 and t2[0] < 2: return(1)
    elif t2[0] > 1 and t1[0] < 2: return(0)
    elif t2[0] < 2 and t1[0] < 2:
        if t2[1] < t1[1]: return(1)
        elif t1[1] < t2[1]: return(0)
    elif t2[0] > 1 and t1[0] > 1:
        if t1[0] > t2[0]: return(1)
        elif t2[0] > t1[0]: return(0)
        elif t2[0] == t1[0]:
            if t2[1] > t1[1]: return(1)
            else: return(0)
            
def roll(skill):
    y = 0
    i = 0
    result = ""
    attString = ""
    margin = 0
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
        margin = y - skill
    print(Style.RESET_ALL)
    return [result, margin]

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
    mod = skill - char.shock + target.SM
    if char.shock > 0:
        print(f"\n{char.name} attacks with -{char.shock} shock!")
    else:
        print(f"\n{char.name} attacks!")
    result = roll(mod)[0]
    print(f"Result: {result}")
    defence = 0
    dmg = 0
    tempdice = getattr(char, char.equippedWeapon.dmgSrc)
    dice = []
    dice.extend(tempdice)
    print(dice)
    if dType.lower() == "s":
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
            defence = roll(target.parry)[0]
        elif target.defend == 2:
            defence = roll(target.parry+2)[0]
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
            #Crit Fail Chart
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
        target.shock += dmg
    if target.tempHP <= (target.maxHP*-5):
        target.dead = 1
        print(f"{target.name} dies from extreme damage.")
    elif target.tempHP <= 0 and abs(int(target.tempHP/target.maxHP)) > target.dCheck:
        target.dCheck = abs(int(target.tempHP/target.maxHP))
        print(f"{target.name} makes a Death Check at -{target.dCheck}:")
        survival = roll(target.HT-target.dCheck)[0]
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
        normalizeCurrency(PC)
        
        destination = input("""\nWhere will you go? Into the [d]ungeons,
to fight in the [a]rena, into [t]own, equip from [i]nventory, or [q]uit? """)
        if destination.lower() == "a":
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

        elif destination.lower() == "t":
            status = 2
            while status == 2:
                status = townloop(PC)

        elif destination.lower() == "d":
            status = 3
            PC.floor = 1
            PC.room = 0
            PC.lost = 0
            while status == 3:
                status = dungeonloop(PC)

        elif destination.lower() == 'i':
            intinv(PC)
                
        elif destination.lower() == "q":
            print("You retire for the time being.")
            status = 0

def normalizeCurrency(PC):
    PC.SP += (PC.cuP*.1) + (PC.EP/2) + (PC.GP*10) + (PC.PP*50)
    PC.cuP = 0
    PC.EP = 0
    PC.GP = 0
    PC.PP = 0

def combatloop(PC, enemy):
    turn = 1
    while PC.dead == 0 and enemy.dead == 0:
        print(Fore.CYAN + Style.DIM + f"Turn #{turn}")
        print(Style.RESET_ALL)
        if turn%2 == 1:
            PC.defend = 1
            if PC.tempHP < 0:
                saveMod = abs(int(PC.tempHP/PC.maxHP))
                print(f'You make a Death Check at -{saveMod}: ')
                save = roll(PC.HT-saveMod)[0]
                if save < 2:
                    print("""You succumb to your wounds and lose consciousness.
You collapse in the mud, beaten and ashamed. """)
                    return(0)
            if turn == 1:
                fight = input("Attack? (Y/N)")
            else:
                fight = input("Continue attacking? (Y/N) ")
            if fight.lower() == "y":
                attType = input("""\n[N]ormal attack, [A]ll-Out Attack (no defence),
All-Out [D]efend, or [R]eady an item? """)
                if attType.lower() == "n":
                    attack(PC, PC.DX, enemy)
                elif attType == "a":
                    PC.defend = 0
                    aoa = input("""\n[D]etermined (+4 to hit);
Dou[b]le (2 attacks with weapon that doesn't need to be readied,
or dual wielded weapons);
[S]trong (+2 dmg or +1/die, whichever is better) """)
                    if aoa.lower() == "d":
                        attack(PC, PC.DX+4, enemy)
                    elif aoa.lower() == "b":
                        attack(PC, PC.DX, enemy)
                        attack(PC, PC.DX, enemy)
                    elif aoa.lower() == "s":
                        attack(PC, PC.DX, enemy, aoa)
                elif attType.lower() == "d":
                    PC.defend = 2
                elif attType.lower() == "r":
                    ready = input("[R]eady your weapon, or [a]ccess your inventory?")
                    if ready.lower() == "r":
                        print("You ready your weapon.")
                    elif ready.lower() == "a":
                        intinv(PC)
                    
            else:
                run = input("Really run away? Y/N ")
                if run.lower() == 'y':
                    chk = contest(PC.HT, enemy.HT)
                    if chk == 1:
                        print("You get away safely! (You coward.)")
                        return(0)
                    else:
                        print("Your foe isn't letting you get away that easy! ")
            PC.shock = 0
        else:
            enemy.defend = 1
            if enemy.tempHP < 0:
                saveMod = abs(int(enemy.tempHP/enemy.maxHP))
                print(f"{enemy.name} makes a Death Check at -{saveMod}:")
                save = roll(enemy.HT-saveMod)[0] 
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
        if fight.lower() == "y":
            return(1)
        else:
            opt = input("[Q]uit, or [r]eturn from the arena? ")
            if opt.lower() == "r":
                print("You leave the arena.")
                return(4)
            else:
                print("You retire to your chambers to rest and recouperate.")
                return(0)
    elif loc == "dungeon":
        if enemy == 'none':
            pass
        else:
            for x in mobL['mobs']:
                if enemy == x['name']:
                    if x['spLoot'] != "None":
                        item = x['spLoot']
                        index = [i for i, v in enumerate(lootTabT) if v[0] == item].pop()
                        addLoot(index, int(x['spLootQty']), PC)
                        print(f"You recover a {x['spLoot']} from the corpse!")
                    if x['spLoot'] == "None" and x['lTab'] != "None":
                        drawLoot(PC, x['lTab'], PC.floor)
                else: pass
        

def townloop(PC):
    print(Style.RESET_ALL)
    opt = input("""Town is under construction. Pay for [h]ealing; Train s[T]ats
or s[K]ills; Buy [C]P;  [S]ell loot; Equip from [I]nventory;
Press [r] to return. """)
    if opt.lower() == "r": return(4)
    elif opt.lower() == 'i':
        intinv(PC)
        return(2)
    elif opt.lower() == "t":
        buyStat(PC)
    elif opt.lower() == "c":
        buyCP(PC)
    elif opt.lower() == "h":
        heals(PC)
    elif opt.lower() == "s":
        sellStuff(PC)
    elif opt.lower() == "k":
        buySkills(PC)

def buyStat(PC):
    stat = input("\nRaise a stat? [ST]/10CP [DX]/20CP [IQ]/20CP [HT]/10CP [B]ack ")
    if stat == "b" or stat == "B":
        return(2)
    elif stat.lower() == "st":
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
    elif stat.lower() == "dx":
        if (PC.CP - 20) >= 0:
            PC.CP -= 20
            PC.DX += 1
            print(Fore.GREEN + f"""Your DX is now {PC.DX}! You have {PC.CP} CP remaining.\n""")
            return(2)
        else:
            deficit = abs(PC.CP-20)
            print(f"Sorry, you need {deficit} more CP to advance this stat.")
            return(2)
    elif stat.lower() == "iq":
        if (PC.CP - 20) >= 0:
            PC.CP -= 20
            PC.IQ += 1
            print(Fore.GREEN + f"""Your IQ is now {PC.IQ}! You have {PC.CP} CP remaining.\n""")
            return(2)
        else:
            deficit = abs(PC.CP-20)
            print(f"Sorry, you need {deficit} more CP to advance this stat.")
            return(2)
    elif stat.lower() == "ht":
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

def buyCP(PC):
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
    elif buy.lower() == "b":
        return(2)

def heals(PC):
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
            elif tithe.lower() == "b":
                return(2)
        elif (PC.maxHP - PC.tempHP) < heal:
            heal = PC.maxHP - PC.tempHP
            if PC.SP - (heal*10) >= 0:
                PC.SP -= (heal*10)
                PC.tempHP += heal
                print(Fore.GREEN + f"Restored {heal} HP. You now have {PC.tempHP} HP remaining.")
                return(2)
    elif heal.lower() == "f":
            heal = PC.maxHP - PC.tempHP
            if PC.SP - (heal*10) >= 0:
                PC.SP -= (heal*10)
                PC.tempHP += heal
                print(Fore.GREEN + f"Restored {heal} HP. You now have {PC.tempHP} HP remaining.")
                return(2)

def sellStuff(PC):
    ask = input("Sell vendor [t]rash?")
    if ask.lower() == "t":
        total = 0
        x = 0
        toDel = []
        for i in PC.inventory:
            if i[0][2] == "trash":
                total = (i[1] * i[0][1])
                PC.SP += int(total)
                print(f"Gained {total} SP for {i[1]}x {i[0][0]}.")
                
                toDel.append(x)
            else:
                pass
            x += 1
        #cleanup
        if not toDel:
            print("Nothing to sell.")
        else:
            toDel.reverse()
            for i in toDel:
                del PC.inventory[i]
                print(i)
            print(f"You now have {PC.SP} SP.")
    return(2)

def buySkills():
    print ("Working on it. Ain't that nice?")
    return(2)

#--------Dungeon Rooms-----------        
def sidePassage(PC, ex):
    if ex%2 == 1:
            passage = "There is a glint in the passage."
    else: passage = ""
    c = input(f"Side Passage. {passage} [C]ontinue past it, or [t]ake the passage?")
    if c.lower() == "t":
        if passage != "":
            t = random.randrange(1, 21)
            if t < 3:
                print("Wandering monster.")
                foe = wanderingMonster(PC.floor)
                end = combatloop(PC, foe)
                if end == 1:
                    victory(PC, 'dungeon', foe.name)
                else: return(0)
            elif t > 2 and t < 5:
                print("Trap!")
                trap(PC)
            elif t > 4 and t < 7:
                print("Valuable item!")
                d = random.randrange(1,20)
                if d > 15:
                    drawLoot(PC, "armor")
                elif d < 16 and d > 10:
                    drawLoot(PC, "weapon")
                else: drawLoot(PC, "treasure")
            else: print("Just a reflection from a shallow puddle.")
        else: print("You take the passage without incident.")
    elif c.lower() == "c": print("You continue forward safely.")

def passage(PC):
    print("The passage continues straight for 60 feet.")
    if PC.lost > 0:
        print("You feel like you're wandering in circles.")
        PC.room = random.randrange(1, 11)

def door(PC):
    c = input("A locked door. [F]orce it, or [c]ontinue onward?")
    if c.lower() == "c": print("You continue forward safely.")
    elif c.lower() == "f":
        force = 0
        bail = 0
        while force < 2 and bail < 1:
            force = roll(PC.ST)[0]
            if force > 1:
                print("You successfully breach the door.")
                chamber(PC)
            else:
                wm = random.randrange(1, 6)
                if wm == 1:
                    print("Wandering Monster")
                    foe = wanderingMonster(PC.floor)
                    end = combatloop(PC, foe)
                    if end == 1:
                        victory(PC, 'dungeon', foe.name)
                    else: return(0)
                c = input("The door sticks tight. [T]ry again, or [c]ontinue past?")
                if c.lower() == "c":
                    bail = 1
                    print("You continue forward safely.")
                elif c.lower() == "t":
                    bail = 0

def chamber(PC):
    print("Chamber/room.")
    contents = random.randrange(1, 21)
    if contents < 13:
        print("This room is bare and its contents picked over.")
        #loot useful stuff? chance
    elif contents > 12 and contents < 15:
        print("Wandering Monster")
        foe = wanderingMonster(PC.floor)
        end = combatloop(PC, foe)
        if end == 1:
            victory(PC, 'dungeon', foe.name)
        else: return(0)
    elif contents > 14 and contents < 18:
        print("Treasure and monster!")
        #stealth check
        foe = wanderingMonster(PC.floor)
        end = combatloop(PC, foe)
        if end == 1:
            victory(PC, 'dungeon', foe.name)
            drawLoot(PC, "treasure", PC.floor)
        else: return(0)
    elif contents == 18:
        print("Treasure!")
        t = random.randrange(1, 4)
        if t == 1: trap(PC)
        drawLoot(PC, "treasure", PC.floor)
    elif contents == 19:
        print("Stairs!")
        stairs(PC)
    elif contents == 20:
        print("Tricks and traps.")
        trap(PC)

def passageTurn(PC, ex):
    if ex%2 == 1:
            passage = "There is a glint in the passage."
    else: passage = ""
    c = input(f"The passage turns. {passage} [C]ontinue past it, or [b]acktrack?")
    if c.lower() == "c":
        if passage != "":
            t = random.randrange(1, 21)
            if t < 3:
                print("Wandering monster.")
                foe = wanderingMonster(PC.floor)
                end = combatloop(PC, foe)
                if end == 1:
                    victory(PC, 'dungeon', foe.name)
                else: return(0)
            elif t > 2 and t < 5:
                trap(PC)
            elif t > 4 and t < 7:
                print("Valuable item!") #Draw valuable item
                d = random.randrange(1,20)
                if d > 15:
                    drawLoot(PC, "armor")
                elif d < 16 and d > 10:
                    drawLoot(PC, "weapon")
                else: drawLoot(PC, "treasure")
            else: print("Just a reflection from a shallow puddle.")
        else: print("You take the passage without incident.")
    elif c.lower() == "b":
        backtrack = roll(PC.IQ-(PC.room-1))[0]
        if backtrack > 1:
            print("You make your way back.")
            PC.room = 0
        else:
            print("Uh oh, this doesn't look right... You're lost.")
            PC.lost = 1

def stairs(PC):
    var = random.randrange(1, 20)
    appearance = ""
    change = 0
    chamber = 0
    if var == 1 or var == 12:
        appearance = "Stairs leading up. "
        change = 1
        result = "You take the stairs up to the next level. "
    elif var > 1 and var < 7:
        appearance = "Stairs leading down. "
        change = -1
        result = "You decend to the next level. "
    elif var  == 7 or var == 13:
        appearance = "Stairs leading down. "
        change = -2
        result = "You decend two levels. "
    elif var == 8:
        appearance = "Stairs leading down. "
        change = -3
        result = "You decend three levels. "
    elif var == 9:
        appearance = "Stairs leading up. "
        chute = random.randrange(1, 6)
        if chute == 1:
            change = -2
            result = """The stairs lead up to what appears to be a dead end, but
as you turn back, a chute opens beneath you! You are deposited two levels down. """
        else:
            change = 0
            result = "The stairs climb upwards, but the top is blocked by rubble. "
    elif var == 10:
        appearance = "Stairs leading down. "
        chute = random.randrange(1, 6)
        if chute == 1:
            change = -1
            result = """The stairs lead down to what appears to be a dead end, but
as you turn back, a chute opens beneath you! You are deposited one level down. """
        else:
            change = 0
            result = "The stairs decend into darkness, but the bottom is blocked by rubble. "
    elif var == 11:
        appearance = "Stairs leading up. "
        chute = random.randrange(1, 6)
        if chute == 1:
            change = 1
            result = """The stairs climb for nearly two levels, but a
chute opens beneath you at the top, and you drop a level. """
        else:
            change = 2
            result = "The stairs climb upwards for two levels. "
    elif var > 13 and var < 17:
        appearance = "A trapdoor in the floor. "
        change = -1
        result = "You decend an old iron ladder to the next level. "
    elif var == 17:
        appearance = "A trapdoor in the floor. "
        change = -2
        result = "You decend an old iron ladder two levels. "
    elif var > 17:
        appearance = "Stairs leading up. "
        change = -1
        result = """The stairs ascend a level, but upon cresting the top of the
landing, retract into a slide and deposit you in a chamber two levels below. """
        chamber = 1

    
    c = input(f"{appearance} [T]ake the stairs, or [c]ontinue past? ")
    if c.lower() == "c":
        print("You move past without incident. ")
        #useful loot chance?
    elif c.lower() == "t":
        print("You take the stairs. ")
        print(result)
        PC.floor = PC.floor - change
        print(f"You are now on level {PC.floor}.")
        if chamber > 0:
            chamber(PC)
#--------End Dungeon Rooms--------

def explore(PC):
    ex = 0
    ex = random.randrange(1, 21)
    if PC.lost > 0: PC.room -= 1
    else: PC.room += 1
    if PC.lost > 0 and PC.room == 0:
        print("This area looks familiar. You regain your bearings.")
        PC.lost = 0
        PC.room = 0
        print(f"Lost = {PC.lost}\t Room = {PC.room}")
        
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
        if back.lower() == "b":
            backtrack = roll(PC.IQ-(PC.room-1))[0]
            if backtrack > 1:
                print("You make your way back.")
                PC.room = 0
            else:
                print("Uh oh, this doesn't look right... You're lost.")
                PC.lost = 1
                
    elif ex == 18:
        stairs(PC)
            
    elif ex == 19:
        print("Wandering monster!")
        foe = wanderingMonster(PC.floor)
        end = combatloop(PC, foe)
        if end == 1:
            victory(PC, 'dungeon', foe.name)
        elif end == 0:
            return(0)
        #Need monsters beyond floor 1
    elif ex == 20:
        print("Tricks or traps.")
        #Need the poster
        trap(PC)
    else:
        print("Oops! Rolled out of range.")

def trap(PC):
    choice = ''
    spot = roll(PC.IQ)[0]
    #randomize triggers, hazards
    darts = random.randrange(2, 4)
    if spot > 1:
        choice = input("You detect a trap! [D]isarm, or [e]vade it?")
    else: PC.defend = 0
    if choice.lower() == 'e':
        print("You gingerly step over the pressure plate, and leave the trap intact for the next unsuspecting soul.")
        return
    elif choice.lower() == 'd':
        disarm = roll(PC.DX)[0]
        if disarm > 1:
            print("You carefully dismantle the trigger mechanism and collect a few spare parts you could probably sell to a scrapper.")
            addLoot(8, darts, PC)
            return
    print(f"A pressure plate sinks beneath your foot, and darts fly from the walls!")
    
    i = 0
    foe = baseHuman()
    foe.name = "Trap"
    equipWeapon(foe, "fangs")
    foe.equippedWeapon.name = "darts"
    while i < darts:
        attack(foe, 12, PC)
        i += 1
    PC.defend = 1
                
def dungeonloop(PC):
    print(Style.RESET_ALL)
    print(f"Lost = {PC.lost}\t Room = {PC.room}\t Floor = {PC.floor}")
    if PC.lost == 0 and PC.room < 1:
        opt = input("Dungeon under construction. [E]xplore the dungeon! "
            "Test [l]ooting. Equip from [i]nventory. Press [r] to return.")
        if opt.lower() == "r":
            if PC.floor < 2: return(4)
            else:
                backtrack = roll(PC.IQ-(PC.room-1))[0]
                if backtrack > 1:
                    print("You successfully ascend to the next floor, and keep your bearings.")
                    PC.room = 0
                else:
                    print("This isn't the way you came down... You ascend one floor, but are lost.")
                    PC.lost = 1
        elif opt.lower() == "l":
            drawLoot(PC, "treasure")
            return(3)
        elif opt.lower() == 'i':
            intinv(PC)
            return(3)
        elif opt.lower() == "e":
            explore(PC)
            if PC.dead == 1: return(0)
            else:
                return(3)
    elif PC.lost > 0:
        opt = input("[E]xplore randomly, hoping to find your way back. ")
        if opt.lower() == "e":
            explore(PC)
            if PC.dead == 1: return(0)
            else:
                return(3)
    elif PC.room > 0 and PC.lost == 0:
        opt = input("Dungeon under construction. [E]xplore the dungeon! [B]acktrack.")
        if opt.lower() == "e":
            explore(PC)
            if PC.dead == 1: return(0)
            else:
                return(3)
        elif opt.lower() == "b":
            if PC.room > 1:
                backtrack = roll(PC.IQ-(PC.room-1))[0]
                if backtrack > 1:
                    print("You make your way back.")
                    PC.room = 1
                    return(3)
                else:
                    print("Uh oh, this doesn't look right... You're lost.")
                    PC.lost = 1
                    return(3)
            else:
                print("You make your way back.")
                PC.room = 0
                return(3)
    
    

gearL = loadGear()
mobL = loadMobs()
skillL = loadSkills()

test = playerClass()
rArmor = random.choice(gearL['armor'])
equipArmor(test, rArmor['ID'])
rWeap = random.choice(gearL['weapons'])
equipWeapon(test, rWeap['ID'])
test.Skills = skT

#foe = wanderingMonster()

#start()
#------------Test stuff for Inventory---------------
def generateMenu():
	for i, each in enumerate(gearL['armor']):	
		tup = (i, each['name'])
		menu.append(tup)
	return menu

def menuSelect():
	for each in menu:
		print(f'{each[0]} - {each[1]}')
	select = input('Enter the number of your selection: ')
	choice = menu[int(select)][1]
	print(f'You chose {choice}.')

#-------------End Test Stuff for Inventory----------

def intinv(char):
    a = input("Do what? Equip [a]rmor, [w]ield weapon, or [u]se an item?")
    if a.lower() == 'a': name = 'armor'
    elif a.lower() == 'w': name = 'weapon'
    elif a.lower() == 'u': name = 'item'
    print(name)
    print(type(name))
    i = 1
    menu = []
    
    for v, each in enumerate(char.inventory):
        if each[0][2] == name:
            tup = (i, each[0][0], v)
            menu.append(tup)
            i += 1
            
    for each in menu:
        print(f'{each[0]} - {each[1]}')

    if menu == []:
        print(f'No useable {name} in your inventory!')
        return
        
    select = input('Enter the number of your selection: ')
    choice = menu[int(select)-1][1]
    if name == 'armor':
        if char.equippedArmor.ID != 'Naked':
            drawLoot(char, 'armor', item = char.equippedArmor.ID)
        equipArmor(char, choice)
        print(menu[int(select)-1])
        toDel = menu[int(select)-1][2]
        print(f'ToDel = {toDel}')
        del char.inventory[toDel]
    elif name == 'weapon':
        if char.equippedWeapon.name != 'Bare Handed':
            drawLoot(char, 'weapon', item = char.equippedWeapon.ID)
        equipWeapon(char, choice)
        print(menu[int(select)-1])
        toDel = menu[int(select)-1][2]
        print(f'ToDel = {toDel}')
        del char.inventory[toDel]
    elif name == 'item':
        print("Not implemented yet.")
        #Adjust when usable items are added.

if __name__ == "__main__":
    start()
