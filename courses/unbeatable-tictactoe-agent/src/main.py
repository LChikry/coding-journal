import tkinter


playerX = "X"
playerO = "O"
curr_player = playerX

BOARD_WIDTH: int = 3
BOARD_HEIGHT: int = 3
board: list = [0] * BOARD_HEIGHT * BOARD_WIDTH


def set_tile(index_pos) -> None:
    if board[index_pos]["text"] != "": return
    
    global curr_player
    board[index_pos]["text"] = curr_player
    if curr_player == playerO: curr_player = playerX
    else: curr_player = playerO

    player_turn_label["text"] = f"{curr_player}'s turn"


def new_game():
    for row in range(BOARD_HEIGHT):
        for col in range(BOARD_WIDTH):
            board[row*BOARD_WIDTH+col]["text"] = ""
    
    global curr_player
    curr_player = playerX
    player_turn_label["text"] = f"{curr_player}'s turn"


color_blue: str = "#4584B6"
color_yellow: str = "#FFDE57"
color_gray: str = "#343434"
color_light_gray: str = "#646464"

window = tkinter.Tk()
window.title("Unbeatable Tic Tac Toe Agent")
window.resizable(False, False)
frame = tkinter.Frame(window) 


player_turn_label = tkinter.Label(frame, text=f"{curr_player}'s turn", font=("Consolas", 20), background=color_gray, foreground="white")

player_turn_label.grid(row=0, column=0, columnspan=3, sticky="we")

for row in range(BOARD_HEIGHT): 
    for col in range(BOARD_WIDTH):
        print(row*BOARD_WIDTH+col)
        index_pos = row*BOARD_WIDTH+col
        board[index_pos] = tkinter.Button(frame, text="", font=("Consolas", 50, "bold"), background=color_gray, foreground=color_blue, width=4, height=2, command=lambda i=index_pos: set_tile(i))

        board[row*BOARD_WIDTH+col].grid(row=row+1, column=col)


new_game_btn = tkinter.Button(frame, text="New Game", font=("Consolas", 20), background=color_gray, foreground="black", height=2, command=new_game)

new_game_btn.grid(row=4, column=0, columnspan=3, sticky="we")

frame.pack()

window.update()
ww = window.winfo_width()
wh = window.winfo_height()
screen_w = window.winfo_screenwidth()
screen_h = window.winfo_screenheight()

window_x = int((screen_w/2) - (ww/2))
window_y = int((screen_h/2) - (wh/2))

window.geometry(f"{ww}x{wh}+{window_x}+{window_y}")
window.mainloop()