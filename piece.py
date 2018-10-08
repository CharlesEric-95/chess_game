#Python version : 3.7
#Author : Charles-Eric Callaud

#Libs
import os

#My files
from direction import Direction

class Color:
    (
        BLACK,
        WHITE
    ) = range(2)


class Piece:
    def __init__(self, color, vectors, repeat):
        self.color = color
        self.directions = Direction(vectors, repeat) 
    
    def get_picture_path(self) :
        raise NotImplementedError


class Pawn(Piece):
    def __init__(self, color):
        vectors = [(-1,1),(0,1),(1,1)]
        if color == Color.BLACK : vectors = [(z[0], -z[1]) for z in vectors]
        super.__init__(color, vectors, False)

    def get_picture_path(self):
        color = "white" if self.color == Color.WHITE else "black"
        return os.path.join("resources", "%s_pawn"%(color))
