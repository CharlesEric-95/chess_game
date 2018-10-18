#Python version : 3.7
#Author : Charles-Eric Callaud

class Chess_Controller:
    def __init__(self, chess_model, chess_graphic_interface, IA):
        self.chess_model = chess_model
        self.chess_graphic_interface = chess_graphic_interface
        self.IA = IA
    
    def configure_graphic_functions(self):
        board = self.chess_graphic_interface.get_board()
        board.bind("<Button-1>", self.get_selected_case)
        board.bind_all("u", self.cancel_last_move)
        board.bind_all("i", self.ia_play)
    
    def ia_play(self, event):
        self.IA.play_best_move()
        self.update_graphic_interface()

    def get_selected_case(self, event) :
        case_size = self.chess_graphic_interface.case_size
        column = min(7, max(0, event.x//case_size)) #Avoid border effects 
        line = min(7, max(0, event.y//case_size))   
        selected_index = 8*line + column
        selected_case = self.chess_model.select_case(selected_index)
        if selected_case: self.update_graphic_interface(line, column)
        else : self.update_graphic_interface()
    
    def cancel_last_move(self, event):
        self.chess_model.cancel_last_move()
        self.update_graphic_interface()

    def update_graphic_interface(self, selected_line=None, selected_column=None):
        self.chess_graphic_interface.update(
            self.chess_model.get_board_info(),
            selected_line,
            selected_column)

    def start_game(self) :
        self.configure_graphic_functions()
        self.update_graphic_interface()
        self.chess_graphic_interface.get_master().mainloop()
