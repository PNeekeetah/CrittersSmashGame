"""
Date : 19.10.2020

@author: Nikita Popescu
"""

from tkinter import *
import numpy as np
from BitVectorIdea import BitBoard
import BitVector as biv
import Node 
import SearchAlgorithm
import time


BLUE_COLOR = "#ADD8E6"
GREY_COLOR = "#F0F0F0"
BLACK_COLOR = "#000000"
RED_COLOR = "#FA8072"

class LightsOn:
    """
    Constructor (self : LightsOn, size : int, boardSize = 600 : int) takes
    in a size and creates a size x size board. 
    """
    def __init__(self,size,boardSize = 600 ):
        self.window = Tk()
        self.window.title("Lights On")
        self.canvas = Canvas(self.window, width=boardSize, height=boardSize)
        self.canvas.pack()
        self.canvas.bind("<Button-1>",self.colorRect)
        self.canvas.bind("<Button-3>",self.eraseAll)
        self.window.bind("<Key>",self.key_handler)
        self.x = 0
        self.y = 0
        self.size = size
        self.rows = size
        self.cols = size
        self.rowh = boardSize/size
        self.colh = boardSize/size
        self.boardSize = boardSize
        self.orthogonal = True
        if (size <= 4):
            self.level = BitBoard(size,False,True)
            BitBoard.findAllPossibleTransisitons(self.level)
        else:
            self.level = BitBoard(size,False,False)            
        self.playMode = False
        print("Press 'I' for more information.")
    
    """
    key_handler(self : LightsOn, eventorigin) handles key strokes.
    
    """
    def key_handler(self, eventorigin):
        if ((eventorigin.char == "i") or (eventorigin.char == "I")):
            self.showTutorial()
        elif ((eventorigin.char == "p") or (eventorigin.char == "P")):
            self.goToPlayMode()
        elif (((eventorigin.char == "x") or (eventorigin.char == "X")) and
              self.playMode == False):
            self.toggleCross()
        elif (((eventorigin.char == "s") or (eventorigin.char == "S")) and
              self.playMode == True):
            self.showSolution()
    
    """
    toggleCross(self : LightsOn) switches between using the orthogonal
    whacking and the diagonal whacking routines.
    """
    def toggleCross(self):
        self.orthogonal ^= True
        self.updateBoard()
    
    """
    showTutorial(self : LightsOn) shows a brief tutorial on how to
    interact with the game.
    """
    def showTutorial(self):
        messagebox.showinfo( "Instructions", 
        """
        Left Click on any square on the grid to color 
        Right Click anywhere on the grid to erase it
        Press "I" to bring up this dialog box
        Press "P" to start Play Mode
        Press "X" to toggle between Orthogonal switch or Cross switch
        Press "S" to show the solution from the current state of the board.
        Once "Play Mode" is active, you cannot use "X" anymore
        In "Play Mode", blue is used to indicate that the orthogonally 
        adjacent squares get toggled, whereas red is used to indicate that
        the diagonal squares get toggled.
        If a solution exists, it will be shown in green.
        If the solution doesn't exist, the squares will flash black and Play Mode
        is quit automatically
        """)
    
    """
    showSolution(self : LightsOn) calls the BFS() method and displays the solution
    step by step by flashing green squares for each individual step of the solution
    or it flashes black squares if a solution doesn't exist. Play Mode is quit if 
    no solution exists.
    """
    def showSolution(self):
        print ("Showing solution")
        self.playMode = False
        self.level.findAllPossibleTransisitons(diagonalWhack= (not self.orthogonal))
        search = SearchAlgorithm.SearchAlgorithm(self.level.getSparseAdjacencyMatrix().tolil())
        startNode = Node.Node(int(self.level.getBitBoard())) # starting from node Node.Node(1) fails
        endNode = Node.Node(0)
        path = search.BFS(startNode,endNode)
        auxBoard = self.level.getBitBoard()
        if (path[0] == False):
            board = biv.BitVector(intVal = 0,size = self.size**2 )
            lastBoard = self.level.getBitBoard()
            self.flash(lastBoard,board,0.2,color = "#4c4c4c" )                    
            time.sleep(0.9)
            print("Done Showing Solution")
            self.level.setBitBoard(auxBoard)
            self.updateBoard()
            self.window.update()
        else:    
            for node in reversed(path[1]):
                board = biv.BitVector(intVal = node.getNumber(),size = self.size**2 )
                lastBoard = self.level.getBitBoard()
                time.sleep(1)
                self.flash(lastBoard,board,0.2)              
            
            time.sleep(0.9)
            print("Done Showing Solution")
            self.level.setBitBoard(auxBoard)
            self.updateBoard()
            self.window.update()
            self.playMode = True

    """
    goToPlayMode(self : LightsOn) switches Play Mode to true. In play mode,
    it is not possible to assign or erase squares.
    """
    def goToPlayMode(self):
        self.playMode = True
    
    """
    getClick(self : LightsOn, eventorigin) gets the x and y position of the 
    mouse click within the canvas.
    """
    def getclick(self,eventorigin):
        self.x = eventorigin.x
        self.y = eventorigin.y

    """
    colorRect (self : LightsOn, eventorigin) either colors 1 rectangle at 
    the origin of the click if in play mode or it runs the diagonalWhack/
    orthogonalWhack if within Play Mode.
    """
    def colorRect(self,eventorigin):
        self.getclick(eventorigin)
        r = int (self.x // self.rowh)
        c = int (self.y // self.colh)
        if (self.playMode == False):
            self.level.assignCritterOnBoard(r,c)
        else:
            if (self.orthogonal):
                self.level.orthogonalWhack(r,c)
            else:
                self.level.diagonalWhack(r,c)
        
        self.updateBoard()
        #print (self.level.getBitBoard())
    
    """
    flash(self : LightsOn, 
          lastState : BitVector, 
          currentState : BitVector, 
          duration = 0.2 : float, 
          color = "#98FB98" : string)
    toggles between 2 board states to show the difference between them. Flashing
    takes 5*2*duration seconds overall. Flashing is done using the color specified 
    in "color".
    """    
    def flash (self, lastState, currentState, duration = 0.2, color = "#98FB98"):
        for i in range (5):
            self.level.setBitBoard(lastState)
            self.updateBoard(color)
            self.window.update()
            time.sleep(duration)
            self.level.setBitBoard(currentState)
            self.updateBoard(color)
            self.window.update()
            time.sleep(duration)
    
    """
    updateBoard (self : LightsOn, color = None : string) iterates through all
    the cells of the board and updates each one accordingingly. 0's are represented
    as grey cells, 1's are represented either via red or blue squares, depending 
    on the game mode. 
    If all cells are 0, an end game prompt is called.
    """
    def updateBoard (self, color = None):
        bitBoard = self.level.getBitBoard()
        for i in range (self.size**2):
            r = i//self.size
            c = i%self.size
            x1 = r*self.rowh
            y1 = c*self.colh
            x2 = x1 + self.rowh
            y2 = y1 + self.colh
            if (bitBoard[r*self.rows+c] == 1):
                if (color is None ):
                    if (self.orthogonal):
                        self.canvas.create_rectangle(x1, y1, 
                                                 x2, y2, 
                                                 fill=BLUE_COLOR, 
                                                 outline=BLACK_COLOR)
                    else :
                        self.canvas.create_rectangle(x1, y1, 
                                                 x2, y2, 
                                                 fill=RED_COLOR, 
                                                 outline=BLACK_COLOR)
                else:
                    self.canvas.create_rectangle(x1, y1, 
                                                 x2, y2, 
                                                 fill=color, 
                                                 outline=BLACK_COLOR)
            else:
                self.canvas.create_rectangle(x1, y1, 
                                     x2, y2, 
                                     fill=GREY_COLOR, 
                                     outline=BLACK_COLOR)
        if (int(bitBoard) == 0):
            if (self.playMode):
                self.endgame()
    
    """
    endgame (self : LightsOn) shows an end game prompt and it switches play
    mode to false.
    """
    def endgame (self):
        if (self.playMode == True):
            messagebox.showinfo( "Endgame", 
            """You won""")
            self.playMode = False

    """
    eraseAll (self : LightsOn, eventorigin) will make all squares grey and
    it will assign 0 to all cells of the board
    """
    def eraseAll(self,eventorigin):
        if (self.playMode == False):
            bitBoard = self.level.getBitBoard()
            for i in range(self.rows):
                for j in range(self.cols):
                    if (bitBoard[i*self.rows+j] == 1):
                        self.level.assignCritterOnBoard(i,j)
                    x1 = i*self.rowh
                    y1 = j*self.colh
                    x2 = x1 + self.rowh
                    y2 = y1 + self.colh
                    self.canvas.create_rectangle(x1, y1, 
                                             x2, y2, 
                                             fill=GREY_COLOR, 
                                             outline=BLACK_COLOR)
            #print (self.level.getBitBoard())
    
    """
    drawLines(self : LightsOn) draws horizontal and vertical lines that
    delimit the positions of the cells. The lines are there solely as 
    a visual aid.
    """
    def drawLines(self):
        for i in range(self.rows+1):
            self.canvas.create_line(i * self.boardSize / self.rows, 
                                    0, 
                                    i * self.boardSize / self.rows, 
                                    self.boardSize)

        for i in range(self.cols+1):
            self.canvas.create_line(0, 
                                    i * self.boardSize / self.cols, 
                                    self.boardSize, 
                                    i * self.boardSize / self.cols)
    
    """
    mainloop( self: LightsOn) is the game loop.
    """
    def mainloop(self):
        while True:
            self.window.update()
            
window = LightsOn(4,1000)
window.drawLines()
window.mainloop()
