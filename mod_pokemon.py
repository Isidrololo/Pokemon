# Write class to create pokemons:
import os
import random
import numpy as np

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
def battle_turn(pokemon1, pokemon2, move1, move2, nmove1, nmove2, h1, h2, ally=1):
    """
    INPUT
        pokemon1(obj): pokemon with priority this turn
        pokemon2(obj): pokemon with no priority this turn
        move1(obj):    movement selected for pokemon1
        move2(obj):    movement selected for pokemon2    
        nmove1(int):   index of move1 within all the possible movements of pokemon1
        nmove2(int):   index of move2 within all the possible movements of pokemon2
        h1(int):       initial health points for pokemon1 (before combat started)
        h2(int):       initial health points for pokemon2 (before combat started)
        ally(int):     from pokemon1 or pokemon2, which is the ally?
    """

    # Show pokemon status:
    if (ally==1):
        battle_status(pokemon1, pokemon2, h1, h2)
    else:
        battle_status(pokemon2, pokemon1, h2, h1)

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

#****************************************************************************
#****************************************************************************
#****************************************************************************
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
    def is_attacked(self, attacker: object, nmove: int):
        # Get attacker movement attributes:
        move = getattr(attacker,"move_"+str(nmove))
        pow = move.power

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