#Python version : 3.7
#Author : Charles-Eric Callaud

class User:
    (
        HUMAN,
        COMPUTER,
    ) = range(2)

class Player:
    def __init__(self, user, chess_game=None):
        self.user = user
        self.chess_game = chess_game
    
    def add_chess_game(self, chess_game):
        self.chess_game = chess_game

    def play(self):
        if self.chess_game==None:
            raise ValueError("Chess_game must be added to Player first with player.add_chess_model()")
        else :
            return self.play_best_move()

    def play_best_move(self):
        if self.user == User.HUMAN: return False, None, None
        else : raise NotImplementedError('"COMPUTER" player should be written as a child class of Player')
