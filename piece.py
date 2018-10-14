#Python version : 3.7
#Author : Charles-Eric Callaud

#Libs
import os

#My files
from direction import Direction

class Color:
    (
        NONE,
        BLACK,
        WHITE
    ) = range(3)


class Piece:
    def __init__(self, name, color, vectors, repeat):
        self.name = name
        self.color = color
        if color == Color.BLACK : vectors = [(z[0], -z[1]) for z in vectors]
        self.directions = Direction(vectors, repeat) 
    
    def __str__(self) :
        if not self.name : return ""
        color = "white" if self.color == Color.WHITE else "black"
        return "%s_%s"%(color, self.name)
    
    def get_captured(self) :
        self.name = ""
        self.color = Color.NONE
        self.directions = Direction([], False)


class Null(Piece):
    def __init__(self):
        super().__init__(None, Color.NONE, [], False)


class Pawn(Piece):
    def __init__(self, color):
        vectors = [(-1,1),(0,1),(1,1)]
        super().__init__("pawn", color, vectors, False)


class Rook(Piece):
    def __init__(self, color):
        vectors = []
        super().__init__("rook", color, vectors, True)


class Knight(Piece):
    def __init__(self, color):
        vectors = []
        super().__init__("knight", color, vectors, False)


class Bishop(Piece):
    def __init__(self, color):
        vectors = []
        super().__init__("bishop", color, vectors, True)


class King(Piece):
    def __init__(self, color):
        vectors = []
        super().__init__("king", color, vectors, False)


class Queen(Piece):
    def __init__(self, color):
        vectors = []
        super().__init__("queen", color, vectors, True)