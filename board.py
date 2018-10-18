#Python version : 3.7
#Author : Charles-Eric Callaud

#Libs
from random import randint, choice

#My files
from piece import Color, Null, Pawn, Rook, Knight, Bishop, King, Queen
from move import Move
from player import User

class Board:
    def __init__(self, player1, player2, graphic_interface, verbose = False) :
        self.board = [
            Rook(Color.BLACK),
            Knight(Color.BLACK),
            Bishop(Color.BLACK),
            Queen(Color.BLACK),
            King(Color.BLACK),
            Bishop(Color.BLACK),
            Knight(Color.BLACK),
            Rook(Color.BLACK)
        ]
        self.board += [Pawn(Color.BLACK) for _ in range(8)]
        self.board += [Null() for _ in range(32)]
        self.board += [Pawn(Color.WHITE) for _ in range(8)]
        self.board += [
            Rook(Color.WHITE),
            Knight(Color.WHITE),
            Bishop(Color.WHITE),
            Queen(Color.WHITE),
            King(Color.WHITE),
            Bishop(Color.WHITE),
            Knight(Color.WHITE),
            Rook(Color.WHITE)
        ]
        self.board_with_boundaries = [
            -1, -1, -1, -1, -1, -1, -1, -1, -1, -1,
            -1, -1, -1, -1, -1, -1, -1, -1, -1, -1,
            -1,  0,  1,  2,  3,  4,  5,  6,  7, -1,
            -1,  8,  9, 10, 11, 12, 13, 14, 15, -1,
            -1, 16, 17, 18, 19, 20, 21, 22, 23, -1,
            -1, 24, 25, 26, 27, 28, 29, 30, 31, -1,
            -1, 32, 33, 34, 35, 36, 37, 38, 39, -1,
            -1, 40, 41, 42, 43, 44, 45, 46, 47, -1,
            -1, 48, 49, 50, 51, 52, 53, 54, 55, -1,
            -1, 56, 57, 58, 59, 60, 61, 62, 63, -1,
            -1, -1, -1, -1, -1, -1, -1, -1 ,-1 ,-1,
            -1, -1, -1, -1, -1, -1, -1, -1, -1, -1
        ]
        self.player1 = player1
        self.player2 = player2
        self.graphic_interface = graphic_interface
        self.selected_case = None
        self.selected_case_2 = None
        self.turn = Color.WHITE
        self.special_moves_authorization = [
            True, #White castle
            True, #White castle (queen side)
            True, #Black castle
            True, #Black castle (queen side)
            -1,   #White "en passant" capture
            -1    #Black "en passant" capture
        ]
        self.moves_played=[]
        self.end = False
        self.verbose = verbose

    def get_line(self, case):
        return 8-case//8
    
    def get_column(self, case):
        return case%8 + 1

    def get_position(self, piece_name, piece_color):
        return [
            index for index in range(64) 
            if (
                self.board[index].name == piece_name 
                and self.board[index].color == piece_color
            )
        ]

    def get_all_positions(self, color):
        return [
            index for index in range(64) 
            if self.board[index].color == color
        ]

    def play(self):
        if self.end : return
        has_played = False
        if self.turn == Color.WHITE:
            if self.player1.user == User.HUMAN:
                has_played = self.try_move()
            if self.player1.user == User.COMPUTER:
                has_played = self.player1.play()
        elif self.turn == Color.BLACK:
            if self.player2.user == User.HUMAN:
                has_played = self.try_move()
            if self.player2.user == User.COMPUTER:
                has_played = self.player2.play()
        if self.is_check_mate() : 
            print("%s wins"%("Black" if self.turn == Color.WHITE else "White"))
            self.end = True
            return
        if has_played : self.play()

    def select_case(self, index) :
        if self.selected_case == None :
            self.selected_case = index
            return True
        else:
            self.selected_case_2 = index
            self.play()
            return False
   
    def random_move(self):
        departure = choice(self.get_all_positions(self.turn))
        arrival = randint(0,63)
        while not self.try_move(departure, arrival):
            departure = choice(self.get_all_positions(self.turn))
            arrival = randint(0,63)
        return True
    
    def reset_selected_cases(self):
        self.selected_case = None
        self.selected_case_2 = None

    def get_board_info(self):
        board_info = [str(piece) for piece in self.board]
        return board_info

    def teleport(self, departure, arrival):
        board = self.board
        board[departure], board[arrival] = board[arrival], board[departure]

    def try_move(self, departure=None, arrival=None):
        if self.verbose : print("\nTRY TO MOVE %s"%("white" if self.turn == Color.WHITE else "black"))
        if departure == None : departure = self.selected_case
        if arrival == None : arrival = self.selected_case_2
        if departure == None or arrival == None: return self.dont_move()
        if not self.is_move_legal(
            departure, 
            arrival, 
            self.get_move_conditions(departure, arrival)
        ):
            return self.dont_move()
        return self.move(departure, arrival)

    def get_move_conditions(self, departure, arrival, veto = ""):
        conditions =  "color direction path arrival"
        piece = self.board[departure]
        if piece.name == "king" and piece.color == Color.WHITE :
            if arrival == departure+2 :
                conditions =  "color path check unattacked_path arrival castle_w"
            elif arrival == departure-2 :
                conditions =  "color path check unattacked_path arrival castle_wq"
        elif piece.name == "king" and piece.color == Color.BLACK :
            if arrival == departure+2 :
                conditions =  "color path check unattacked_path arrival castle_b"
            elif arrival == departure-2 :
                conditions =  "color path check unattacked_path arrival castle_bq"
        elif piece.name == "pawn" and piece.color == Color.WHITE :
            if arrival == departure-16:
                conditions =  "color path empty_arrival first"
            elif arrival == departure-8 :
                conditions =  "color empty_arrival"
            elif arrival == departure-7 or arrival == departure-9 :
                if self.is_case_empty(arrival) : conditions =  "color passant"
                else : conditions =  "color hostile_arrival"
        elif piece.name == "pawn" and piece.color == Color.BLACK :
            if arrival == departure+16:
                conditions =  "color path empty_arrival first"
            elif arrival == departure+8 :
                conditions =  "color empty_arrival"
            elif arrival == departure+7 or arrival == departure+9 :
                if self.is_case_empty(arrival) : conditions =  "color passant"
                else : conditions =  "color hostile_arrival"

        for keyword in veto.split(" ") :
            conditions = conditions.replace(keyword.replace(" ",""), "")
        return conditions
            

    def is_move_legal(self, departure, arrival, keywords):
        if self.verbose: print("Keywords : %s"%(keywords))
        piece = self.board[departure]
        hostile_color = Color.WHITE if piece.color == Color.BLACK else Color.BLACK
        if "color" in keywords and not self.is_piece_the_good_color(piece) : 
            if self.verbose: print("Piece not the good color")
            return False
        if "direction" in keywords and not self.is_piece_going_into_the_right_directions(departure, arrival):
            if self.verbose: print("Piece not going into the good directions")
            return False
        if "path" in keywords and self.is_path_occupied(departure, arrival):
            if self.verbose: print("Path occupied by other pieces")
            return False
        if "arrival" in keywords and self.is_case_already_occupied_by_team(arrival, piece.color): 
            if self.verbose: print("Arrival already occupied")
            return False
        if "check" in keywords and self.is_king_checked(piece.color):
            if self.verbose: print("King checked")
            return False
        if "unattacked_path" in keywords and self.is_path_attacked(departure, arrival, hostile_color):
            if self.verbose: print("Path attacked")
            return False
        if "empty_arrival" in keywords and not self.is_case_empty(arrival):
            if self.verbose: print("Arrival isn't empty")
            return False
        if "hostile_arrival" in keywords and not self.does_case_contains_piece_of_color(arrival, hostile_color):
            if self.verbose: print("Arrival does not contain hostile piece")
            return False
        if "castle_w" in keywords and not self.special_moves_authorization[0]:
            return False
        if "castle_wq" in keywords and not self.special_moves_authorization[1]:
            return False
        if "castle_b" in keywords and not self.special_moves_authorization[2]:
            return False
        if "castle_bq" in keywords and not self.special_moves_authorization[3]:
            return False
        if "passant" in keywords and not self.can_do_en_passant_capture(departure, arrival):
            return False
        if "first" in keywords and not self.is_pawn_first_move(departure):
            return False
        return True

    def dont_move(self):
        if self.verbose: print("NO MOVE")
        self.reset_selected_cases()
        return False

    def move(self, departure=None, arrival=None):
        if departure == None : departure = self.selected_case
        if arrival == None : arrival = self.selected_case_2
        new_move = Move(
            departure, 
            arrival, 
            self.special_moves_authorization[:],
            captured = not self.is_case_empty(arrival)
        )
        if self.is_special_move(departure, arrival) : 
            self.special_move_features(departure, arrival, new_move)
        board = self.board
        self.reset_selected_cases()
        board[arrival].get_captured()
        self.update_special_moves_authorization(departure, arrival)
        board[departure], board[arrival] = board[arrival], board[departure]
        piece = board[arrival]
        if piece.name == "pawn" and piece.color == Color.WHITE and arrival <= 7 :
            piece.get_promoted()
            new_move.promotion = True
        elif piece.name == "pawn" and piece.color == Color.BLACK and arrival >= 56:
            piece.get_promoted()
            new_move.promotion = True
        self.turn = Color.BLACK if self.turn == Color.WHITE else Color.WHITE
        self.moves_played.append(new_move)
        if self.is_king_checked(piece.color) : 
            self.cancel_last_move()
            return False
        return True

    def special_move_features(self, departure, arrival, move):
        piece = self.board[departure]
        if piece.name == "king" and piece.color == Color.WHITE :
            if arrival == departure+2 : #White castle
                self.teleport(63, 61)
                move.special_departure = 63
                move.special_arrival = 61
                return
            if arrival == departure-2 : #White castle (queen side)
                self.teleport(56, 59)
                move.special_departure = 56
                move.special_arrival = 59
                return
        if piece.name == "king" and piece.color == Color.BLACK :
            if arrival == departure+2 : #Black castle
                self.teleport(7, 5)
                move.special_departure = 7
                move.special_arrival = 5
                return
            if arrival == departure-2 : #Black castle (queen side)
                self.teleport(0, 3)
                move.special_departure = 0
                move.special_arrival = 3
                return
        if piece.name == "pawn" and piece.color == Color.WHITE :
            if arrival == departure-7:
                if self.is_case_empty(arrival):
                    self.board[departure+1].get_captured()
                    move.case_of_captured_piece = departure+1
                    move.captured = True
            elif arrival == departure-9:
                if self.is_case_empty(arrival):
                    self.board[departure-1].get_captured()
                    move.case_of_captured_piece = departure-1
                    move.captured = True
        if piece.name == "pawn" and piece.color == Color.BLACK :
            if arrival == departure+7:
                if self.is_case_empty(arrival):
                    self.board[departure-1].get_captured()
                    move.case_of_captured_piece = departure-1
                    move.captured = True
            elif arrival == departure+9:
                if self.is_case_empty(arrival):
                    self.board[departure+1].get_captured()
                    move.case_of_captured_piece = departure+1
                    move.captured = True


    def is_special_move(self, departure, arrival):
        piece = self.board[departure]
        if piece.name == "king":
            if arrival in [departure+2, departure-2] : return True
        elif piece.name == "pawn":
            factor = -1 if piece.color == Color.WHITE else +1
            arrivals = [departure + factor*i for i in [7,8,9,16]]
            if arrival in arrivals: return True
        return False
    
    def cancel_last_move(self):
        if self.verbose: print("Last move cancelled.")
        if len(self.moves_played) == 0 : return
        self.end = False
        last_move = self.moves_played.pop(-1)
        if last_move.promotion: self.board[last_move.arrival].cancel_promotion()
        self.teleport(last_move.arrival, last_move.departure)
        if last_move.captured:
            self.board[last_move.case_of_captured_piece].resurrect()
        if last_move.special_departure != None :
            self.teleport(last_move.special_arrival, last_move.special_departure)
        self.special_moves_authorization = last_move.special_moves_authorization
        self.turn = Color.WHITE if self.turn == Color.BLACK else Color.BLACK
        
    def update_special_moves_authorization(self, departure, arrival):
        authorization = self.special_moves_authorization
        if departure in [60, 63] : authorization[0] = 0
        if departure in [56, 60] : authorization[1] = 0
        if departure in [4, 7] : authorization[2] = 0
        if departure in [0, 4] : authorization[3] = 0
        piece = self.board[departure]
        if piece.name == "pawn" and self.get_line(departure) == 2 and self.get_line(arrival) == 4:
            authorization[5] = self.get_column(departure)
        else :
            authorization[5] = 0
        if piece.name == "pawn" and self.get_line(departure) == 7 and self.get_line(arrival) == 5:
            authorization[4] = self.get_column(departure)
        else :
            authorization[4] = 0
        

    # -------------------------- USUAL VERIFICATIONS ---------------------------

    def is_piece_the_good_color(self, piece): 
        colors_match = self.turn == piece.color
        return True if colors_match else False

    def is_case_already_occupied_by_team(self, case, color) :
        return self.board[case].color == color

    def is_piece_going_into_the_right_directions(self, departure, arrival):
        piece = self.board[departure]
        return arrival in self.get_reachable_cases(piece, departure)

    def is_path_occupied(self, departure, arrival) :
        path = self.get_path(departure, arrival)
        for case in path : 
            if self.board[case].name != None: 
                return True
        return False

    def is_check_mate(self):
        if not self.is_king_checked(self.turn): return False
        positions = self.get_all_positions(self.turn)
        for position in positions:
            piece=self.board[position]
            arrivals = self.get_reachable_cases(piece, position)
            for arrival in arrivals:
                if self.try_move(position, arrival) :
                    self.cancel_last_move()
                    return False
        return True

    # ------------------------- SPECIAL VERIFICATIONS --------------------------

    def is_king_checked(self, color):
        hostile_color = Color.BLACK if color == Color.WHITE else Color.WHITE
        position = self.get_position("king", color)[0]
        return self.is_case_attacked_by(position, hostile_color)

    def is_path_attacked(self, departure, arrival, hostile_color):
        path = self.get_path(departure, arrival)
        for case in path : 
            if self.is_case_attacked_by(case, hostile_color) : return True
        return False

    def is_case_empty(self, case):
        return self.board[case].name == None

    def does_case_contains_piece_of_color(self, case, color):
        return self.board[case].color == color

    def is_pawn_first_move(self, departure):
        pawn = self.board[departure]
        if pawn.color == Color.WHITE and self.get_line(departure) == 2:
            return True
        if pawn.color == Color.BLACK and self.get_line(departure) == 7:
            return True
        return False
    # --------------------------------- OTHERS ---------------------------------

    def get_reachable_cases(self, piece, departure):
        reachable_cases = []
        for vector in piece.vectors:
            new_departure = self.board_with_boundaries.index(departure)
            new_case = new_departure + vector
            while self.board_with_boundaries[new_case] != -1 :
                reachable_cases.append(self.board_with_boundaries[new_case])
                if piece.move_on_several_cases : new_case += vector
                else : new_case = 0
        return reachable_cases


    def get_path(self, departure, arrival):
        if self.get_line(departure) == self.get_line(arrival) :
             return self.get_path_line(departure, arrival)
        if self.get_column(departure) == self.get_column(arrival) : 
            return self.get_path_column(departure, arrival)
        if self.get_distance(departure) == self.get_distance(arrival) :
            return self.get_path_diagonal_slash_shape(departure, arrival)
        if departure%9 == arrival%9 and self.get_distance(departure)%2 == self.get_distance(arrival)%2:
            return self.get_path_diagonal_anti_slash_shape(departure, arrival)
        return []
    
    def get_path_line(self, departure, arrival):
        departure, arrival = min(departure, arrival), max(departure, arrival)
        return [departure + i for i in range(1, arrival-departure)]
    
    def get_path_column(self, departure, arrival): 
        departure, arrival = min(departure, arrival), max(departure, arrival)
        return [departure + 8*i for i in range(1, arrival//8-departure//8)]

    def get_path_diagonal_slash_shape(self, departure, arrival):
        departure, arrival = min(departure, arrival), max(departure, arrival)
        return [departure + 7*i for i in range(1, arrival//7-departure//7)]
    
    def get_path_diagonal_anti_slash_shape(self, departure, arrival):
        departure, arrival = min(departure, arrival), max(departure, arrival)
        return [departure + 9*i for i in range(1, arrival//9-departure//9)]

    def get_distance(self, index):
        return index%8 + index//8

    def is_case_attacked_by(self, case, hostile_color):
        if self.verbose: print("Is case %s attacked ?"%case)
        hostile_positions = self.get_all_positions(hostile_color)
        for position in hostile_positions:
            piece = self.board[position] 
            cases = self.get_reachable_cases(piece, position)
            if case in cases:
                conditions = self.get_move_conditions(position, case, veto="color")
                if self.is_move_legal(position, case, conditions):
                    if self.verbose: print("Case %s attacked by %s"%(case, position))
                    return True
        if self.verbose: print("Case %s unattacked"%case)
        return False

    def can_do_en_passant_capture(self, departure, arrival):
        if self.get_line(departure) == 5:
            return self.get_column(arrival) == self.special_moves_authorization[4]
        if self.get_line(departure) == 4:
            return self.get_column(arrival) == self.special_moves_authorization[5]