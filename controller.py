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
    
    def get_line_and_column_from_event(self, event):
        case_size = self.chess_graphic_interface.case_size
        column = min(8, max(1, event.x//case_size + 1)) #Avoid border effects 
        line = 9-min(8, max(1, event.y//case_size + 1))
        return line, column
    
    def get_index_from(self, line, column):
        score = (8-line)*8 + column -1
        return score

    def get_index_from_event(self, event):
        return self.get_index_from(*self.get_line_and_column_from_event(event))

    def get_line_and_column_from_index(self, index):
        return (
            self.chess_model.get_line(index),
            self.chess_model.get_column(index)
        )

    def configure_graphic_functions(self):
        board = self.chess_graphic_interface.get_board()
        board.bind("<Button-1>", self.get_selected_case)
        board.bind_all("u", self.cancel_last_move)
        board.bind("<Button-2>", self.kill_or_resurrect)
        board.bind("<Button-3>", self.teleport)
    
    def kill_or_resurrect(self, event):
        selected_index = self.get_index_from_event(event)
        piece = self.chess_model.board[selected_index]
        if piece.name == None : piece.resurrect()
        else : piece.get_captured()
        self.update_graphic_interface()

    def teleport(self, event):
        selected_index = self.get_index_from_event(event)
        if self.teleport_departure == None:
            self.teleport_departure = selected_index
        else:
            self.chess_model.teleport(self.teleport_departure, selected_index)
            self.teleport_departure = None
        self.update_graphic_interface()

    def get_selected_case(self, event) :
        line, column = self.get_line_and_column_from_event(event)
        selected_index = self.get_index_from(line, column)
        selected_case = self.chess_model.select_case(selected_index)
        if selected_case: self.update_graphic_interface([(line, column)])
        else : 
            self.play()
    
    def cancel_last_move(self, event):
        self.chess_model.cancel_last_move()
        self.update_graphic_interface()

    def update_graphic_interface(self, highlited_case=[]):
        self.chess_graphic_interface.update(
            self.chess_model.get_board_info(), highlited_case
            )

    def play(self):
        if self.chess_model.end : return
        has_played, departure, arrival = self.play_a_color(self.chess_model.turn)

        if has_played: 
            departure = self.get_line_and_column_from_index(departure)
            arrival = self.get_line_and_column_from_index(arrival)
            self.update_graphic_interface([departure, arrival])

        if self.chess_model.is_check_mate() : 
            print("%s wins"%("Black" if self.chess_model.turn == Color.WHITE else "White"))
            self.chess_model.end = True
            return 

        if has_played : self.play()
        return

    def play_a_color(self, color):
        player = self.player1 if color == Color.WHITE else self.player2
        if player.user == User.HUMAN:
            has_played, departure, arrival = self.chess_model.try_move()
        elif player.user == User.COMPUTER:
            has_played, departure, arrival = player.play()
        if departure == None or arrival == None : 
            return has_played, None, None
        return has_played, departure, arrival

    def start_game(self) :
        self.configure_graphic_functions()
        self.update_graphic_interface()
        self.play()
        self.chess_graphic_interface.get_master().mainloop()
