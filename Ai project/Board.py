import tkinter as tk
import tkinter.messagebox
import Player
import time
import random
from math import *

#AlphaBeta

depth = 0
convert = []

class Board:
    def __init__(self, master ,user,pc):
        self.master = master
        self.user = user
        self.pc = pc

        self.master.title("Othello")
        self.canvas = tk.Canvas(master, width=400, height=400, bg="white")#Original 400*400
        self.canvas.pack()
        
        # Show Score board
        self.score_frame = tk.Frame(master, width=400, height=50, bg="white")
        self.score_frame.pack(fill="both", expand=True)

        # Player Score
        self.player1_score_label = tk.Label(self.score_frame, text="User : 2", font=("Helvetica", 16))
        self.player1_score_label.pack(side="left", padx=10, pady=10)
        # PC Score
        self.player2_score_label = tk.Label(self.score_frame, text="PC : 2", font=("Helvetica", 16))
        self.player2_score_label.pack(side="right", padx=10, pady=10)
        
        self.board_size = 8
        self.draw_board()
        self.canvas.bind("<Button-1>", self.on_click)
        self.place_oval(3,3,self.user.symbol)
        self.place_oval(4,4,self.user.symbol)
        self.place_oval(3,4,self.pc.symbol)
        self.place_oval(4,3,self.pc.symbol)

        self.showValidMoves()#Show the first four availabe moves
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
                print()
#-----------------------------------------------------------------------
    def on_click(self, event):
        #------------------User Turn----------------------------------
        global convert
        usercol = event.x // 50  
        userrow = event.y // 50
        #User Turn
        if (not self.valid_move(userrow,usercol,1) and self.Availabe_moves):#not valid move even there are
            return
        
        if self.valid_move(userrow,usercol,1):
            self.board[userrow][usercol] = 1
            x0 = usercol * 50 + 5  
            y0 = userrow * 50 + 5   
            x1 = x0 + 40
            y1 = y0 + 40
            self.canvas.create_oval(x0, y0, x1, y1,fill="black")
            self.make_line(convert,1)
        
        #If user pick not available move and there are/is availabe move(s)

        NewUserScore = self.ScoreRecord(1)#It Calculate the new updated score after making a move
        NewPCScore = self.ScoreRecord(2)
        self.player1_score_label.config(text="User : " + str(NewUserScore))
        self.player2_score_label.config(text="PC : " + str(NewPCScore))


        #Clear the Highlighted ovals that valid to the user
        self.clearValidMoves()

        self.PC_move()
#-----------------------------------------------------------------------
    def PC_move(self):
        #------------------PC Turn----------------------------------
        pcrow,pccolm = self.create_difficulty("easy")      
        if pcrow == None or pcrow == None:#If no Valid moves
            self.GameOver()  
            #Show the Avialable moves again when no valid moves for PC and there are for user
            self.showValidMoves()
            return
         
        self.board[pcrow][pccolm] = 2
        x0 = pccolm * 50 + 5  
        y0 = pcrow * 50 + 5  
        x1 = x0 + 40
        y1 = y0 + 40
        self.canvas.create_oval(x0, y0, x1, y1,fill="white")
        self.make_line(convert,2)

        NewUserScore = self.ScoreRecord(1)#It Calculate the new updated score after making a move
        NewPcScore = self.ScoreRecord(2)  #It Calculate the new updated score after making a move

        self.player1_score_label.config(text="User : " + str(NewUserScore))
        self.player2_score_label.config(text="PC : " + str(NewPcScore))
        
        AMlist = self.Availabe_moves(1)
        if (not AMlist):#After PC move if no valid moves for User , return to PC and check for GameOver()
            self.PC_move()            

        
        self.GameOver()
        self.showValidMoves()
#-----------------------------------------------------------------------
    def valid_move(self, x, y, playernum):
        global convert
        tmpconvert = [] #Creating temp list contain the valid line(s) should be converted
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
            flag = True
            while (rows in range(self.board_size) and cols in range(self.board_size) and flag ):
                if self.board[rows][cols] == 0:
                    convert.clear()
                    break
                if self.board[rows][cols] == playernum:
                    tmpconvert.extend(convert)# Add 1 Valid line 
                    flag = False
                if(flag):
                    convert.append((rows, cols))#Add the valid moves for user
                    rows += direction[0]
                    cols += direction[1]
        convert = tmpconvert
        return False if not convert else True
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
            global depth
            if level == "easy":
                return self.easyMode()
            elif level == "medium":
                depth = 3
                return self.mediumMode()
            elif level == "hard":
                depth = 5
                return self.hardMode()
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
    def mediumMode(self):
        global depth
        alphabetaResult = self.alphaBeta(self.board,depth,-float("inf"),float("inf"),2)
        location = alphabetaResult[2]
        x = location[0]
        y = location[1]
        return x,y  
