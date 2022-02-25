import sqlite3

players = {}
with open("NBA DK Boom Bust.csv") as f:
    lines = f.readlines()
    for line in lines:
        parts = line.split(",")
        players[parts[0].replace('"',"")] = {
            "name":parts[0].replace('"',""),
            "team":parts[1].replace('"',""),
            "position":parts[2].replace('"',""),
            "salary":parts[3].replace('"',"") + parts[4].replace('"',""),
            "projection":parts[5].replace('"',""),
            "stdev":parts[6].replace('"',""),
            "ceiling":parts[7].replace('"',""),
            "floor":parts[8].replace('"',""),
            "bust":parts[9].replace('"',""),
            "boom":parts[10].replace('"',"")

        }


conn = sqlite3.connect('players.db')
c = conn.cursor()
c.execute("""CREATE TABLE players(
             name text,
             team text,
             position text,
             salary integer,
             projection real,
             stdev real,
             ceiling real,
             floor real,
             bust real,
             boom real
)""")


for player in players:
    try:
        c.execute("INSERT INTO players VALUES (?,?,?,?,?,?,?,?,?,?)",(players[player]['name'],players[player]['team'],'UTIL',int(players[player]['salary']),float(players[player]['projection']),float(players[player]['stdev']),float(players[player]['ceiling'])
             ,float(players[player]['floor']),float(players[player]['bust']),float(players[player]['boom'])))
        c.execute("INSERT INTO players VALUES (?,?,?,?,?,?,?,?,?,?)",(players[player]['name'],players[player]['team'],'CPT',int(players[player]['salary']) * 1.5,float(players[player]['projection']) * 1.5,float(players[player]['stdev']),float(players[player]['ceiling'])
             ,float(players[player]['floor']),float(players[player]['bust']),float(players[player]['boom'])))
    except ValueError:
        pass

conn.commit()

c.execute("ALTER TABLE players ADD COLUMN name_id text")
c.execute("ALTER TABLE players ADD COLUMN game_info text")
c.execute("ALTER TABLE players ADD COLUMN id integer")

with open("DKSalaries.csv") as f:
    lines = f.readlines()
    for line in lines:
        parts = line.split(",")
        c.execute("UPDATE players SET name_id=?,game_info=?,id=?,salary=? WHERE name=?",(parts[1],parts[6],parts[3],parts[5],parts[2]))
        conn.commit()
