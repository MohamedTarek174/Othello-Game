import tkinter as tk
from Difficulty import *
from Board import *
from Player import *
import functions
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
