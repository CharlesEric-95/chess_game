#Python version : 3.7
#Author : Charles-Eric Callaud

#My files
from piece import Color, Null, Pawn, Rook, Knight, Bishop, King, Queen
from move import Move

class Board:
    def __init__(self, player1, player2, graphic_interface) :
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

    def select_case(self, index) :
        if self.selected_case == None :
            self.selected_case = index
        else:
            self.selected_case_2 = index
            self.try_move()
    
    def reset_selected_cases(self):
        self.selected_case = None
        self.selected_case_2 = None

    def get_board_info(self):
        board_info = [str(piece) for piece in self.board]
        return board_info

    def teleport(self, departure, arrival):
        board = self.board
        board[departure], board[arrival] = board[arrival], board[departure]

    def try_move(self):
        print("\nTRY TO MOVE")
        if self.selected_case == None : return self.dont_move()
        if self.selected_case_2 == None : return self.dont_move()
        if not self.is_move_legal(
            self.selected_case, 
            self.selected_case_2, 
            self.get_move_conditions()
        ):
            return self.dont_move()
        return self.move()

    def get_move_conditions(self):
        departure = self.selected_case
        arrival = self.selected_case_2
        piece = self.board[departure]
        if arrival in self.get_reachable_cases(piece, departure, True):
            if piece.name == "king" and piece.color == Color.WHITE :
                if arrival == departure+2 :
                    return "color path unattacked_path arrival castle_w"
                if arrival == departure-2 :
                    return "color path unattacked_path arrival castle_wq"
            if piece.name == "king" and piece.color == Color.BLACK :
                if arrival == departure+2 :
                    return "color path unattacked_path arrival castle_b"
                if arrival == departure-2 :
                    return "color path unattacked_path arrival castle_bq"
            if piece.name == "pawn" and piece.color == Color.WHITE :
                if arrival == departure-16:
                    return "color path empty_arrival"
                if arrival == departure-8 :
                    return "color empty_arrival"
                if arrival == departure-7 or arrival == departure-9 :
                    if self.is_case_empty(arrival) :
                        return "color passant"
                    return "color hostile_arrival"
            if piece.name == "pawn" and piece.color == Color.BLACK :
                if arrival == departure+16:
                    return "color path empty_arrival"
                if arrival == departure+8 :
                    return "color empty_arrival"
                if arrival == departure+7 or arrival == departure+9 :
                    if self.is_case_empty(arrival) :
                        return "color passant"
                    return "color hostile_arrival"
        else :
            return "usual"

    def is_move_legal(self, departure, arrival, keywords = None):
        if keywords == None : keywords = "usual"
        keywords = keywords.replace("usual", "color direction path arrival")
        print("Keywords : %s"%keywords)
        piece = self.board[departure]
        hostile_color = Color.WHITE if piece.color == Color.BLACK else Color.BLACK
        if "color" in keywords and not self.is_piece_the_good_color() : 
            print("Piece not the good color")
            return False
        if "direction" in keywords and not self.is_piece_going_into_the_right_directions():
            print("Piece not going into the good directions")
            return False
        if "path" in keywords and self.is_path_occupied():
            print("Path occupied by other pieces")
            return False
        if "arrival" in keywords and self.is_case_already_occupied(): 
            print("Arrival already occupied")
            return False
        if "check" in keywords and self.is_king_checked(piece.color):
            print("King checked")
            return False
        if "unattacked_path" in keywords and self.is_path_attacked(departure, arrival, hostile_color):
            print("Path attacked")
            return False
        if "empty_arrival" in keywords and not self.is_case_empty(arrival):
            print("Arrival isn't empty")
            return False
        if "hostile_arrival" in keywords and not self.does_case_contains_piece_of_color(arrival, hostile_color):
            print("Arrival does not contain hostile piece")
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
        return True

    def dont_move(self):
        self.reset_selected_cases()
        return False

    def move(self):
        new_move = Move(
            self.selected_case, 
            self.selected_case_2, 
            self.special_moves_authorization[:]
        )
        if self.is_special_move() : self.special_move_patterns(new_move)
        index = self.selected_case
        index_2 = self.selected_case_2
        board = self.board
        self.reset_selected_cases()
        board[index_2].get_captured()
        board[index], board[index_2] = board[index_2], board[index]
        piece = board[index_2]
        if piece.color == Color.WHITE and index_2 <= 7 :
            piece.get_promoted()
        elif piece.color == Color.BLACK and index_2 >= 56:
            piece.get_promoted()
        self.turn = Color.BLACK if self.turn == Color.WHITE else Color.WHITE
        self.moves_played.append(new_move)
        return True

    def special_move_patterns(self, move):
        departure = self.selected_case
        arrival = self.selected_case_2
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
            if arrival == departure-7 or arrival == departure-9 :
                if self.is_case_empty(arrival) :
                    self.board[arrival-8].get_captured()
                    move.case_of_captured_piece = arrival-8
                    return
        if piece.name == "pawn" and piece.color == Color.BLACK :
            if arrival == departure+7 or arrival == departure+9 :
                if self.is_case_empty(arrival) :
                    self.board[arrival+8].get_captured()
                    move.case_of_captured_piece = arrival+8
                    return

    def is_special_move(self):
        return self.is_piece_going_into_the_right_directions(True)
    
    def cancel_last_move(self):
        if len(self.moves_played) == 0 : return
        last_move = self.moves_played.pop(-1)
        color_captured = Color.WHITE if self.turn == Color.WHITE else Color.BLACK
        self.teleport(last_move.arrival, last_move.departure)
        captured_piece = self.board[last_move.case_of_captured_piece]
        captured_piece.resurrect(color_captured)
        if last_move.special_departure != None :
            self.teleport(last_move.special_arrival, last_move.special_departure)
        self.special_moves_authorization = last_move.special_moves_authorization
        self.turn = Color.WHITE if self.turn == Color.BLACK else Color.BLACK
        

    # -------------------------- USUAL VERIFICATIONS ---------------------------

    def is_piece_the_good_color(self): 
        colors_match = self.turn == self.board[self.selected_case].color
        return True if colors_match else False

    def is_case_already_occupied(self) :
        board = self.board
        selected_case = self.selected_case
        selected_case_2 = self.selected_case_2
        return board[selected_case].color == board[selected_case_2].color

    def is_piece_going_into_the_right_directions(self, special_move = False):
        case = self.selected_case
        piece = self.board[self.selected_case]
        print("Reachable cases %s: %s"%(
            "Special " if special_move else "",
            self.get_reachable_cases(piece, case, special_move)
            ))
        return self.selected_case_2 in self.get_reachable_cases(piece, case, special_move)

    def is_path_occupied(self) :
        path = self.get_path(self.selected_case, self.selected_case_2)
        print("Path : %s"%path)
        for case in path : 
            if self.board[case].name != None: 
                print("Piece on the way : %s"%self.board[case].name)
                return True
        return False

    # ------------------------- SPECIAL VERIFICATIONS --------------------------

    def is_king_checked(self, color):
        hostile_color = Color.BLACK if color == Color.WHITE else Color.WHITE
        position = self.get_position("king", color)[0]
        return self.is_case_attacked_by(position, hostile_color)
        """
        hostile_positions = self.get_all_positions(hostile_color)
        for position in hostile_position:
            piece = self.board[position] 
            if king in self.get_reachable_cases(piece, position):
                if #Faire un move à conditions variables# :
                    return True
        return False
        """

    def is_path_attacked(self, departure, arrival, hostile_color):
        path = self.get_path(departure, arrival)
        for case in path : 
            if self.is_case_attacked_by(case, hostile_color) : return True
        return False

    def is_case_empty(self, case):
        return self.board[case].name == None

    def does_case_contains_piece_of_color(self, case, color):
        return self.board[case].color == color

    # --------------------------------- OTHERS ---------------------------------

    def get_reachable_cases(self, piece, departure, special_move = False):
        reachable_cases = []
        if special_move == False: vectors = piece.vectors
        else : vectors = piece.get_special_move_vectors()
        for vector in vectors:
            new_departure = self.board_with_boundaries.index(departure)
            new_case = new_departure + vector
            while self.board_with_boundaries[new_case] != -1 :
                reachable_cases.append(self.board_with_boundaries[new_case])
                if piece.move_on_several_cases : new_case += vector
                else : new_case = 0
        return reachable_cases


    def get_path(self, departure, arrival):
        if departure//8 == arrival//8 : return self.get_path_line(departure, arrival)
        if departure%8 == arrival%8 : return self.get_path_column(departure, arrival)
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
        return False 
        #TODO
        """
        hostile_pieces = self.get_all_positions(hostile_color)
        for position in hostile_position:
            piece = self.board[position] 
            if case in self.get_reachable_cases(piece, position):
                if #Faire un move à conditions variables# :
                    return True
        return False
        """

    def can_do_en_passant_capture(self, departure, arrival):
        return False
        #TODO