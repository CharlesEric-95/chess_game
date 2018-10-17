#Python version : 3.7
#Author : Charles-Eric Callaud

#Libs
import os
import tkinter as tk

import config_interface as config

class ChessGraphicInterface:
    def __init__(self, master, board_size = config.board_size):
        #Variables zone
        self.case_size = board_size//8
        self.board_size = self.case_size * 8
        #Tkinter zone
        self.master = master
        self.master.title("Chess Game")
        self.board = tk.Canvas(
            master = self.master, 
            width = self.board_size, 
            height = self.board_size
        )
        self.board.image_used = {}
        self.board.pack()
    
    def get_master(self):
        return self.master

    def get_board(self):
        return self.board

    def draw_board(self) :
        self.board.delete("all")
        self.board.create_rectangle(
            2,2,self.board_size+1,self.board_size+1,fill=None
        ) #Offsets are chosen in order to make the grid visible
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

    def draw_pieces_on_board(self, board_info) :
        x, y = 0, 0
        for i in range(64):
            piece = board_info[i]
            if piece != "" :
                picture_path = os.path.join(
                    config.pictures_folder, 
                    "%s.%s"%(piece, config.pictures_extension)
                )
                center_x = x + (self.case_size)/2
                center_y = y + (self.case_size)/2
                if picture_path in self.board.image_used : 
                    piece_picture = self.board.image_used[picture_path]
                else :
                    piece_picture = tk.PhotoImage(
                        file=picture_path,
                        master=self.master
                    )
                    self.board.image_used[picture_path] = piece_picture
                self.board.create_image(center_x, center_y, image=piece_picture)
            x += self.case_size
            if x == self.board_size :
                x = 0
                y += self.case_size

    def update(self, board_info):
        self.draw_board()
        self.draw_pieces_on_board(board_info) 
        self.master.update_idletasks()
        self.master.update()