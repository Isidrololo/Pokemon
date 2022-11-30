# If you run this script, the following .csv files will be generated in ./Data/:
#                   data.csv: base stats for each pokemon belonging Generation I
#   [ID]_[pokemon]_moves.csv: stats of every move for each pokemon in Generation I
#            table_types.csv: types char in Generation I with 15 different types 
#
# Execution time expected: ~6 min

from bs4 import BeautifulSoup
import numpy  as np
import pandas as pd
import requests
import re
import time

# Start timer:
start = time.time()

# Set directory for the output files:
outdir = "./Data/"

# Download HTML code to generate BeautifulSup object:
url = "https://bulbapedia.bulbagarden.net/"
pageurl = url + "wiki/List_of_Pokémon_by_National_Pokédex_number" 
response = requests.get(pageurl).text
soup = BeautifulSoup(response, "html.parser")
# print(soup.prettify())  # DEBUG: display HTML file with appropriate indentation

# Find tables for each pokemon generation:
tables = soup.find_all("table", class_="roundy")

# Find names and links for each pokemon in Generation I:
pok_names = []
pok_links = []
infos = tables[0].find_all("a", title=re.compile("Pok"), href=re.compile("Pok"))
for ind,info in enumerate(infos):
    pok_names.append(info.get("title").replace(" (Pokémon)", ""))
    pok_links.append(info.get("href"))
    # print("{:>2}. {:<20} {:<}".format(ind+1, pok_names[-1], pok_links[-1]))  # DEBUG: display name/link for each pokemon

# Remove repeated entries: when creating a dictionary, Python automatically removes the repeated entries
pok_names = list(dict.fromkeys(pok_names))
pok_links = list(dict.fromkeys(pok_links))

# Fix url's for each pokemon:
npok = len(pok_names)
pok_links = [url + pok_links[i] for i in range(npok)]

# Create a dictionary with names and links:
if (npok!=151):  # DEBUG
    raise Exception("ERROR: number of pokemons in Generation I different from 151!")
pok_info = {pok_names[i]: pok_links[i] for i in range(len(pok_names))}

# Create a loop to find base stats for each pokemon:
pok_stats = []
pok_moves = [list() for i in range(npok)]
for i in range(npok):

    # Display progress:
    print("{:>1}. {:<20}".format(i+1, pok_names[i]))

    # Get HTML code:
    req = requests.get(pok_links[i]).text
    soup = BeautifulSoup(req, "html.parser")

    # Find names and values for base stats:
    tag_name = soup.find_all("div", style="float:left")
    tag_vals = soup.find_all("div", style="float:right")
    stats_name = [tag_name[j].span.string for j in range(6)]
    stats_vals = [tag_vals[j].string      for j in range(6)]

    # Find types:
    tag_type = soup.find_all("table", class_="roundy")
    tag_type = tag_type[0].find_all("a", title=re.compile("(type)"))
    type1 = tag_type[0].b.string
    type2 = tag_type[1].b.string
    if (type2.lower()=="unknown"):
        type2 = []

    # Store base stats:
    tmp = {"ID": i+1, "Name": pok_names[i]}
    nstats = len(stats_name)
    for ist,stat in enumerate(stats_name):
        tmp.update( {stats_name[ist]: stats_vals[ist]} )
    tmp.update( {"type1": type1} )
    tmp.update( {"type2": type2} )
    pok_stats.append(tmp)

    # Find Generation I learnset in other web site: added exceptions for Nidoran, Mr. Mime and Farfectch'd url's since they are problematic
    if   (pok_names[i].lower()=="nidoran♀"):
        link = "https://pokemondb.net/pokedex/nidoran-f/moves/1/"
    elif (pok_names[i].lower()=="nidoran♂"):
        link = "https://pokemondb.net/pokedex/nidoran-m/moves/1/"
    elif (pok_names[i].lower()=="farfetch'd"):
        link = "https://pokemondb.net/pokedex/farfetchd/moves/1/"
    elif (pok_names[i].lower()=="mr. mime"):
        link = "https://pokemondb.net/pokedex/mr-mime/moves/1/"
    else:
        link = "https://pokemondb.net/pokedex/" + pok_names[i].lower() + "/moves/1/"
    req = requests.get(link).text
    soup = BeautifulSoup(req, "html.parser")
    trs = soup.find("table", class_="data-table").tbody.children

    # Loop over moves:
    for it,tr in enumerate(trs):
        # print("{}. {}".format(it+1, tr.a.string))  # DEBUG
        tds = list(tr.children)
        lvl = int(tds[0].string)
        nam = tds[1].a.string
        typ = tds[2].a.string
        cat = tds[3].img.get("title")
        pow = tds[5].string
        if (pow=="—"):  # get rid off moves with pow=0
            continue
        pow = int(pow)
        if (tds[7].string=="∞"):  # exception for "swift" (rapidez)
            acc = 100
        else:
            acc = int(tds[7].string)

        # Obtain PP from a deeper url:
        if (" ") in nam:
            name_mod = nam.lower().replace(" ", "-")
        else:
            name_mod = nam.lower()
        url_pp = "https://pokemondb.net/move/" + name_mod
        req_pp = requests.get(url_pp).text
        soup_pp = BeautifulSoup(req_pp, "html.parser")
        table_pp = soup_pp.find("table", class_="vitals-table")
        trs_pp = list(table_pp.tbody.children)
        pp = int(trs_pp[4].find("td").contents[0])

        # Add move stats to the global list:
        pok_moves[i].append( {"Name": nam, "level": lvl, "Type": typ, "Category": cat, "Power": pow, "Accuracy": acc, "PP": pp} )

# Create a DataFrame with all the info and export it as a .csv file:
pok_df = pd.DataFrame(pok_stats)
pok_df.to_csv(outdir + "data.csv", index=False, encoding="utf-8", sep="\t")
print(">> Output file created: {}".format(outdir + "data.csv"))

# Store movements in independet files for each pokemon:
for ip in range(npok):
    pok = pok_names[ip]
    outfile = outdir + str(ip+1).zfill(3) + "_" + pok.lower() + "_moves.csv"
    pok_df = pd.DataFrame(pok_moves[ip])
    pok_df.to_csv(outfile, index=False, encoding="utf-8", sep="\t")
    print(">> Moves data saved in: {}".format(outfile))

# Dowload type chart for Generation I:
outfile = outdir + "table_types.csv"
url = "https://pokemondb.net/type/old"
response = requests.get(url).text
soup = BeautifulSoup(response, "html.parser")

# Find data table corresponding to Generation I:
tables = soup.find_all("table", class_="type-table")
table = tables[1]
trs = table.tbody.find_all("tr")

# Get name types:
nt = len(trs)
types = []
matrix = np.inf*np.ones([nt,nt])
for itr,tr in enumerate(trs):
    types.append(tr.th.a.string)
    tds = tr.find_all("td")
    for itd,td in enumerate(tds):
        if   (td.string==None):
            matrix[itr,itd] = 1
        elif (td.string=="½"):  # I did not find any other way to solve this issue...
            matrix[itr,itd] = 0.5
        else:
            matrix[itr,itd] = float(td.string)
        
# Create DataFrame with type chart and save it in .csv format:
table_types = pd.DataFrame(matrix, columns=types)
table_types.to_csv(outfile, index=False, encoding="utf-8", sep="\t")
print(">> Output file created: {}".format(outfile))

# Display total time spent:
final = time.time()
dt = final-start
print("---------------------------------")
print(" Exec Time: {:.2f}h, {:.2f}min, {}s".format(dt/3600, dt/60, round(dt)))
print("---------------------------------")