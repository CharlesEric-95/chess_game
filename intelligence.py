#Python version : 3.7
#Author : Charles-Eric Callaud

#My files
from piece import Color

class AlphaBeta:
    def __init__(self, chess_game):
        self.chess_game = chess_game
    
    def get_score(self):
        if self.chess_game.is_check_mate():
            if self.chess_game.turn == Color.WHITE : return -1000
            return 1000
        score = 0
        for piece in self.chess_game.board:
            factor = +1 if piece.color == Color.WHITE else -1
            if piece.name == "pawn": score += factor*1
            elif piece.name == "rook": score += factor*5
            elif piece.name == "knight": score += factor*3
            elif piece.name == "bishop": score += factor*3
            elif piece.name == "queen": score += factor*12
        return score

    def find_best_move(self, depth):
        if depth == 0 or self.chess_game.is_check_mate() : 
            return self.get_score(), None, None
        
        if self.chess_game.turn == Color.WHITE:
            score, best_departure, best_arrival = self.compute_maxi(depth)
        else : 
            score, best_departure, best_arrival = self.compute_mini(depth)
        
        return score, best_departure, best_arrival

    def compute_maxi(self, depth):
        score = -float("inf")
        positions = self.chess_game.get_all_positions(self.chess_game.turn)
        for position in positions:
            piece = self.chess_game.board[position]
            arrivals = self.chess_game.get_reachable_cases(piece, position)
            for arrival in arrivals:
                if self.chess_game.try_move(position, arrival):
                    new_score,_,_ = self.find_best_move(depth-1)
                    if new_score > score:
                        score = new_score
                        best_departure = position
                        best_arrival = arrival
                    self.chess_game.cancel_last_move()
        return score, best_departure, best_arrival

    def compute_mini(self, depth):
        score = float("inf")
        positions = self.chess_game.get_all_positions(self.chess_game.turn)
        for position in positions:
            piece = self.chess_game.board[position]
            arrivals = self.chess_game.get_reachable_cases(piece, position)
            for arrival in arrivals :
                if self.chess_game.try_move(position, arrival):
                    new_score,_,_ = self.find_best_move(depth-1)
                    if new_score < score:
                        score = new_score
                        best_departure = position
                        best_arrival = arrival
                    self.chess_game.cancel_last_move()
        return score, best_departure, best_arrival

    def play_best_move(self):
        print("IA thinking...")
        ordre = 3
        score, departure, arrival = self.find_best_move(ordre)
        print("MinMax results : %s, %s, %s"%(departure, arrival, score))
        self.chess_game.move(departure, arrival)
        