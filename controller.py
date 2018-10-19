#Python version : 3.7
#Author : Charles-Eric Callaud

#My files
from piece import Color
from player import User

class Chess_Controller:
    def __init__(self, chess_model, chess_graphic_interface, player1, player2):
        self.chess_model = chess_model
        self.chess_graphic_interface = chess_graphic_interface
        self.player1 = player1
        self.player2 = player2
        player1.add_chess_game(self.chess_model)
        player2.add_chess_game(self.chess_model)
        self.teleport_departure = None
    
    def configure_graphic_functions(self):
        board = self.chess_graphic_interface.get_board()
        board.bind("<Button-1>", self.get_selected_case)
        board.bind_all("u", self.cancel_last_move)
        board.bind("<Button-2>", self.kill_or_resurrect)
        board.bind("<Button-3>", self.teleport)
    
    def kill_or_resurrect(self, event):
        case_size = self.chess_graphic_interface.case_size
        column = min(7, max(0, event.x//case_size)) #Avoid border effects 
        line = min(7, max(0, event.y//case_size))   
        selected_index = 8*line + column
        piece = self.chess_model.board[selected_index]
        if piece.name == None : piece.resurrect()
        else : piece.get_captured()
        self.update_graphic_interface()

    def teleport(self, event):
        case_size = self.chess_graphic_interface.case_size
        column = min(7, max(0, event.x//case_size)) #Avoid border effects 
        line = min(7, max(0, event.y//case_size))   
        selected_index = 8*line + column
        if self.teleport_departure == None:
            self.teleport_departure = selected_index
        else:
            self.chess_model.teleport(self.teleport_departure, selected_index)
            self.teleport_departure = None
        self.update_graphic_interface()

    def get_selected_case(self, event) :
        case_size = self.chess_graphic_interface.case_size
        column = min(7, max(0, event.x//case_size)) #Avoid border effects 
        line = min(7, max(0, event.y//case_size))   
        selected_index = 8*line + column
        selected_case = self.chess_model.select_case(selected_index)
        if selected_case: self.update_graphic_interface(line, column)
        else : 
            self.play()
            self.update_graphic_interface()
    
    def cancel_last_move(self, event):
        self.chess_model.cancel_last_move()
        self.update_graphic_interface()

    def update_graphic_interface(self, selected_line=None, selected_column=None):
        self.chess_graphic_interface.update(
            self.chess_model.get_board_info(),
            selected_line,
            selected_column)

    def play(self):
        if self.chess_model.end : return
        has_played = False
        if self.chess_model.turn == Color.WHITE:
            if self.player1.user == User.HUMAN:
                has_played = self.chess_model.try_move()
            if self.player1.user == User.COMPUTER:
                has_played = self.player1.play()
            self.update_graphic_interface()
        elif self.chess_model.turn == Color.BLACK:
            if self.player2.user == User.HUMAN:
                has_played = self.chess_model.try_move()
            if self.player2.user == User.COMPUTER:
                has_played = self.player2.play()
            self.update_graphic_interface()
        if self.chess_model.is_check_mate() : 
            print("%s wins"%("Black" if self.chess_model.turn == Color.WHITE else "White"))
            self.chess_model.end = True
            return
        if has_played : self.play()

    def start_game(self) :
        self.configure_graphic_functions()
        self.play()
        self.update_graphic_interface()
        self.chess_graphic_interface.get_master().mainloop()