#-----------------------------------------------------------------------
    def hardMode(self):
        global depth
        alphabetaResult = self.alphaBeta(self.board,depth,-float("inf"),float("inf"),2)
        location = alphabetaResult[2]
        x = location[0]
        y = location[1]
        return x,y     
#-----------------------------------------------------------------------
    def alphaBeta(self,myboard,depth,alpha,beta,maximizing):
        Availbesboards = []
        choices = []

        for x in range(8):
            for y in range(8):
                if self.valid_move(x,y,2):
                    test = self.validBoard(2)
                    Availbesboards.append(test)#list of boards that each (solution of valid move)
                    choices.append([x,y])#valid points/move that make this possible solution

        if depth == 0 or len(choices) == 0:#no valid moves
            return (self.easyMode())

        if maximizing == 2:#Max the move for the PC
            v = -float("inf")
            bestBoard = []
            bestChoice = []
            for Avilabeboard in Availbesboards:#Check each possible board 
                boardValue = self.alphaBeta(Avilabeboard,depth-1,alpha,beta,1)#Call the new possible board to check Min
                if boardValue[0]>v:
                    v = boardValue[0]
                    bestBoard = Avilabeboard
                    bestChoice = choices[Availbesboards.index(Avilabeboard)]
                alpha = max(alpha,v)#Pick the Max value
                if beta <= alpha:
                    break
            return([v,bestBoard,bestChoice])
        else:#Min the move for the User
            v = float("inf")
            bestBoard = []
            bestChoice = []
            for Avilabeboard in Availbesboards:
                boardValue = self.alphaBeta(Avilabeboard,depth-1,alpha,beta,2)#Call the new possible board to check Max and so on...
                if boardValue[0]<v:
                    v = boardValue[0]
                    bestBoard = Avilabeboard
                    bestChoice = choices[Availbesboards.index(Avilabeboard)]
                beta = min(beta,v)#Pick the Min value
                if beta<=alpha:
                    break
            return([v,bestBoard,bestChoice])
#-----------------------------------------------------------------------
    def validBoard(self,playernum):
        tmpboard = self.board
        for cell in convert:
            tmpboard[cell[0]][cell[1]] = playernum
        return tmpboard
#-----------------------------------------------------------------------
    def finalResult(self):#Contain Draw and Winner (NOT nessecery to be Full)
        sum_1 = 0
        sum_2 = 0
        for i in range(self.board_size):
            for j in range(self.board_size):
                if self.board[i][j] != 0:
                    if self.board[i][j] == 1 :
                        sum_1+=1
                    elif self.board[i][j] == 2 :
                        sum_2+=1  



        if sum_1 == sum_2: #Draw Case
            return 0
        else :
            return 1 if sum_1 > sum_2 else 2 
#-----------------------------------------------------------------------
    def ScoreRecord(self,playernum):
        sum = 0
        for i in range(self.board_size):
            for j in range(self.board_size):
                if self.board[i][j] == playernum :
                    sum+=1
        return sum
#-----------------------------------------------------------------------
    def GameOver(self):
        list1 = self.Availabe_moves(1)
        list2 = self.Availabe_moves(2)

        if not list1 and not list2: #Means no more moves for both User and PC
            if self.finalResult() == 1:
                score = self.ScoreRecord(1)
                self.player1_score_label.config(text="User Wins with score " + str(score))
                self.player2_score_label.config(text="")

            elif self.finalResult() == 2:
                score = self.ScoreRecord(2)
                self.player1_score_label.config(text="PC Wins with score " + str(score))
                self.player2_score_label.config(text="")
            else:
                score = self.ScoreRecord(2)
                self.player1_score_label.config(text="Draw with score " + str(score))
                self.player2_score_label.config(text="")
#-----------------------------------------------------------------------
    # def checkZeros(self):#Check if the game is finished when board full
    #     for i in range(self.board_size):
    #         for j in range(self.board_size):
    #             if self.board[i][j] == 0:
    #                 return True
    #     return False #Board is full