import tkinter as tk
import tkinter.messagebox
from Difficulty import *
import sys
import Player
import time
from math import *
#Check Final result for:
    #NO more moves even the board is not full
    #The board is full
#AlphaBeta


convert = []
class Board:
    def __init__(self, master ,user,pc):
        self.master = master
        self.user = user
        self.pc = pc


        self.master.title("Othello")
        self.canvas = tk.Canvas(master, width=400, height=400, bg="green")
        self.canvas.pack()
        self.board_size = 8
        self.draw_board()
        self.canvas.bind("<Button-1>", self.on_click)
        self.place_oval(3,3,self.user.symbol)
        self.place_oval(4,4,self.user.symbol)
        self.place_oval(3,4,self.pc.symbol)
        self.place_oval(4,3,self.pc.symbol)

        self.showValidMoves()
#-----------------------------------------------------------------------
    def draw_board(self):
        self.board = [[0]*self.board_size for _ in range(self.board_size)] # Initialize the board
        for i in range(self.board_size):
            for j in range(self.board_size):
                x0 = i * 50
                y0 = j * 50
                x1 = x0 + 50
                y1 = y0 + 50
                self.canvas.create_rectangle(x0, y0, x1, y1, fill="green")
#-----------------------------------------------------------------------
    def on_click(self, event):
        global convert
        usercol = event.x // 50  
        userrow = event.y // 50
        #User Turn
        if self.valid_move(userrow,usercol,1):
            self.board[userrow][usercol] = 1
            x0 = usercol * 50 + 5  
            y0 = userrow * 50 + 5  
            x1 = x0 + 40
            y1 = y0 + 40
            self.canvas.create_oval(x0, y0, x1, y1,fill="black")
            self.make_line(convert,1)

      
        
        self.clearValidMoves()#Clear the Highlighted ovals that valid to the user

        #PC Turn
        pcrow,pccolm = self.create_difficulty("easy")        
        #If no Valid moves
        if pcrow == None or pcrow == None:
            self.GameOver()
            return 
        self.board[pcrow][pccolm] = 2
        x0 = pccolm * 50 + 5  
        y0 = pcrow * 50 + 5  
        x1 = x0 + 40
        y1 = y0 + 40
        self.canvas.create_oval(x0, y0, x1, y1,fill="white")
        self.make_line(convert,2)
        
        self.GameOver()
        

        self.showValidMoves()
#-----------------------------------------------------------------------
    def place_oval(self,row , col,symbol):
        if 0 <= col < self.board_size and 0 <= row < self.board_size and self.board[row][col] == 0:
            if(self.board[row][col] == 0):
                if symbol =="b":
                    self.board[row][col] = 1 
                else: # w
                    self.board[row][col] = 2
                self.user.Decrement_Disks()#decrement num of disks for player
                x0 = col * 50 + 5  
                y0 = row * 50 + 5  
                x1 = x0 + 40
                y1 = y0 + 40
                if symbol =="b":
                    self.canvas.create_oval(x0, y0, x1, y1, fill="black")  
                elif symbol == "w":
                    self.canvas.create_oval(x0, y0, x1, y1, fill="white")
                print(self.board)
                print()
#-----------------------------------------------------------------------
    # def checkZeros(self):#Check if the game is finished when board full
    #     for i in range(self.board_size):
    #         for j in range(self.board_size):
    #             if self.board[i][j] == 0:
    #                 return True
    #     return False #Board is full
#-----------------------------------------------------------------------
    def finalResult(self):#Contain Draw and Winner (NOT nessecery to be Full)
        sum = 0
        sum_1 = 0
        sum_2 = 0
        for i in range(self.board_size):
            for j in range(self.board_size):
                if self.board[i][j] != 0:
                    sum+=1
                    if self.board[i][j] == 1 :
                        sum_1+=1

                    if self.board[i][j] == 2 :
                        sum_1+=2    
        if sum_1 == sum_2: #Draw Case
            return 0
        else :
            return 1 if sum_1 > sum_2 else 2 
