#Python version : 3.7
#Author : Charles-Eric Callaud

#My files
from piece import Color

def sum(chess_game):
    if chess_game.is_check_mate():
        if chess_game.turn == Color.WHITE : return -1000
        return 1000
    if chess_game.is_draw():
        return 0
    score = 0
    for piece in chess_game.board:
        factor = +1 if piece.color == Color.WHITE else -1
        if piece.name == "pawn": score += factor*1
        elif piece.name == "rook": score += factor*5
        elif piece.name == "knight": score += factor*3
        elif piece.name == "bishop": score += factor*3
        elif piece.name == "queen": score += factor*12
    return score