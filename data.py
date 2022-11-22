from mod_pokemon import Pokemon, Movement

# Store names of pokemons available in this data base:
pokemon_list = ["Charmander", "Bulbasaur"]

# Define base stats for Charmander:
name = "Charmander"
t1  = "Fire"
t2  = []
hp  = 39
at  = 52
df  = 43
sat = 60
sdf = 50
spd = 65
lvl = 8

# Create Charmander:
charmander = Pokemon(name, t1, t2, hp, at, df, sat, sdf, spd, lvl)

# Define base stats for Bulbasaur:
name = "Bulbasaur"
t1  = "Grass"
t2  = "Poison"
hp  = 45
at  = 49
df  = 49
sat = 65
sdf = 65
spd = 45 
lvl = 10

# Create Bulbasaur:
bulbasaur = Pokemon(name, t1, t2, hp, at, df, sat, sdf, spd, lvl)


#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++


# Create movement: scratch
name = "Scratch"
typ = "Normal"
cat = "Physical"
pow = 40
acc = 100
pp = 35
scratch = Movement(name, typ, cat, pow, acc, pp)

# Create movement: ember
name = "Ember"
typ = "Fire"
cat = "Special"
pow = 40
acc = 100
pp = 25
ember = Movement(name, typ, cat, pow, acc, pp)

# Create movement: tackle
name = "Tackle"
typ = "Normal"
cat = "Physical"
pow = 40
acc = 100
pp = 35
tackle = Movement(name, typ, cat, pow, acc, pp)

# Create movement: vine whip
name = "Vine Whip"
typ = "Grass"
cat = "Physical"
pow = 45
acc = 100
pp = 25
vine_whip = Movement(name, typ, cat, pow, acc, pp)


#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++


# Add appropriate movements to charmander:
charmander.add_move(scratch)
charmander.add_move(ember)

# Add appropriate movements to bulbasaur:
bulbasaur.add_move(tackle)
bulbasaur.add_move(vine_whip)