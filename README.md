# Pokemon
*Pokemon 1st Generation Simple Battle Simulator.*

# Contents:
1. **main.py**: script to run the simulation

2. **mod_pokemon.py**: classes and functions used

3. **get_data.py**: script used to obtain all the data for the 1st Generation of Pokemon from Web Scrapping using BeautifulSoup package

4. **./Data/\*.csv**: files created by *get_data.py* to be read during the combat

5. **text_funcs.py**: several functions with text to be displayed during the combat

# How to run the simulator?
1. Run the *main.py* file with python3
2. Press ENTER to pass the dialogues
3. Report bugs and/or send your insults to *isidrolosada@gmail.com*

# Releases:
- Beta 1.0: 
    - Bug fixed when selecting allied pokemon movement with an empty input.
    - Improved selection of allied pokemon. The code has been generalized to implement more possible pokemons in the future (not implemented yet).
    - Balance adjustment: decreased level of Charmander (10-->8) to equilibrate the combat. Now it is more likely to win with Bulbasaur (depending on how lucky you are).
- Beta 1.1:
    - Bug fixed when entering 0 to select pokemon and movements during battle.
- Beta 1.2:
    - Bug fixed when any movement has no PP. Also, when there are no moves with PP, the pokemon is forced to use STRUGGLE.
- Beta 2.0:
    - Included a script *get_data.py* to obtain, using Web Scraping, all the data related with the Generation I of Pokemon. Every action is detailed so it can be understood easily. I am not an expert in Web Scraping so I am sure that things could have been done more efficiently.
    - Related with the previous point, the folder *./Data/* has been added with several .csv files as data base.
    - The selection of pokemons at the start of the combat has been changed. Now, the player can choose from the whole pool of pokemons in Generation I. The pokemon of the enemy is selected randomly from the whole pool. The level stat of each pokemon is chosen depending on their types in order to balance the game. The stats of both pokemons are displayed at the beggining of the combat.
    - Created *text_funcs.py* with most of the texts that appear in the combat just to improve readability of *main.py*.
