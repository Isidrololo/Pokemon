# Pokemon
*Pokemon 1st Generation simple battle simulator.*

# Contents:
1. **main.py**: script to run the simulation

2. **data.py**: script with the data from bulbapedia.com

3. **mod_pokemon.py**: objects and functions used

# How to run the simulator?
1. Run the file *main.py* with python3
2. Press enter to pass the dialogues
3. Report bugs and/or send your insults to isidrolosada@gmail.com

# Releases:
- Beta 1.0: 
    - Bug fixed when selecting allied pokemon movement with an empty input.
    - Improved selection of allied pokemon. The code has been generalized to implement more possible pokemons in the future (not implemented yet).
    - Balance adjustment: decreased level of Charmander (10-->8) to equilibrate the combat. Now it is more likely to win with Bulbasaur (depending on how lucky you are).
- Beta 1.1:
    - Bug fixed when entering 0 to select pokemon and movements during battle.
- Beta 1.2:
    - Bug fixed when any movement has no PP. Also, when there are no moves with PP, the pokemon is forced to use STRUGGLE.
