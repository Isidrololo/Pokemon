# Classes and functions to be used in main.py
import os
import csv
import random
import numpy as np

# Classes:
class Pokemon:
    def __init__(self, name, t1, t2, hp, at, df, sat, sdf, spd, lvl):
        # Define Pokemon stats from base stats and level:
        self.name = name                                # Pokemon's name
        self.type1 = t1                                 # Type 1
        self.type2 = t2                                 # Type 2
        self.health  = calculate_hp(hp, lvl)            # Health Points
        self.attack  = calculate_stat(at, lvl)          # Physical Attack
        self.defense = calculate_stat(df, lvl)          # Physical Defense
        self.special_attack = calculate_stat(sat, lvl)  # Special Attack
        self.special_defense = calculate_stat(sdf, lvl) # Special Defense
        self.speed = calculate_stat(spd, lvl)           # Speed
        self.level = lvl                                # level of experience
        if (self.health>0):                             # Is the Pokemon able to combat?
            self.status = "Healthy"
        else:
            self.status = "Fainted"

    # Display all attributes of a Pokemon object:
    def all_attrs(self):
        print("   {:>15}: {}".format("Name",            self.name))
        print("   {:>15}: {}".format("Type 1",          self.type1))
        print("   {:>15}: {}".format("Type 2",          self.type2))
        print("   {:>15}: {}".format("HP",              self.health))
        print("   {:>15}: {}".format("Attack",          self.attack))
        print("   {:>15}: {}".format("Defense",         self.defense))
        print("   {:>15}: {}".format("Special Attack",  self.special_attack))
        print("   {:>15}: {}".format("Special Defense", self.special_defense))
        print("   {:>15}: {}".format("Speed",           self.speed))
        print("   {:>15}: {}".format("Level",           self.level))
        print("   {:>15}: {}".format("Status",          self.status))
        for i in range(1,5):
            if hasattr(self, "move_"+str(i)):
                print("   {:>15}: {}".format("Move #"+str(i), getattr(getattr(self, "move_"+str(i)),"name")))
        print("")

    # Add movements to the Pokemon object:
    def add_move(self, move):
        if   not hasattr(self,"move_1"):
            self.move_1 = move
        elif not hasattr(self,"move_2"):
            self.move_2 = move
        elif not hasattr(self,"move_3"):
            self.move_3 = move
        else:
            self.move_4 = move

    # Reduce health when the Pokemon is attacked:
    def is_attacked(self, attacker: object, nmove):

        # Get attacker movement attributes:
        if   (isinstance(nmove, bool) and nmove==False):
            move = struggle
        elif (isinstance(nmove, int)):
            move = getattr(attacker,"move_"+str(nmove))
        pow = move.power

        # Check if the selected movement has PPs:
        if (move.power_points<=0):
            raise Exception(" ERROR: no PP for movement {} of pokemon {}".format(move.name, attacker.name))

        # Get attacker pokemon level:
        lvl = attacker.level

        # Determine critical movement factor:
        th = int(attacker.speed/2)  # threshold
        th = min(th,255)            # maximum value for threshold
        rn = random.randint(0,255)  # random integer number
        is_crit = None              # the attack has been critical?
        if (rn<th):
            is_crit = True
            crit = 2
        else:
            is_crit = False
            crit = 1

        # Get appropriate attack/defense stats:
        if   (move.category=="Physical"):
            A = attacker.attack
            D = self.defense
        elif (move.category=="Special"):
            A = attacker.special_attack
            D = self.special_defense
        else:
            raise Exception("ERROR: Unknown move type!")
            
        # STAB multiplier:
        stab = 1
        if (attacker.type1==move.type) or (attacker.type2==move.type):
            stab = 1.5

        # Find effectiveness of attacker movement on defender:
        T1 = type_table(move.type,self.type1)
        T2 = type_table(move.type,self.type2)

        # Find random number:
        rn = random.randint(217,255)/255

        # Calculate final damage:
        dmg = ( ( (2*lvl*crit/5 + 2)*pow*A/D )/50 + 2 )*stab*T1*T2*rn

        # Subtract health points from defender:
        self.health -= int(dmg)

        # Has the Pokemon fainted?
        if (self.health<=0):
            self.status = "Fainted"

        # If STRUGGLE has been used:
        if (move.name=="Struggle"):
            attacker.health -= int(dmg/2)
            if (attacker.health<=0):
                attacker.status = "Fainted"
        else:
            # Subtract PP from attack movement:
            move.move_used()
            setattr(attacker,"move_"+str(nmove),move)    

        return is_crit
        
# Write class to create attacks:
class Movement:
    # Define movement base stats:
    def __init__(self, name, typ, cat, pow, acc, pp):
        self.name = name             # Movement name
        self.type = typ              # Type of the move (fire, water, etc.)
        self.category = cat          # Category: physical of special
        self.power = pow             # Power
        self.accuracy = acc          # Accuracy
        self.power_points = pp       # Maximum number of tries allowed in the same combat

    # Reduce PP when the movement is used:
    def move_used(self):
        self.power_points -= 1


