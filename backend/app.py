from flask import Flask, jsonify, request
from typing import Iterable, Iterator
from itertools import zip_longest
from time import time
from ReversiSolver import ReversiSolver
app = Flask(__name__)

games = {}

@app.route('/new_game', methods=['POST'])
def newGame():
    id = str(time()).replace(".", "")
    if id in games:
        id = id+"a"
    game = ReversiSolver()
    games[id] = {}
    games[id]['game'] = game
    games[id]['type'] = 'ai' # ai, human
    return jsonify({"status": 200, "id": id, "states": game.get_states()})

def grouper(n: int, iterable: Iterable, padvalue: str ='0') -> Iterator:
    return zip_longest(*[iter(iterable)]*n, fillvalue=padvalue)

@app.route('/move', methods=['POST'])
def move():
    player_move = tuple(request.get_json()["move"])
    id = request.get_json()["id"]
    game = games[id]['game']
    color = request.get_json()["color"]
    use_ai = request.get_json()["use_ai"]
    move, flips = game.move(player_move, color=color, respond_with_move=use_ai)
    return jsonify({"move": move, "flips": flips, "states": game.get_states()})


# @app.route('/next_move', methods=['POST'])
# def getNextMove():
#     player_move = tuple(request.get_json()["move"])
#     id = request.get_json()["id"]
#     use_ai = request.get_json()["use_ai"]
#     game = games[id]['game']
#     # move = game.move(player_move, respond_with_move=use_ai)
#     # chunks: Iterator = grouper(8, state)
#     # for chunk in chunks:
#     #     print(chunk)

#     return jsonify({"move": move, "states": game.get_states()})