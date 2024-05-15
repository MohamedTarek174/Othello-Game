# Author : Mohamed Tarek Abdelsattar
# Date : 05-16-2024
# Othello is a classic board game played by two players.
# The game is played on an 8x8 grid board.
# Each player has disks that are typically black on one side and white on the other.
# The objective of the game is to have the majority of disks turned to display your color (black or white) by the end of the game.
# The Game uses Alpha-Beta Method (AI) to Generate the best solution for Meduim & Hard levels

import tkinter as tk
from Board import *
from Player import *
#Win - Draw - ShowValidMoves - IsValid

class Manger:
    def __init__(self, master ):
        self.master = master
        self.master.title("Othello")
        #Player is 1
        #PC     is 2
        self.user = Player(32,"b")
        self.PC = Player(32,"w")

        self.board = Board(master,self.user,self.PC)

def main():
    root = tk.Tk()
    app = Manger(root)
    root.mainloop()

if __name__ == "__main__":
    main()
