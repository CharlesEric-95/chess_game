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
        if self.name == None: return ""
        color = "white" if self.color == Color.WHITE else "black"
        return "%s_%s"%(color, self.name)
    
    def get_special_move_vectors(self):
        return []

    def get_captured(self) :
        self.name = None
        self.color = Color.NONE
        self.vectors = []
        self.move_on_several_cases = False

    def get_promoted(self) :
        return

    def get_resurrected(self, color):
        raise NotImplementedError


class Null(Piece):
    def __init__(self):
        super().__init__(None, Color.NONE, [], False)
    
    def resurrect(self, color):
        return


class Pawn(Piece):
    def __init__(self, color):
        vectors = []
        super().__init__("pawn", color, vectors, False)
    
    def resurrect(self, color):
        self.__init__(color)

    def get_special_move_vectors(self):
        vectors = [-9, -10, -11, -20]
        return vectors if self.color == Color.WHITE else [ -x for x in vectors]

    def get_promoted(self):
        self.name = "queen"
        self.vectors = [-11, -10, -9, -1, +1, +9, +10, +11]
        self.move_on_several_cases = True


class Rook(Piece):
    def __init__(self, color):
        vectors = [-10, -1, +1, +10]
        super().__init__("rook", color, vectors, True)
    
    def resurrect(self, color):
        self.__init__(color)


class Knight(Piece):
    def __init__(self, color):
        vectors = [-21, -19, -12, -8, 8, 12, 19, 21]
        super().__init__("knight", color, vectors, False)
    
    def resurrect(self, color):
        self.__init__(color)


class Bishop(Piece):
    def __init__(self, color):
        vectors = [-11, -9, 9, 11]
        super().__init__("bishop", color, vectors, True)
    
    def resurrect(self, color):
        self.__init__(color)


class King(Piece):
    def __init__(self, color):
        vectors = [-11, -10, -9, -1, +1, +9, +10, +11]
        super().__init__("king", color, vectors, False)
    
    def get_special_move_vectors(self):
        return [-2, 2]
    
    def resurrect(self, color):
        self.__init__(color)


class Queen(Piece):
    def __init__(self, color):
        vectors = [-11, -10, -9, -1, +1, +9, +10, +11]
        super().__init__("queen", color, vectors, True)
    
    def resurrect(self, color):
        self.__init__(color)