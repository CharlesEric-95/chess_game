#Python version : 3.7
#Author : Charles-Eric Callaud

class Direction:
    #Class describing available moves for a chess piece.
    def __init__(self, vectors, repeat):
        self.vectors = vectors
        self.repeat = repeat
            