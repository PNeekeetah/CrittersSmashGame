# -*- coding: utf-8 -*-
"""
Created on Wed Oct  7 19:02:07 2020

@author: Nikita
"""
import numpy as np
from random import randint

class GameBoard: 
    def __init__(self, size):
        self.size = size
        self.board = np.zeros((size+2,size+2), dtype = int)
        self.adjacentMatrix = np.zeros((size,size),dtype = int)
        self.leastDisturbanceMatrix = np.zeros((size,size),dtype = int)
    
    def printFullBoard(self):
        print (self.board)
    
    def printBoardState(self):
        print (self.board[1:self.size+1, 1:self.size+1])
    
    def printAdjacentBoardState(self):
        print(self.adjacentMatrix)
        
    def printLeastDisturbance(self):
        print(self.leastDisturbanceMatrix)
        
    def assignCritter(self,x_pos,y_pos):
        if ((x_pos >= 0) and (x_pos <= self.size-1) and 
        (y_pos >= 0) and (y_pos <= self.size-1)):
            self.board[x_pos+1,y_pos+1] = 1
        else:
            print( "Warning : Out Of Bounds Assignment")
    
    def whackUp(self, x_pos,y_pos):
        self.board[x_pos-1,y_pos] = self.board[x_pos-1,y_pos] ^ 1
        
    def whackDown(self, x_pos,y_pos):
        self.board[x_pos+1,y_pos] = self.board[x_pos+1,y_pos] ^ 1
        
    def whackLeft(self, x_pos,y_pos):
        self.board[x_pos,y_pos-1] = self.board[x_pos,y_pos-1] ^ 1
        
    def whackRight(self, x_pos,y_pos):
        self.board[x_pos,y_pos+1] = self.board[x_pos,y_pos+1] ^ 1
    
    def whackCenter (self, x_pos,y_pos):
        self.board[x_pos,y_pos] = self.board[x_pos,y_pos] ^ 1
    
        
    def whack(self, x_pos, y_pos):
        
        if(x_pos == 1) and (y_pos == 1): # Upper Left corner
            self.whackRight(x_pos,y_pos)
            self.whackDown(x_pos,y_pos)
            self.whackCenter(x_pos,y_pos)
            
        elif(x_pos == self.size) and (y_pos == self.size): # Lower Right Corner
            self.whackLeft(x_pos,y_pos)
            self.whackUp(x_pos,y_pos) 
            self.whackCenter(x_pos,y_pos)
    
        elif(x_pos == 1) and (y_pos == self.size): # Upper Right Corner
            self.whackLeft(x_pos,y_pos)
            self.whackDown(x_pos,y_pos)
            self.whackCenter(x_pos,y_pos)
        
        elif(x_pos == self.size) and (y_pos == 1): # Lower Left Corner
            self.whackRight(x_pos,y_pos)
            self.whackUp(x_pos,y_pos)
            self.whackCenter(x_pos,y_pos)
            
        elif (x_pos == 1):  # Upper Edge
            self.whackLeft(x_pos,y_pos)
            self.whackDown(x_pos,y_pos)
            self.whackRight(x_pos,y_pos)
            self.whackCenter(x_pos,y_pos)
            
        elif (x_pos == self.size): # Lower Edge
            self.whackLeft(x_pos,y_pos)
            self.whackUp(x_pos,y_pos)
            self.whackRight(x_pos,y_pos)
            self.whackCenter(x_pos,y_pos)
        
        elif (y_pos == 1):  # Left Edge
            self.whackDown(x_pos,y_pos)
            self.whackUp(x_pos,y_pos)
            self.whackRight(x_pos,y_pos)
            self.whackCenter(x_pos,y_pos)
        
        elif (y_pos == self.size): # Right Edge
            self.whackDown(x_pos,y_pos)
            self.whackUp(x_pos,y_pos)
            self.whackLeft(x_pos,y_pos)
            self.whackCenter(x_pos,y_pos)
        
        else: # Within Grid
            self.whackDown(x_pos,y_pos)
            self.whackUp(x_pos,y_pos)
            self.whackLeft(x_pos,y_pos)
            self.whackRight(x_pos,y_pos)
            self.whackCenter(x_pos,y_pos)
    
    def updateAdjacentMatrix(self, randomness = False):
        self.adjacentMatrix = np.zeros((self.size,self.size),dtype = int)
        for i in range (0,self.size):
            for j in range (0, self.size):
                self.adjacentMatrix[i,j] = (self.board[i+1,j+1] + 
                                            self.board[i+2,j+1]*2 +
                                            self.board[i+1,j+2]*2 + 
                                            self.board[i,j+1]*2 + 
                                            self.board[i+1,j]*2 +
                                            int (i+2 == self.size+1) +
                                            int (j+2 == self.size+1) +
                                            int (i == 0) +
                                            int (j == 0) + int(randomness)*randint(1,1000))*self.board[i+1,j+1]
                
    def updateLeastDisturbanceMatrix(self):
        self.leastDisturbanceMatrix = np.zeros((self.size,self.size),dtype = int)
        for i in range (0,self.size):
            for j in range (0, self.size):
                self.leastDisturbanceMatrix[i,j] = (self.board[i+1,j+1]*( 
                -int((self.board[i+2,j+1] == 0) * (i+2 != self.size+1)) +                                      # Down 
                -int((self.board[i+1,j+2] == 0) * (j+2 != self.size+1)) +                                      # Right
                -int((self.board[i,j+1] == 0) * (i != 0)) +                                        # Up              
                -int((self.board[i+1,j] == 0) * (j != 0)))                                         # Left
                - int(self.board[i+1,j+1] == 0)*6 )
                
    def findMaxHeuristicAdjacent (self, randomness = False):
        self.updateAdjacentMatrix(randomness)
        x = -1
        y = -1
        maxval = 0;
        for i in range (0,self.size):
            for j in range (0, self.size):
                if (self.adjacentMatrix[i,j] > maxval):
                    x = i;
                    y = j;
                    maxval = self.adjacentMatrix[i,j] 
        if ((x == -1) and (y == -1)):
            print ("Succesfully found solution")
        else:
            self.whack(x+1,y+1)
            self.updateAdjacentMatrix(randomness)

    def findMaxHeuristicLeastDisturbance(self):
        self.updateLeastDisturbanceMatrix()
        x = -1
        y = -1
        maxval = -6;
        for i in range (0,self.size):
            for j in range (0, self.size):
                if (self.leastDisturbanceMatrix[i,j] > maxval):
                    x = i;
                    y = j;
                    maxval = self.leastDisturbanceMatrix[i,j]
        if ((x == -1) and (y == -1)):
            print ("Succesfully found solution")
            return True
        else:
            self.whack(x+1,y+1)
            self.updateLeastDisturbanceMatrix()
            return False
            
    def boardCardinality(self):
        return np.count_nonzero(self.board) 
    