#****************************************************************************
#****************************************************************************
#****************************************************************************
# Functions:

# Select random pokemon from Generation I:
def create_pokemon_rand(level):

    # Find random ID:
    ir = random.randint(1,151)

    # Load data from Generation I:
    file = "./Data/data.csv"
    with open(file, "r") as fid:
        datas = csv.reader(fid)
        header = next(datas)[0].split("\t")
        rows = []
        for data in datas:
            rows.append(data)
    datas = []
    for row in rows:
        datas.append(row[0].split("\t"))

    # Find name associated to the random ID:
    name = datas[ir-1][1]

    # Create pokemon object:
    pokemon = create_pokemon(name, level)
    return pokemon

# Create Pokemon object:
def create_pokemon(name, level):

    # Get base stats:
    datadir = "./Data/"
    file = "data.csv"
    rows = []
    with open(datadir + file, "r") as fid:
        data = csv.reader(fid)
        header = next(data)
        for row in data:
            rows.append(row)
    stats = []
    for row in rows:
        stats.append(row[0].split("\t"))

    # Find pokemon:
    ip = None
    if ("nidoran" in name.lower()):
        print("\n    >> En el caso de Nidoran, puedes elegir su sexo biol??gico ('macho' o 'hembra'):\n\t".format(name))
        sexo = input("         >> Selecci??n: ")
        if (sexo.lower()=="macho"):
            name = "nidoran???"
        elif (sexo.lower()=="hembra"):
            name = "nidoran???"
    for ist,stat in enumerate(stats):
        if (stat[1].lower()==name.lower()):
            ip = ist
    if (ip==None):
        print("\n ===> Esa opci??n no es valida, prueba otra vez. Venga, que no puede ser tan dif??cil...")
        pokemon = None
        return pokemon
    data = stats[ip]

    # Create Pokemon object:
    id, name, hp, at, df, sat, sdf, spd, t1, t2 = data
    pokemon = Pokemon(name, t1, t2, int(hp), int(at), int(df), int(sat), int(sdf), int(spd), level)    

    # Add the final 4 moves according to "level":
    file = "{}_{}_moves.csv".format(id.zfill(3), pokemon.name.lower())
    moves = []
    with open(datadir + file, "r") as fid:
        data = csv.reader(fid)
        header = next(data)
        header = header[0].split("\t")
        for move in data:
            moves.append(move[0].split("\t"))

    # Remove moves out of level:
    ind = []
    for im,move in enumerate(moves):
        cap_level = int(move[1])
        if (cap_level>level):
            ind.append(im)
    if len(ind)>0:
        ind = slice(min(ind), max(ind)+1)
        del moves[ind]

    # Remove repeated moves:
    ind = []
    for im in range(len(moves)):
        iname = moves[im][0]
        for jm in range(im+1,len(moves)):
            if jm in ind:
                continue
            jname = moves[jm][0]
            if (iname==jname):
                ind.append(max(im,jm))
    if len(ind)>0:
        ind = sorted(ind, reverse=True)
        for i in ind:
            del moves[i]
    nm = len(moves)
    
    # Create Movement objects and add them to the Pokemon object:
    if (nm>4):
        counter=4
        for im in range(nm-1,-1,-1):
            name, kk, typ, cat, pow, acc, pp = moves[im]
            move_tmp = Movement(name, typ, cat, int(pow), int(acc), int(pp))
            setattr(pokemon, "move_"+str(counter), move_tmp)
            counter-=1
            if (counter==0):
                break
    else:
        for im in range(nm-1,-1,-1):
            name, kk, typ, cat, pow, acc, pp = moves[im]
            move_tmp = Movement(name, typ, cat, int(pow), int(acc), int(pp))
            setattr(pokemon, "move_"+str(nm), move_tmp)
            nm-=1
            if (nm==0):
                break

    # Output:
    return pokemon


# Battle status:
def battle_status(pokemon1, pokemon2, h1, h2):
    """
    INPUT:
        pokemon1: Pokemon object representing the user's pokemon
        pokemon2: Pokemon object representing enemy pokemon
        h1: initial health points for pokemon1
        h2: initial health points for pokemon2
    """
    print("xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx")
    print("x  Rival:    {:<15}   Nivel={:<5}   PS={:>3}/{:<3} x".format(pokemon2.name, pokemon2.level, max(0,pokemon2.health), h2))
    print("x  Aliado:   {:<15}   Nivel={:<5}   PS={:>3}/{:<3} x".format(pokemon1.name, pokemon1.level, max(0,pokemon1.health), h1))
    print("xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx")
    input(), os.system("clear")

# Define simplified type table:
def type_table(attack_type, defense_type):

    # Load data from .csv file:
    with open("./Data/table_types.csv", "r") as fid:
        data = csv.reader(fid)
        types = next(data)[0].split("\t")
        rows = []
        for row in data:
            rows.append(row)
    values = []
    for row in rows:
        values.append(row[0].split("\t"))

    # Find type factor:
    if (attack_type in types) and (defense_type in types):
        t1 = types.index(attack_type)
        t2 = types.index(defense_type)
        factor = float(values[t1][t2])
    else:
        factor = 1.0
    return factor

