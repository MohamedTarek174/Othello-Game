import tkinter as tk
from Difficulty import *
class Board:
    def __init__(self, master , game ,user,pc):
        self.master = master
        self.game =game
        self.user = user
        self.pc = pc


        self.master.title("Othello")
        self.canvas = tk.Canvas(master, width=400, height=400, bg="green")
        self.canvas.pack()
        self.board_size = 8
        self.board = [[0]*self.board_size for _ in range(self.board_size)] # Initialize the board
        self.draw_board()
        self.canvas.bind("<Button-1>", self.on_click)


    def draw_board(self):
        for i in range(self.board_size):
            for j in range(self.board_size):
                x0 = i * 50
                y0 = j * 50
                x1 = x0 + 50
                y1 = y0 + 50
                self.canvas.create_rectangle(x0, y0, x1, y1, fill="green")

    def on_click(self, event):
        col = event.x // 50  
        row = event.y // 50 
        self.place_oval(row,col,self.user.symbol)
        x,y = self.game.play(self.board,self.pc)#pc turn
        self.place_oval(x,y,self.pc.symbol)


        
    def place_oval(self,row , col,symbol):
        if 0 <= col < self.board_size and 0 <= row < self.board_size and self.board[row][col] == 0:
            if(self.board[row][col]==0):
                if symbol =='x':
                    self.board[row][col] = 1 
                else:
                    self.board[row][col] = 2
                self.user.Decrement_Disks()#decrement num of disks for player
                x0 = col * 50 + 5  
                y0 = row * 50 + 5  
                x1 = x0 + 40
                y1 = y0 + 40
                if symbol =='x':
                    self.canvas.create_oval(x0, y0, x1, y1, fill="white")  
                else:
                    self.canvas.create_oval(x0, y0, x1, y1, fill="black")  
                print(self.board)
    