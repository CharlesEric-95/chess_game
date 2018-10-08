#Python version : 3.7
#Author : Charles-Eric Callaud

import tkinter as tk

class ChessGraphicInterface:
    def __init__(self, board_size):
        self.case_size = board_size//8
        self.board_size = self.case_size * 8

        self.root = tk.Tk()
        self.root.title = "Chess Game"
        self.board = tk.Canvas(self.root)
        self.board.pack()

        self.draw_board()

        self.root.mainloop()
    
    def draw_board(self) :
        colors=['white','black']
        x, y, line = 0, 0, 0
        line = 0
        for i in range(64) :
            self.board.create_rectangle(
                x, y, x + self.case_size, y + self.case_size,
                fill= str(colors[(i + line) % 2])
            )
            x += self.case_size
            if x == self.board_size  :
                x=0
                y += self.case_size
                line += 1

    def refresh(self): 
        self.root.refresh()