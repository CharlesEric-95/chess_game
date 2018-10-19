#Python version : 3.7
#Author : Charles-Eric Callaud

#My files
from piece import Color
from player import Player, User

class AlphaBeta(Player):
    def __init__(self, ordre, score_function, chess_game=None):
        self.ordre = ordre
        self.score_function = score_function
        self.user = User.COMPUTER
        self.chess_game = chess_game
    
    def get_score(self):
        return self.score_function(self.chess_game)

    def find_best_move(
            self, depth, best_min = float("inf"), best_max = -float("inf")
            ):
        if depth == 0 or self.chess_game.is_check_mate() : 
            return self.get_score(), None, None
        if self.chess_game.turn == Color.WHITE:
            score, best_departure, best_arrival = self.compute_maxi(depth, best_min, best_max)
            best_min = min(score, best_min)
        else : 
            score, best_departure, best_arrival = self.compute_mini(depth, best_min, best_max)
            best_max = max(score, best_max)
        return score, best_departure, best_arrival

    def compute_maxi(self, depth, best_min, best_max):
        score = -float("inf")
        positions = self.chess_game.get_all_positions(self.chess_game.turn)
        for position in positions:
            piece = self.chess_game.board[position]
            arrivals = self.chess_game.get_reachable_cases(piece, position)
            for arrival in arrivals:
                if self.chess_game.try_move_bool(position, arrival):
                    new_score,_,_ = self.find_best_move(depth-1, best_min, best_max)
                    self.chess_game.cancel_last_move()
                    if new_score > score:
                        score = new_score
                        best_departure = position
                        best_arrival = arrival
                    if score >= best_min: return score, None, None #Alpha cut
                    best_max = max(best_max, score)

        return score, best_departure, best_arrival

    def compute_mini(self, depth, best_min, best_max):
        score = float("inf")
        positions = self.chess_game.get_all_positions(self.chess_game.turn)
        for position in positions:
            piece = self.chess_game.board[position]
            arrivals = self.chess_game.get_reachable_cases(piece, position)
            for arrival in arrivals :
                if self.chess_game.try_move_bool(position, arrival):
                    new_score,_,_ = self.find_best_move(depth-1, best_min, best_max)
                    self.chess_game.cancel_last_move()
                    if new_score < score:
                        score = new_score
                        best_departure = position
                        best_arrival = arrival
                    if score <= best_max: return score, None, None #Beta cut
                    best_min = min(best_min, score)
                    
        return score, best_departure, best_arrival

    def play_best_move(self):
        print("IA thinking...")
        ordre = self.ordre
        score, departure, arrival = self.find_best_move(ordre)
        print("AlphaBeta results : %s, %s, %s"%(departure, arrival, score))
        return self.chess_game.move(departure, arrival), departure, arrival
