# Write class to create pokemons:
import os
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

    # Type factor equals unity when any of the types is empty:
    if (not attack_type) or (not defense_type):
        T = 1
        return T

    # Define general order of Pokemon types:
    type_order = ["Normal", "Fire", "Water", "Grass", "Poison"]

    # Define type chart with a matrix:
    M = np.matrix([ [1,1,1,1,1], [1,0.5,0.5,2,1], [1,2,0.5,0.5,1], [1,0.5,2,0.5,0.5], [1,1,1,2,0.5] ])

    # Find the appropriate matrix element:
    try:
        iT = type_order.index(attack_type)
        jT = type_order.index(defense_type)
    except:
        raise Exception("ERROR: Unknown attack/defense type!")

    # Output corresponding type multiplier:
    T = M[iT,jT]
    return T

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
        input(" ¡{} usó {}! ".format(pokemon1.name, move1.name)); os.system("clear")
        battle_status(pokemon1, pokemon2, h1, h2)
    else:
        input(" ¡Enemigo {} usó {}! ".format(pokemon1.name, move1.name)); os.system("clear")
        battle_status(pokemon2, pokemon1, h2, h1)
    if (is_crit==True):
        input("¡Ataque crítico!")
        os.system("clear")
    t1 = type_table(move1.type,pokemon2.type1)
    t2 = type_table(move1.type,pokemon2.type2)
    if   (t1*t2>1):
        input(" ¡Es súper efectivo!"), os.system("clear")
    elif (t1*t2<1):
        input(" No es muy efectivo..."), os.system("clear")
    if (pokemon2.status=="Fainted"):
        return

    # If STRUGGLE has been used by pokemon1:
    if (isinstance(nmove1, bool) and nmove1==False):
        if (ally==1):
            input(" ¡{} también se ha hecho daño!".format(pokemon1.name))
        else:
            input(" ¡El {} enemigo también se ha hecho daño!".format(pokemon1.name))
        os.system("clear")

    # If the defender survives, now it attacks:
    is_crit = pokemon1.is_attacked(pokemon2,nmove2)
    if (ally==2):
        input(" ¡{} usó {}! ".format(pokemon2.name, move2.name)); os.system("clear")
        battle_status(pokemon2, pokemon1, h2, h1)
    else:
        input(" ¡Enemigo {} usó {}! ".format(pokemon2.name, move2.name)); os.system("clear")
        battle_status(pokemon1, pokemon2, h1, h2)
    if (is_crit==True):
        input("¡Ataque crítico!")
        os.system("clear")
    t1 = type_table(move2.type,pokemon1.type1)
    t2 = type_table(move2.type,pokemon1.type2)
    if   (t1*t2>1):
        input(" ¡Es súper efectivo!"); os.system("clear")
    elif (t1*t2<1):
        input(" No es muy efectivo..."); os.system("clear")
    if (pokemon1.status=="Fainted"):
        return

    # If STRUGGLE has been used by pokemon2:
    if (isinstance(nmove2, bool) and nmove2==False):
        if (ally==2):
            input(" ¡{} también se ha hecho daño!".format(pokemon2.name))
            
        else:
            input(" ¡ El {} enemigo también se ha hecho daño!".format(pokemon2.name))
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