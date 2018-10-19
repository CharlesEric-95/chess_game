#Python version : 3.7
#Author : Charles-Eric Callaud

#Libs
import tkinter as tk

#My files
from piece import Color
from player import Player, User
from board import Board
from chess_graphic_interface import ChessGraphicInterface
from controller import Chess_Controller
from intelligence import AlphaBeta
import score_function as sf

root = tk.Tk()
graphic_interface = ChessGraphicInterface(root, 700)
player1 = Player(User.HUMAN)
player2 = Player(User.HUMAN) #AlphaBeta(3, sf.sum)
chess_game = Board(player1, player2, graphic_interface)
controller = Chess_Controller(chess_game, graphic_interface, player1, player2)
controller.start_game()