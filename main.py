#Python version : 3.7
#Author : Charles-Eric Callaud

#Libs
import tkinter as tk

#My files
from user import User
from board import Board
from chess_graphic_interface import ChessGraphicInterface
from controller import Chess_Controller
from intelligence import AlphaBeta

root = tk.Tk()
graphic_interface = ChessGraphicInterface(root, 700)
player1 = User.HUMAN
player2 = User.HUMAN
board = Board(player1, player2, graphic_interface)
IA = AlphaBeta(board)
controller = Chess_Controller(board, graphic_interface, IA)
controller.start_game()