# Define a function to simulate a turn during a battle:
def battle_turn(pokemon1, pokemon2, nmove1, nmove2, h1, h2, ally=1):
    """
    INPUT
        pokemon1(obj):    pokemon with priority this turn
        pokemon2(obj):    pokemon with no priority this turn  
        nmove1(int/bool): index of move1 within all the possible movements of pokemon1
        nmove2(int/bool): index of move2 within all the possible movements of pokemon2
        h1(int):          initial health points for pokemon1 (before combat started)
        h2(int):          initial health points for pokemon2 (before combat started)
        ally(int):        from pokemon1 or pokemon2, which is the ally?
    """

    # Show pokemon status:
    if (ally==1):
        battle_status(pokemon1, pokemon2, h1, h2)
    else:
        battle_status(pokemon2, pokemon1, h2, h1)

    # Define movements selected:
    if (isinstance(nmove1, bool) and nmove1==False):
        move1 = struggle
    else:
        move1 = getattr(pokemon1,"move_"+str(nmove1))
    if (isinstance(nmove2, bool) and nmove2==False):
        move2 = struggle
    else:
        move2 = getattr(pokemon2,"move_"+str(nmove2))

    # Fastest pokemon attacks:
    is_crit = pokemon2.is_attacked(pokemon1, nmove1)
    if (ally==1):
        input(" ??{} us?? {}! ".format(pokemon1.name, move1.name)); os.system("clear")
        battle_status(pokemon1, pokemon2, h1, h2)
    else:
        input(" ??Enemigo {} us?? {}! ".format(pokemon1.name, move1.name)); os.system("clear")
        battle_status(pokemon2, pokemon1, h2, h1)
    if (is_crit==True):
        input("??Ataque cr??tico!")
        os.system("clear")
    t1 = type_table(move1.type,pokemon2.type1)
    t2 = type_table(move1.type,pokemon2.type2)
    if   (t1*t2>1):
        input(" ??Es s??per efectivo!"), os.system("clear")
    elif (t1*t2<1):
        input(" No es muy efectivo..."), os.system("clear")
    if (pokemon2.status=="Fainted"):
        return

    # If STRUGGLE has been used by pokemon1:
    if (isinstance(nmove1, bool) and nmove1==False):
        if (ally==1):
            input(" ??{} tambi??n se ha hecho da??o!".format(pokemon1.name))
        else:
            input(" ??El {} enemigo tambi??n se ha hecho da??o!".format(pokemon1.name))
        os.system("clear")

    # If the defender survives, now it attacks:
    is_crit = pokemon1.is_attacked(pokemon2,nmove2)
    if (ally==2):
        input(" ??{} us?? {}! ".format(pokemon2.name, move2.name)); os.system("clear")
        battle_status(pokemon2, pokemon1, h2, h1)
    else:
        input(" ??Enemigo {} us?? {}! ".format(pokemon2.name, move2.name)); os.system("clear")
        battle_status(pokemon1, pokemon2, h1, h2)
    if (is_crit==True):
        input("??Ataque cr??tico!")
        os.system("clear")
    t1 = type_table(move2.type,pokemon1.type1)
    t2 = type_table(move2.type,pokemon1.type2)
    if   (t1*t2>1):
        input(" ??Es s??per efectivo!"); os.system("clear")
    elif (t1*t2<1):
        input(" No es muy efectivo..."); os.system("clear")
    if (pokemon1.status=="Fainted"):
        return

    # If STRUGGLE has been used by pokemon2:
    if (isinstance(nmove2, bool) and nmove2==False):
        if (ally==2):
            input(" ??{} tambi??n se ha hecho da??o!".format(pokemon2.name))
            
        else:
            input(" ?? El {} enemigo tambi??n se ha hecho da??o!".format(pokemon2.name))
        os.system("clear")

# Calculate final value for any stat but HP (assuming IV=EV=0):
def calculate_stat(base, level):
    stat = (base + 50)*level/50 + 5
    stat = int(stat)
    return stat
    
# Calculate final value for HP (assuming IV=EV=0):
def calculate_hp(base, level):
    hp = (base + 50)*level/50 + 10
    hp = int(hp)
    return hp

# Check if the pokemon has no PP for any of its movements:
def check_global_pp(pokemon):

    # Calculate total number of PP's:
    npp = 0
    for i in range(0,4):
        if hasattr(pokemon,"move_"+str(i)):
            npp += getattr(getattr(pokemon,"move_"+str(i)),"power_points")

    # Set value for no_global_pp (bool):
    if (npp==0):
        no_global_pp = True
    else:
        no_global_pp = False
    return no_global_pp

# Create movement: struggle
name = "Struggle"
typ = "Normal"
cat = "Physical"
pow = 50
acc = 100
pp = 1
struggle = Movement(name, typ, cat, pow, acc, pp)