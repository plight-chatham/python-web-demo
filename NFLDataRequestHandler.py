import sqlite3
from http.server import BaseHTTPRequestHandler
from NFLPlayerClasses import Player

class NFLDataRequestHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        if self.path.lower().startswith( "/players" ):
            self.do_player_detail()
        else:
            self.do_main_index()


    def do_main_index(self):
        with open('templates/PlayerIndex.html') as index_file:
            template = index_file.read()

        players = self.fetch_player_list()
        player_list_html = ""
        for player in players:
            player_list_html += "<li>"
            player_list_html += f"<a href='/players/{player.nflId}'>{player.name}</a>"
            player_list_html += "</li>\n"

        response = template.replace("{{player_list_items}}", player_list_html)
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(response.encode('utf-8'))


    def do_player_detail(self):
        id = self.path.split("/")[-1]
        player = self.fetch_player_detail(id)
        plays = self.fetch_plays_with_player(id)
        with open('templates/PlayerDetail.html') as index_file:
            template = index_file.read()

        response = template.replace("{{player_name}}", player.name)
        response = response.replace("{{position}}", player.position)

        plays_html = ""
        for play in plays:
            plays_html += f"<li>"
            plays_html += f"{play[1]}"
            plays_html += "</li>\n"
        response = response.replace("{{plays}}", plays_html)

        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(response.encode('utf-8'))


    def fetch_player_list(self):
        conn = sqlite3.connect("data/nfl-players-plays.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM players")
        contents = cursor.fetchall()
        result = []
        for row in contents:
            result.append(Player(row))
        return result


    def fetch_plays_with_player(self, nflId):
        conn = sqlite3.connect("data/nfl-players-plays.db")
        cursor = conn.cursor()
        cursor.execute(f"""
            select displayName, playDescription 
            from plays as p
            join players_plays as pp on pp.gameId = p.gameId and p.playId = pp.playId
            join players as pl on pp.nflId = pl.nflId
            where pl.nflId = {nflId}""")
        contents = cursor.fetchall()
        result = []
        for row in contents:
            result.append(row)
        return result


    def fetch_player_detail(self, nflId):
        conn = sqlite3.connect("data/nfl-players-plays.db")
        cursor = conn.cursor()
        cursor.execute(f"SELECT * FROM players where nflId = {nflId}")
        contents = cursor.fetchall()
        return Player(contents[0])
