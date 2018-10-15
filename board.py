#Python version : 3.7
#Author : Charles-Eric Callaud

#My files
from piece import Color, Null, Pawn, Rook, Knight, Bishop, King, Queen

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

    def select_case(self, index) :
        if self.selected_case == None :
            self.selected_case = index
        else:
            self.selected_case_2 = index
            self.try_move()

    def get_board_info(self):
        board_info = [str(piece) for piece in self.board]
        return board_info

    def reset_selected_cases(self):
        self.selected_case = None
        self.selected_case_2 = None

    def try_move(self):
        if self.selected_case == None : return self.dont_move()
        if self.selected_case_2 == None : return self.dont_move()
        if not self.move_legal() : return self.dont_move()
        return self.move()

    def dont_move(self):
        self.reset_selected_cases()
        return False

    def move(self):
        index = self.selected_case
        index_2 = self.selected_case_2
        board = self.board
        self.reset_selected_cases()
        board[index_2].get_captured()
        board[index], board[index_2] = board[index_2], board[index]
        self.turn = Color.BLACK if self.turn == Color.WHITE else Color.WHITE
        return True

    def move_legal(self):
        if not self.is_piece_the_good_color() : 
            print("Piece not the good color")
            return False
        if self.is_case_already_occupied() : 
            print("Arrival already occupied")
            return False
        if not self.is_piece_going_into_the_right_directions() : 
            print("Piece not going into the good directions")
            return False
        return True

    def is_piece_the_good_color(self): 
        colors_match = self.turn == self.board[self.selected_case].color
        return True if colors_match else False
    
    def is_piece_going_into_the_right_directions(self):
        case = self.selected_case
        piece = self.board[self.selected_case]
        print(self.get_reachable_cases(piece, case))
        return self.selected_case_2 in self.get_reachable_cases(piece, case)

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
    
    def is_case_already_occupied(self) :
        board = self.board
        selected_case = self.selected_case
        selected_case_2 = self.selected_case_2
        return board[selected_case].color == board[selected_case_2].color
    