#Python version : 3.7
#Author : Charles-Eric Callaud

#Libs
import os

class Color:
    (
        NONE,
        BLACK,
        WHITE
    ) = range(3)


class Piece:
    def __init__(self, name, color, vectors, move_on_several_cases):
        self.name = name
        self.color = color
        if color == Color.BLACK : vectors = [-z for z in vectors]
        self.vectors = vectors
        self.move_on_several_cases = move_on_several_cases

    def __str__(self) :
        if not self.name : return ""
        color = "white" if self.color == Color.WHITE else "black"
        return "%s_%s"%(color, self.name)
    
    def get_special_move_vectors(self):
        return []

    def get_captured(self) :
        self.name = ""
        self.color = Color.NONE
        self.vectors = []
        self.move_on_several_cases = False


class Null(Piece):
    def __init__(self):
        super().__init__(None, Color.NONE, [], False)


class Pawn(Piece):
    def __init__(self, color):
        vectors = [-10]
        super().__init__("pawn", color, vectors, False)

    def get_special_move_vectors(self):
        vectors = [-9, -11, -20]
        return vectors if self.color == Color.WHITE else [ -x for x in vectors]

class Rook(Piece):
    def __init__(self, color):
        vectors = [-10, -1, +1, +10]
        super().__init__("rook", color, vectors, True)


class Knight(Piece):
    def __init__(self, color):
        vectors = [-21, -19, -12, -8, 8, 12, 19, 21]
        super().__init__("knight", color, vectors, False)


class Bishop(Piece):
    def __init__(self, color):
        vectors = [-11, -9, 9, 11]
        super().__init__("bishop", color, vectors, True)


class King(Piece):
    def __init__(self, color):
        vectors = [-11, -10, -9, -1, +1, +9, +10, +11]
        super().__init__("king", color, vectors, False)
    
    def get_special_move_vectors(self):
        return [-2, 2]


class Queen(Piece):
    def __init__(self, color):
        vectors = [-11, -10, -9, -1, +1, +9, +10, +11]
        super().__init__("queen", color, vectors, True)