#-----------------------------------------------------------------------
    def valid_move(self, x, y, playernum):
        global convert
        oppenentnum = 2 if playernum == 1 else 1
        if  self.board[x][y] != 0:
            return False
        convert = [] #Make sure its empty

        neighbor = [(0, 1), (0, -1), (1, 0), (-1, 0)]#Just right left Up down
        for direction in neighbor:
            convert.clear()
            rows = x + direction[0] 
            cols = y + direction[1]
            if  (rows not in range(self.board_size) or cols not in range(self.board_size)):
                continue
            if self.board[rows][cols] != oppenentnum:
                continue
            convert.append((rows, cols))#Add the valid moves
            rows += direction[0]
            cols += direction[1]
            while (rows in range(self.board_size) and cols in range(self.board_size)):
                if self.board[rows][cols] == 0:
                    convert.clear()
                    break
                if self.board[rows][cols] == playernum:
                    return True
                convert.append((rows, cols))#Add the valid moves for user
                rows += direction[0]
                cols += direction[1]
        return False
#-----------------------------------------------------------------------
    def make_line(self, convertedList,playernum):
        # oppenentnum = 2 if playernum == 1 else 1
        for cell in convertedList:
            self.board[cell[0]][cell[1]] = playernum
            x0 = cell[1] * 50 + 5  
            y0 = cell[0] * 50 + 5  
            x1 = x0 + 40
            y1 = y0 + 40

            self.canvas.create_oval(x0, y0, x1, y1,fill="black" if playernum == 1 else "white")
#-----------------------------------------------------------------------
    def Availabe_moves(self,playernum):
        availablemoves = []
        for x in range(self.board_size):
            for y in range(self.board_size):
                if self.valid_move(x, y,playernum):
                    availablemoves.append((x, y))
        return availablemoves
#-----------------------------------------------------------------------
    def showValidMoves(self):
        Moves = self.Availabe_moves(1)
        for validmove in Moves:
            x0 = validmove[1] * 50 + 5  
            y0 = validmove[0] * 50 + 5  
            x1 = x0 + 40
            y1 = y0 + 40
            self.canvas.create_oval(x0, y0, x1, y1)
#-----------------------------------------------------------------------
    def clearValidMoves(self):
        for row in range(self.board_size):
            for col in range(self.board_size):
                if self.board[row][col] == 0:
                    x0 = col * 50
                    y0 = row * 50
                    x1 = x0 + 50
                    y1 = y0 + 50
                    self.canvas.create_rectangle(x0, y0, x1, y1,fill="green")              
#-----------------------------------------------------------------------
    def create_difficulty(self,level):
            if level == "easy":
                return self.easyMode()
            elif level == "medium":
                return Medium()
            elif level == "hard":
                return Hard()
#-----------------------------------------------------------------------
    def easyMode(self):
            empty_cells = []
            empty_cells = self.Availabe_moves(2)

            if empty_cells:
                x, y = random.choice(empty_cells)
                if self.valid_move(x, y, 2):
                    return x, y  
            else:#NO availabe moves for the PC
                return None, None  
#-----------------------------------------------------------------------
    def GameOver(self):
        list1 = self.Availabe_moves(1)
        list2 = self.Availabe_moves(2)

        if not list1 and not list2: #Means no more moves for both User and PC
            if self.finalResult == 1:
                # tkinter.messagebox.showinfo("Game Over", "It's a draw!")
                print("User Wins")
                sys.exit(0)
            elif self.finalResult == 2:
                # tkinter.messagebox.showinfo("Game Over", "It's a draw!")
                print("PC Wins")
                sys.exit(0)
            else:
                # tkinter.messagebox.showinfo("Game Over", "It's a draw!")
                print("Draw!!")
                sys.exit(0)

         