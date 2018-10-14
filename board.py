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
        if not self.is_piece_the_good_color() : return False
        if not self.is_piece_going_into_the_right_directions() : return False
        return True

    def is_piece_the_good_color(self): 
        colors_match = self.turn == self.board[self.selected_case].color
        return True if colors_match else False
    
    def is_piece_going_into_the_right_directions(self):
        return True