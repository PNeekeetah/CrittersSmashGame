from tkinter import *
import numpy as np
from BitVectorIdea import BitBoard
import BitVector as biv


BLUE_COLOR = "#ADD8E6"
GREY_COLOR = "#F0F0F0"
BLACK_COLOR = "#000000"
RED_COLOR = "#FA8072"

class LightsOn:
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
        #self.visited = np.zeros((rows*cols),dtype = bool)
        if (size <= 4):
            self.level = BitBoard(size,False,True)
            BitBoard.findAllPossibleTransisitons(self.level)
        else:
            self.level = BitBoard(size,False,False)
            
        self.playMode = False
        print("Press 'I' for more information.")
        
    def key_handler(self, eventorigin):
        if ((eventorigin.char == "i") or (eventorigin.char == "I")):
            self.showTutorial()
        elif ((eventorigin.char == "p") or (eventorigin.char == "P")):
            self.goToPlayMode()
        elif (((eventorigin.char == "x") or (eventorigin.char == "X")) and
              self.playMode == False):
            self.toggleCross()
            
    def toggleCross(self):
        self.orthogonal ^= True
    
    def showTutorial(self):
        messagebox.showinfo( "Instructions", 
        """
        Left Click on any square on the grid to color 
        Right Click anywhere on the grid to erase it
        Press "I" to bring up this dialog box
        Press "P" to start Play Mode
        Press "X" to toggle between Orthogonal switch or Cross switch
        Once "Play Mode" is active, you cannot use "X" anymore
        In "Play Mode", blue is used to indicate that the orthogonally 
        adjacent squares get toggled, whereas red is used to indicate that
        the diagonal squares get toggled.
        """)
     
    def goToPlayMode(self):
        self.playMode = True
        
    def getclick(self,eventorigin):
        self.x = eventorigin.x
        self.y = eventorigin.y
      
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
        print (self.level.getBitBoard())
        
        
    def updateBoard (self):
        bitBoard = self.level.getBitBoard()
        for i in range (self.size**2):
            r = i//self.size
            c = i%self.size
            x1 = r*self.rowh
            y1 = c*self.colh
            x2 = x1 + self.rowh
            y2 = y1 + self.colh
            if (bitBoard[r*self.rows+c] == 1):
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
                                     fill=GREY_COLOR, 
                                     outline=BLACK_COLOR)
        if (int(bitBoard) == 0):
            self.endgame()
            
    def endgame (self):
        if (self.playMode == True):
            messagebox.showinfo( "Endgame", 
            """You won""")
            self.playMode = False

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
            
    def mainloop(self):
        while True:
            self.window.update()
            
window = LightsOn(3,1000)
window.drawLines()
window.mainloop()
