from flask import Flask, jsonify, request
from flask_cors import CORS
from pprint import pprint

from domain.classes import *
from resoruces.funcs import *

PORT = 5505

app = Flask(__name__)
CORS(app)

deck = Deck()
game = Game(deck)

# GET
@app.route("/", methods=["GET"])
def ping():
    '''
    Bienvenida
    '''
    return "SKYJO API REST"

@app.route("/players", methods=["GET"])
def player_list():
    '''
    Devuelve la lista de jugadores
    '''
    data = []
    for player in game.get_players():
        data.append(player.get_data())
    return jsonify({"players" : data})

@app.route("/checkturn", methods=["GET"])
def check_turn():
    '''
    Devuelve el nombre del jugador que tiene el turno
    '''
    name = game.get_next_turn().get_name()

    return jsonify({"turn" : name})


# POST
@app.route("/logging", methods=["POST"])
def logging_player():
    '''
    Un jugador inicia sesión
    '''
    data = request.get_json()
    pprint(data)
    player = Player(data["name"], data["password"])

    if game.game_status():
        return jsonify({"error" : "impossible logging"})

    if check_logging(data):
        if game.add_player(player):
            return jsonify(player.get_data())

        elif game.get_player(player):
            return jsonify(player.get_data())

        else:
            return jsonify({"error" : "impossible logging"})

    else:
        return jsonify({"error" : "incorrect data"})

@app.route("/start", methods=["POST"])
def start_game():
    '''
    Un jugador vota empezar la partida
    '''
    data = request.get_json()
    players = game.get_players()

    for player in players:
        user = player.get_data()
        if data["vote"]:
            if user["name"] == data["name"] and user["password"] == data["password"]:
                player.vote()
        else:
            break
    
    if game.votes() == len(players) and not game.game_status():
        game.start_game()
        deck.distribute(players)
    
    return jsonify({"votes" : f"{game.votes()}/{len(players)}"})

@app.route("/decks", methods=["POST"])
def get_decks():
    '''
    Devuelve los diferentes tableros de jugador
    '''
    data = request.get_json()
    other_mazes = {}
    for player in game.get_players():
        maze = []
        ind = 0
        for card in player.get_maze():
            if player.get_revealed()[ind]:
                maze.append(card.get_value())
            else:
                maze.append(-3)
            ind += 1
        if player.get_name() == data["name"]:
            owner_maze = maze
        else:
            other_mazes[player.get_name()] = maze
    
    pprint({"owner" : owner_maze, "others" : other_mazes})
    return jsonify({"owner" : owner_maze, "others" : other_mazes})

@app.route("/reveal", methods=["POST"])
def reveal_card():
    '''
    Revela las caras seleccionadas por un jugador
    '''
    data = request.get_json()
    player = game.get_player(Player(data["name"], data["password"]))
    if not player:
        return jsonify({"player" : "not fount"})

    for card in data["to_reveal"]:
        try:
            player.to_reveal(int(card))
        except:
            player.to_reveal(card)

    return jsonify({"player" : "revelling"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True, port=PORT)