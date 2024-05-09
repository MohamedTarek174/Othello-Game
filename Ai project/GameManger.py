import tkinter as tk
from Difficulty import *
from Board import *
from Player import *

class Manger:
    def __init__(self, master , difficulty_level):
        self.master = master
        self.master.title("Othello")
        self.game = DifficultyFactory.create_difficulty(difficulty_level)
        self.user = Player(32,1)
        self.user.symbol ="x"
        self.PC = Player(32,2)
        self.PC.symbol ="y"

        self.board = Board(master,self.game,self.user,self.PC)

def main():
    root = tk.Tk()
    difficulty_level = "easy"
    app = Manger(root,difficulty_level)
    root.mainloop()

if __name__ == "__main__":
    main()