size = 9    
level0 = GameBoard(size)
level0.assignCritter(1,1)
level0.assignCritter(1,2)
level0.assignCritter(0,2)
level0.assignCritter(2,2)
level0.assignCritter(2,5)

checkFrequency = 2
check = checkFrequency
randomness = False
lastCardinality = level0.boardCardinality()
cardinality = level0.boardCardinality()
foundSolution = False
attempt = 0

while (not foundSolution):
    placeholder = level0;
    print ("Attempt " + str(attempt) + "\n")
    attempt+=1
    for i in range (0,10000):
        if randomness:
            foundSolution = placeholder.findMaxHeuristicAdjacent(randomness)
            randomness = False
        else:
            foundSolution = placeholder.findMaxHeuristicAdjacent()
        
        #print ("Step " + str(i) + "\n")
        #placeholder.printFullBoard()
        #print("\n")
        #placeholder.printBoardState()
        #print("\n")
        #placeholder.printAdjacentBoardState()
        #print("\n")
        check-=1
        if (check == 0):
            cardinality = placeholder.boardCardinality()
            if ((cardinality < lastCardinality + 4) and
                (cardinality > lastCardinality - 5)     ) :    
                randomness = True
            lastCardinality = cardinality
            check = checkFrequency
    placeholder.printFullBoard()        
            

