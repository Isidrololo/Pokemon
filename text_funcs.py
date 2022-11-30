# File to call different functions to display text during the simulation.
import os

# Introduction dialogue:
def text_intro():
    os.system("clear")
    print(" ¡Hola, entrenador! Bienvenido al simulador de combates Pokémon de la Primera Generación.")
    input(), os.system("clear")
    print(" Antes de comenzar, deberás elegir un pokémon.")
    input(), os.system("clear")
    print(" Puedes elegir el que quieras, solo tienes que escribir su nombre.")
    input(), os.system("clear")
    print(" Menuda maravilla, ¿verdad? ¿Quién habrá hecho esto?")
    input(), os.system("clear")
    print(" Bueno, a lo que íbamos, elige sabiamente, pues determinará el devenir de esta épica aventura.")
    input(), os.system("clear")

# Start of the combat dialogue:
def text_start_combat(pokemon1, pokemon2, h2):
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

# End of the combat: DEFEAT
def text_defeat(pokemon1):
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

# End of the combat: VICTORY
def text_victory(pokemon2):
    print(" ¡El {} enemigo se desmayó!".format(pokemon2.name))
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
    print(" Elon Musk: *Se sube en su cohete espacial privado, mientras se enciente un puro con un billete de 1000$ y se marcha fuera de órbita*")
    input(), os.system("clear")