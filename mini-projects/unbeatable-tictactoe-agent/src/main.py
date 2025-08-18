import tkinter
from enum import Enum

class Color(Enum):
    BLUE = "#4584B6"
    YELLOW = "#FFDE57"
    GRAY = "#343434"
    LIGHT_GRAY = "#646464"


class Game:
    def __init__(self) -> None:
        self.playerX = "X"
        self.playerO = "O"
        self.cur_player = self.playerX
        self.is_game_over: bool = False
        self.BOARD_WH: int = 3
        self._board: list = [0] * self.BOARD_WH**2

        self._window = tkinter.Tk()
        self._window.title("Unbeatable Tic Tac Toe Agent")
        self._window.resizable(False, False)
        self._player_turn_label: tkinter.Label

        self._setup_game_board()

    def start(self):
        self._window.update()
        ww = self._window.winfo_width()
        wh = self._window.winfo_height()
        screen_w = self._window.winfo_screenwidth()
        screen_h = self._window.winfo_screenheight()

        window_x = int((screen_w/2) - (ww/2))
        window_y = int((screen_h/2) - (wh/2))

        self._window.geometry(f"{ww}x{wh}+{window_x}+{window_y}")
        self._window.mainloop()


    def check_for_winner(self):
        for row in range(self.BOARD_WH):
            for col in range(self.BOARD_WH):
                pass

    def _create_turn_msg(self, frame):
        self._player_turn_label = tkinter.Label(frame, text=f"{self.cur_player}'s turn", font=("Consolas", 20), background=Color.GRAY.value, foreground="white")
        self._player_turn_label.grid(row=0, column=0, columnspan=3, sticky="we")

    def _create_board_btns(self, frame):
        for row in range(self.BOARD_WH): 
            for col in range(self.BOARD_WH):
                index_pos = row*self.BOARD_WH+col
                
                self._board[index_pos] = tkinter.Button(frame, text="", font=("Consolas", 50, "bold"), background=Color.GRAY.value, foreground=Color.BLUE.value, width=4, height=2, command=lambda i=index_pos: self._set_player_mark(i))

                self._board[index_pos].grid(row=row+1, column=col)

    def _set_player_mark(self, index_pos: int) -> None:
        if self.is_game_over: return
        if self._board[index_pos]["text"] != "": return
        
        self._board[index_pos]["text"] = self.cur_player
        if self.cur_player == self.playerO: 
            self._board[index_pos]["foreground"] = Color.YELLOW.value
            self.cur_player = self.playerX
        else:
            self._board[index_pos]["foreground"] = Color.BLUE.value
            self.cur_player = self.playerO

        self._player_turn_label["text"] = f"{self.cur_player}'s turn"
        self.check_for_winner()

    def _create_new_game_btn(self, frame):
        new_game_btn = tkinter.Button(frame, text="New Game", font=("Consolas", 20), background=Color.GRAY.value, foreground="black", height=2, command=self._create_new_game)
        new_game_btn.grid(row=4, column=0, columnspan=3, sticky="we")

    def _create_new_game(self):
        for row in range(self.BOARD_WH):
            for col in range(self.BOARD_WH):
                self._board[row*self.BOARD_WH+col]["text"] = ""
        
        self.cur_player = self.playerX
        self._player_turn_label.config(text=f"{self.cur_player}'s turn", foreground="white")
        self.is_game_over = False

    def _setup_game_board(self):
        frame = tkinter.Frame(self._window) 
        self._create_turn_msg(frame)
        self._create_board_btns(frame)
        self._create_new_game_btn(frame)
        frame.pack()




game = Game()
game.start()