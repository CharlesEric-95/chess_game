#Python version : 3.7
#Author : Charles-Eric Callaud

#Libs
import tkinter as tk

#My files
from user import User
from board import Board
from chess_graphic_interface import ChessGraphicInterface
from controller import Chess_Controller

root = tk.Tk()
graphic_interface = ChessGraphicInterface(root, 700)
player1 = User.HUMAN
player2 = User.COMPUTER
board = Board(player1, player2, graphic_interface)
controller = Chess_Controller(board, graphic_interface)
controller.start_game()