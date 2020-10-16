from tkinter import *
import random
import time
import numpy as np
from PIL import ImageTk,Image

BLUE_COLOR = "#0000FF"
GREY_COLOR = "#F0F0F0"
BLACK_COLOR = "#000000"

class LightsOn:
    def __init__(self,rows,cols,boardSize = 600):
        self.window = Tk()
        self.window.title("Lights On")
        self.rows = rows
        self.cols = cols
        self.rowh = boardSize/rows
        self.colh = boardSize/cols
        self.canvas = Canvas(self.window, width=boardSize, height=boardSize)
        self.canvas.pack()
        self.canvas.bind("<Button-1>",self.colorRect)
        self.lastX = 0
        self.lastY = 0
        self.x = 0
        self.y = 0
        self.boardSize = boardSize
        self.visited = np.zeros((rows*cols),dtype = bool)
        
    def getclick(self,eventorigin):
        self.x = eventorigin.x
        self.y = eventorigin.y
      
    def colorRect(self,eventorigin):
        self.getclick(eventorigin)
        r = self.x // self.rowh
        c = self.y // self.colh

        self.visited[int(r*self.rows+c)] = self.visited[int(r*self.rows+c)] ^ True
        x1 = r*self.rowh
        y1 = c*self.colh
        x2 = x1 + self.rowh
        y2 = y1 + self.colh

        if (self.visited[int(r*self.rows+c)]):
            self.canvas.create_rectangle(x1, y1, 
                                         x2, y2, 
                                         fill=BLUE_COLOR, 
                                         outline=BLACK_COLOR)
        else :
            self.canvas.create_rectangle(x1, y1, 
                                         x2, y2, 
                                         fill=GREY_COLOR, 
                                         outline=BLACK_COLOR)

    def eraseAll(self,eventorigin):
        

    def drawLines(self):
        self.board = []

        for i in range(self.rows):
            for j in range(self.cols):
                self.board.append((i, j))

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
            
window = LightsOn(9,9,600)
window.drawLines()
window.mainloop()
