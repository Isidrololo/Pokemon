### Pokemon combat simulator
import os
import random
import numpy as np
from data import *
from mod_pokemon import Pokemon, Movement, battle_turn, type_table, battle_status

# Introduction:
os.system("clear")
print(" ¡Hola, entrenador! Bienvenido al simulador de combates Pokémon de la Primera Generación.")
input(), os.system("clear")
print(" Antes de comenzar, deberás elegir un pokémon.")
input(), os.system("clear")
print(" Me temo que solo tienes dos opciones pero, ¡no empieces a quejarte ya!")
input(), os.system("clear")
print(" ¿Has hecho tú algo? ¿No? Pues te callas, crack.")
input(), os.system("clear")
print(" Como iba diciendo, tienes únicamente dos opciones para elegir.")
input(), os.system("clear")
print(" Elige sabiamente, pues determinará el devenir de tu épica aventura.")
input(), os.system("clear")

# Pokemon selection:
print(" ¿Qué pokemon prefieres:")
npok = len(pokemon_list)  # number of pokemon availiable
ipok = np.arange(npok)    
pokemon_list_lower = [x.lower() for x in pokemon_list]
for ip, pname in enumerate(pokemon_list):
    obj = eval(pname.lower())
    print("     ({:<1}) {:<15}   Nivel={:<5}".format(ip+1, pname, obj.level))
selected = False
while (selected==False):
    selection = input("\n>> Selección: ")
    if  (not selection.isnumeric()) and (selection.lower()=="charmander" or selection.lower()=="bulbasaur"):
        other = pokemon_list_lower[:]
        other.remove(selection.lower())
        if len(other)==1:
            pokemon1 = eval(selection.lower())
            pokemon2 = eval(other[0].lower())
            selected = True
        else:
            raise Exception("ERROR: code is note ready for more than 2 pokemon in the data base!")
    elif (selection.isnumeric() and int(selection)<=npok):
        selection = int(selection)-1
        mask = (ipok==selection)
        other = ipok[~mask]
        if len(other)==1:
            pokemon1 = eval(pokemon_list_lower[selection])
            pokemon2 = eval(pokemon_list_lower[other[0]])
        else:
            raise Exception("ERROR: code is not ready for more than 2 pokemon in the data base!")
        selected = True
    else:
        print("\n ===> Esa opción no es valida, prueba otra vez. Venga, que no puede ser tan difícil...")

# Store in variables initial health points to be used in battle_status():
h1 = pokemon1.health
h2 = pokemon2.health

# Print results of selection:
os.system("clear")
print(" ¡Perfecto! Has escogido luchar con {}. Tu rival luchará con {}.".format(pokemon1.name, pokemon2.name))
input(); os.system("clear")
t11 = int(type_table(pokemon1.type1,pokemon2.type1))
t12 = int(type_table(pokemon1.type1,pokemon2.type2))
t21 = int(type_table(pokemon1.type2,pokemon2.type1))
t22 = int(type_table(pokemon1.type2,pokemon2.type2))
if t11==2 or t12==2 or t21==2 or t22==2:
    os.system("clear")
    print(" Uy, parece que has elegido un combate facilito... ¡Menudo espabilao!")
    input(), os.system("clear")
else:
    os.system("clear")
    print(" Oh, parece que has elegido un combate complicado... Te gustan los retos, ¿eh? ¡Flipao! Jeje.")
    input(), os.system("clear")

# Start of the combat:
print(" ¡Comencemos con el combate, pues! El entrenador rival sorpresa al que te enfrentarás es...")
input(), os.system("clear")
print(" Chan chan chaaaaan...")
input(), os.system("clear")
print(" ¡Elon Musk! Parece que el megalómano más de moda del momento quiere enfrentarse a ti para decidir el destino de nuestra amada plataforma Twitter.")
input(), os.system("clear")
print(" ¡Oh, Dios! El destino de Twitter está en tus manos. ¿Serás capaz de desbaratar sus maléficos planes? ¿O tal vez salvar Twitter no es la mejor de las ideas?")
input(), os.system("clear")
print(" Sea como fuere, ¡QUE DE COMIENZO EL COMBATE!")
input(), os.system("clear")
print(" Tiririririririri, tin tin tin tintin tin!")
input(), os.system("clear")
print(" ¡Imbécil Elon Musk quiere luchar!")
input(), os.system("clear")
print(" ¡Imbécil Elon Musk envió a {}!".format(pokemon2.name))
input(), os.system("clear")
print("xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx")
print("x  Rival:    {:<15}   Nivel={:<5}   PS={:>3}/{:<3} x".format(pokemon2.name, pokemon2.level, pokemon2.health, h2))
input(), os.system("clear")
print(" ¡Ve {}!".format(pokemon1.name))
input(), os.system("clear")

