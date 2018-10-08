#Python version : 3.7
#Author : Charles-Eric Callaud

#My files
from user import User
from board import Board
from chess_graphic_interface import ChessGraphicInterface

graphic_interface = ChessGraphicInterface(500)
player1 = User.HUMAN
player2 = User.HUMAN
board = Board(player1, player2, graphic_interface)