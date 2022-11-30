### Pokemon combat simulator
import os
import random
import numpy as np
from text_funcs import *
from mod_pokemon import Pokemon, Movement, create_pokemon, create_pokemon_rand, battle_turn, type_table, battle_status, check_global_pp

# Introduction:
text_intro()

# Ally Pokemon selection:
lvl1 = random.randint(1,100)
print(" ¿Qué pokemon prefieres?")
pokemon1 = None
while (pokemon1==None):
    selection = input("\n>> Introduce el nombre de tu selección: ")
    pokemon1 = create_pokemon(selection, lvl1)

# Enemy pokemon selection:
pokemon2 = create_pokemon_rand(lvl1)

# Store in variables initial health points to be used in battle_status():
h1 = pokemon1.health
h2 = pokemon2.health

# Print results of selection:
os.system("clear")
print(" ¡Perfecto! Has escogido luchar con {}. Tu rival será {}.".format(pokemon1.name, pokemon2.name))
input(); os.system("clear")
t11 = type_table(pokemon1.type1,pokemon2.type1)
t12 = type_table(pokemon1.type1,pokemon2.type2)
t21 = type_table(pokemon1.type2,pokemon2.type1)
t22 = type_table(pokemon1.type2,pokemon2.type2)
if   (t11*t12*t21*t22>1):
    print(" Parece que te ha tocado un combate facilito... ¡Menuda suerte!")
    input(), os.system("clear")
    pokemon2.level = min(int(1.2*pokemon2.level),100)
elif (t11*t12*t21*t22<1):
    print(" Oh, parece que te ha tocado un combate complicado... jajaja ¡Menudo pringao!")
    input(), os.system("clear")
    pokemon2.level = max(int(0.8*pokemon2.level),1)
else:
    print(" Parece que se trata de un combate igualado... ¡Veamos de qué eres capaz!")
    input(), os.system("clear")

# Display stats for both pokemons:
print(">> Estadísticas del {} aliado:".format(pokemon1.name))
pokemon1.all_attrs()
print(">> Estadísticas del {} enemigo:".format(pokemon2.name))
pokemon2.all_attrs()
input(" "); os.system("clear")

# Start of the combat:
text_start_combat(pokemon1, pokemon2, h2)

# Development of the combat:
nturns = 0
while (pokemon1.status=="Healthy") and (pokemon2.status=="Healthy"):

    # Show battle status at the begining of the turn:
    battle_status(pokemon1, pokemon2, h1, h2)

    # Check if there are PP's to combat: if not, use default 
    no_global_pp_1 = check_global_pp(pokemon1)
    if (no_global_pp_1==True):
        nmove1 = False
        input(" ¡A {} no le quedan más movimientos!".format(pokemon1.name))
        os.system("clear")
    else:
        # Player selects next movement:
        n=0
        print(" Selecciona uno de los siguientes movimientos de {} introduciendo el número correspondiente:".format(pokemon1.name))
        for i in range(0,4):
            if hasattr(pokemon1,"move_"+str(i+1)):
                n=i+1
                print("   ({:<1}) {:<15} [Tipo: {:<10} PP: {:<2}]".format(i+1, getattr(getattr(pokemon1,"move_"+str(i+1)),"name"), 
                                                                            getattr(getattr(pokemon1,"move_"+str(i+1)),"type"),
                                                                            getattr(getattr(pokemon1,"move_"+str(i+1)),"power_points")))
        right_selection = False
        while (right_selection==False):
            nmove1 = input("\n>> Selección: ")
            if (nmove1.isnumeric() and int(nmove1)>0 and int(nmove1)<=n):
                if getattr(getattr(pokemon1,"move_"+nmove1),"power_points")>0:
                    right_selection = True
                else:            
                    print("\n ===> Te has quedado sin PP para este movimiento, ¡tienes que escoger otro!")
            else:
                print("\n ===> ¿Ya estás trolleando otra vez? Selección inválida, introduce el número entero asociado al ataque que prefieras.")
        nmove1 = int(nmove1)
        os.system("clear")

    # Enemy selects next movement (randomly):
    no_global_pp_2 = check_global_pp(pokemon2)
    if (no_global_pp_2==True):
        nmove2 = False
    else:
        ind = []
        for i in range(0,4):
            if ( hasattr(pokemon2,"move_"+str(i+1)) and getattr(getattr(pokemon2,"move_"+str(i+1)),"power_points")>0 ):
                ind.append(str(i+1))
        nmove2 = int(random.choice(ind))

    # Perform battle turn:
    if   (pokemon1.speed>pokemon2.speed) or (pokemon1.speed==pokemon2.speed):  # if speed values matches, user always wins
        battle_turn(pokemon1, pokemon2, nmove1, nmove2, h1, h2, ally=1)
    elif (pokemon1.speed<pokemon2.speed):
        battle_turn(pokemon2, pokemon1, nmove2, nmove1, h2, h1, ally=2)

    # End of the turn and start again if both Pokemon are healthy:
    nturns += 1

# End of the combat:
if   (pokemon1.status=="Fainted"):
    text_defeat(pokemon1)    
elif (pokemon2.status=="Fainted"):
    text_victory(pokemon2)
