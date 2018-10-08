#Python version : 3.7
#Author : Charles-Eric Callaud

class Board:
    def __init__(self, player1, player2, graphic_interface) :
        self.board = [[0] * 64]
        self.player1 = player1
        self.player2 = player2
        self.graphic_interface = graphic_interface
        
    def ask_refresh(self):
        self.graphic_interface.resfresh()