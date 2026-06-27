from tkinter import *
from tkinter import messagebox

root = Tk()
root.title("Tic Tac Toe")

current_player = "X"
board = [""] * 9

def check_winner():
    win_positions = [
        (0,1,2), (3,4,5), (6,7,8),
        (0,3,6), (1,4,7), (2,5,8),
        (0,4,8), (2,4,6)
    ]

    for a, b, c in win_positions:
        if board[a] == board[b] == board[c] != "":
            return board[a]

    if "" not in board:
        return "Draw"

    return None

def button_click(index):
    global current_player

    if board[index] == "":
        board[index] = current_player
        buttons[index].config(text=current_player)

        result = check_winner()

        if result == "Draw":
            messagebox.showinfo("Game Over", "It's a Draw!")
            reset_game()

        elif result:
            messagebox.showinfo("Winner", f"Player {result} Wins!")
            reset_game()

        else:
            current_player = "O" if current_player == "X" else "X"
            status.config(text=f"Player {current_player}'s Turn")

def reset_game():
    global current_player, board

    current_player = "X"
    board = [""] * 9

    for btn in buttons:
        btn.config(text="")

    status.config(text="Player X's Turn")

status = Label(root, text="Player X's Turn",
               font=("Arial", 14))
status.grid(row=0, column=0, columnspan=3, pady=10)

buttons = []

for i in range(9):
    btn = Button(root,
                 text="",
                 width=8,
                 height=4,
                 font=("Arial", 20),
                 command=lambda i=i: button_click(i))

    btn.grid(row=(i // 3) + 1,
             column=i % 3)

    buttons.append(btn)

reset_btn = Button(root,
                   text="Reset Game",
                   command=reset_game)

reset_btn.grid(row=4,
               column=0,
               columnspan=3,
               pady=10)

root.mainloop()