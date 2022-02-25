import sqlite3
from pydfs_lineup_optimizer import get_optimizer, Site, Sport, ProgressiveFantasyPointsStrategy, RandomFantasyPointsStrategy, exceptions, Player

conn = sqlite3.connect('players.db')
c = conn.cursor()

c.execute("SELECT * FROM players")

players = c.fetchall()
file_text = "Position,Name + ID,Name,ID,Roster Position,Salary,Game Info,TeamAbbrev,AvgPointsPerGame,Max Deviation\n"
for player in players:
    if player[11] != None:
        file_text += f"{player[2]},{player[10]},{player[0]},{player[12]},{player[2]},{player[3]},{player[11]},{player[1]},{round(player[4],2)},{player[5]}\n"


with open("draft_from_file.csv","w") as f:
    f.write(file_text)


optimizer = get_optimizer(Site.DRAFTKINGS_CAPTAIN_MODE, Sport.BASKETBALL)
optimizer.load_players_from_csv("draft_from_file.csv")



lineups = list(optimizer.optimize(28,max_exposure=1))
optimizer.export("result.csv")

with open("result.csv",'r') as f:
    string = f.read()
    text_string = "Name,Own%\n"
    for player in players:
        if player[0] in string:
            actual_ownership = string.count(player[0])/ 28
            text_string += f"{player[0]},{actual_ownership}\n"

    with open("ownership.csv",'w') as q:
        q.write(text_string)