# Development of the combat:
nturns = 0
while (pokemon1.status=="Healthy") and (pokemon2.status=="Healthy"):

    # Show battle status at the begining of the turn:
    battle_status(pokemon1, pokemon2, h1, h2)

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
        try:
            if (int(nmove1)<=n):
                right_selection = True
                break
            else:
                print("\n ===> ¿Ya estás trolleando otra vez? Selección inválida, introduce el número entero asociado al ataque que prefieras.")
        except:
            print("\n ===> ¿Ya estás trolleando otra vez? Selección inválida, introduce el número entero asociado al ataque que prefieras.")
    move1 = getattr(pokemon1,"move_"+str(nmove1))
    os.system("clear")

    # Enemy selects next movement (randomly):
    n=0
    for i in range(0,4):
        if hasattr(pokemon2,"move_"+str(i+1)):
            n=i+1
    nmove2 = random.randint(1,n)   
    move2 = getattr(pokemon2,"move_"+str(nmove2))

    # Perform battle turn:
    if   (pokemon1.speed>pokemon2.speed) or (pokemon1.speed==pokemon2.speed):  # if speed values matches, user always wins
        battle_turn(pokemon1, pokemon2, move1, move2, nmove1, nmove2, h1, h2, ally=1)
    elif (pokemon1.speed<pokemon2.speed):
        battle_turn(pokemon2, pokemon1, move2, move1, nmove2, nmove1, h2, h1, ally=2)

    # End of the turn and start again if both Pokemon are healthy:
    nturns += 1

# End of the combat:
if   (pokemon1.status=="Fainted"):
    print(" ¡{} aliado se desmayó!".format(pokemon1.name))
    input(), os.system("clear")
    print(" ¡Imbécil Elon Musk te ha vencido!")
    input(), os.system("clear")
    print("Imbécil Elon Musk: MUAHAHAHAHA, ¡¡TWITTER ES MÍA!!")
    input(), os.system("clear")
    print("Imbécil Elon Musk: Se acabaron las cancelaciones, se acabaron las feministas, se acabaron los PROGRES.")
    input(), os.system("clear")
    print("Imbécil Elon Musk: Por fin podré tranformar Twitter en...")
    input(), os.system("clear")
    print("Imbécil Elon Musk: ¡¡¡¡¡FOROCOCHES!!!!!")
    input(), os.system("clear")
    print("Imbécil Elon Musk: Ese era mi objetivo desde el principio. ")
    input(), os.system("clear")
    print("Imbécil Elon Musk: Ahora por fin todos comprenderán que hay más buenas personas en Forocoches que en Twitter.")
    input(), os.system("clear")
    print("Imbécil Elon Musk: Y si no lo comprenden, su cuenta será borrada para siempre.")
    input(), os.system("clear")
    print("Imbécil Elon Musk: Twitter será un lugar puro al fin...")
    input(), os.system("clear")
    print("Imbécil Elon Musk: *Se sube en una carroza tirada por empleados de Twitter, completamente amordazados, y se marcha entre latigazos.*")
    input(), os.system("clear")
elif (pokemon2.status=="Fainted"):
    print(" ¡{} enemigo se desmayó!".format(pokemon2.name))
    input(), os.system("clear")
    print(" ¡Has vencido a Imbécil Elon Musk!")
    input(), os.system("clear")
    print(" Elon Musk: ¡¡¡¡NOOOO!!!! No puede ser...")
    input(), os.system("clear")
    print(" Elon Musk: Mi imperio de incels... Cancelado...")
    input(), os.system("clear")
    print(" Elon Musk: ¡Las feminisitas y los progres arruinarán esta red social!")
    input(), os.system("clear")
    print(" Elon Musk: ¿Es que no lo véis? No entiendo cómo no me hacéis caso con lo listo y guay que soy... ")
    input(), os.system("clear")
    print(" Elon Musk: Mentes inferiores... Soy demasiado superior a vosotros... ")
    input(), os.system("clear")
    print(" Elon Musk: Al menos, siempre me quedará Forocoches, libre de mujeres (que me dan miedo) y de rojos (que me dan asco)...")
    input(), os.system("clear")
    print(" Elon Musk: *Se sube en su cohete espacial privado, mientras se enciente un puro con un billete de 1000$ y se marcha fuera de órbita.*")
    input(), os.system("clear")