#Python version : 3.7
#Author : Charles-Eric Callaud

class Move:
    def __init__(
            self,
            departure, arrival,
            special_moves_authorization,
            captured = False,
            promotion = False,
            special_departure = None, 
            special_arrival = None, 
            case_of_captured_piece = None
            ):
        self.departure = departure
        self.arrival = arrival
        self.special_moves_authorization = special_moves_authorization
        self.captured = captured
        self.promotion = promotion
        self.special_departure = special_departure
        self.special_arrival = special_arrival
        if case_of_captured_piece == None:
            self.case_of_captured_piece = arrival
        else:
            self.case_of_captured_piece = case_of_captured_piece
        
        
