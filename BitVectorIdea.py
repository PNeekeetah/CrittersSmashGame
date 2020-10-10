"""

"""
import numpy as np
import BitVector as biv
import time
import sys
from scipy import sparse
import copy
import os
import Node
import SearchAlgorithm
from collections import deque 


class BitBoard:
    totalBitBoards = 0
    
    # Used for ID-ing 
    @staticmethod
    def getCounter():
        BitBoard.totalBitBoards += 1
        return BitBoard.totalBitBoards
    
    def __init__(self, size, createAdjacency = False, createSparseAdjacency = True):
        self.size = size;
        self.board = biv.BitVector(size = size**2)
        if (createAdjacency):
            self.adjacencyMatrix = np.zeros((2**(size**2),2**(size**2)),dtype= bool)
        else :
            self.adjacencyMatrix = None
        if (createSparseAdjacency):
            self.sparseAdjacencyMatrix = sparse.lil_matrix((2**(size**2), 2**(size**2)),  
                                       dtype = bool)
        else:
            self.sparseAdjacencyMatrix = None
            
        self.ID = BitBoard.getCounter()
    
    # Takes a bit vector and shows it as a matrix
    def representBoardAsMatrix(self, bitBoard = None ):
        if (bitBoard is None):
            matrixRepr = np.zeros((self.size,self.size), dtype = bool)
            for i in range (0,self.size):
                for j in range(0,self.size):
                    matrixRepr[i,j] = self.board[self.size*i + j]
            print (matrixRepr)
            del matrixRepr
        elif (type(bitBoard) is biv.BitVector):
            matrixRepr = np.zeros((self.size,self.size), dtype = bool)
            for i in range (0,self.size):
                for j in range(0,self.size):
                    matrixRepr[i,j] = bitBoard[self.size*i + j]
            print (matrixRepr)
            del matrixRepr
    # Assign logic 1 at position x_pos, y_pos
    def assignCritterOnBoard(self, x_pos, y_pos):
        self.board[x_pos*self.size + y_pos] = 1
    
    # Test method that fills half or the entire bit vector
    def fillBoard (self, full = False):
        for i in range (0, self.size):
            if (full == False):
                for j in range (i, self.size):
                    self.assignCritterOnBoard(i,j)
            else:
                for j in range (0, self.size):
                    self.assignCritterOnBoard(i,j)
    
    # Getter for bit vector
    def getBitBoard(self):
        return self.board
    
    # Getter for Adjacency Matrix    
    def getAdjacencyMatrix(self):
        return self.adjacencyMatrix

    # Getter for Sparse Adjacency Matrix
    def getSparseAdjacencyMatrix(self):
        return self.sparseAdjacencyMatrix
    
    # Getter for size
    def getBoardSize(self):
        return self.size
    
    # Method for testing size
    def printObjectSizeStatistics(self, other = None):
        if ((other is None) or (not isinstance(other,BitBoard))):
            print("Object " +str(self.ID) + " has : " 
                  + str(sys.getsizeof(self)/1024**2) +" MB")
            print("Adjacency Matrix has : " + 
                  str(sys.getsizeof(self.adjacencyMatrix)/1024**2) + " MB")
            print("Sparse Adj Matrix has: " + 
                  str(sys.getsizeof(self.sparseAdjacencyMatrix)/1024**2) + " MB")
        else:
            print ("Object" +str(self.ID) +"/Object" + str(other.ID) +" is " + 
                   str(sys.getsizeof(self)/sys.getsizeof(other)))
            print ("AdjMatrix" +str(self.ID) +"/AdjMatrix" + str(other.ID) +" is " + 
                   str(sys.getsizeof(self.adjacencyMatrix)/sys.getsizeof(other.adjacencyMatrix)))
            print ("SparseAdjMatrx" +str(self.ID) +"/SparseAdjMatrix" + str(other.ID) +" is " + 
                   str(sys.getsizeof(self.sparseAdjacencyMatrix)/sys.getsizeof(other.sparseAdjacencyMatrix)))
    
    # Method for filling a sparse matrix
    def fillSparseAdjacencyMatrix(self,debug = False):
        for i in range (0, 2**(self.size**2)):
            if (debug):
                print("Filling Row " + str(i))
            for j in range (i, 2**(self.size**2)):
                #if (debug):
                    #print("Filling Column " + str(j))
                self.sparseAdjacencyMatrix[i,j] = True
                
    def orthogonalWhack(self,x_pos,y_pos):
        bitPos = x_pos*self.size + y_pos
        leftBound = (x_pos)*self.size
        rightBound = (x_pos + 1)*self.size
        if (( 0 <= bitPos) and 
            ( bitPos < self.size**2)):
            if (self.board[bitPos] == 1 ):
                left = bitPos - 1
                right = bitPos + 1
                up = bitPos - self.size
                down = bitPos + self.size
                if (( 0 <= left) and ( left < self.size**2) and (left >= leftBound)):
                    self.board[left] ^= 1
                if (( 0 <= right) and ( right < self.size**2) and (right < rightBound)):
                    self.board[right] ^= 1
                if (( 0 <= up) and ( up < self.size**2)):
                    self.board[up] ^= 1
                if (( 0 <= down) and ( down < self.size**2)):
                    self.board[down] ^= 1
                self.board[bitPos] ^= 1
                
    def findAllPossibleTransisitons(self):
        dirname = os.path.dirname(__file__)
        pathname = os.path.join(dirname,"FoundTransitions\ ")
        
        if (not os.path.exists(pathname)):
            os.mkdir(pathname)  
        
        if ( not os.path.isfile(pathname+str(self.size)+"x"+str(self.size)+"transitions.npz")):
        
            for i in range(2**(self.size**2)-1, -1,-1):
                refBoard = biv.BitVector(intVal = i, size = self.size**2)
                for j in range (0,self.size**2):
                    self.board = copy.deepcopy(refBoard)
                    coords = (j//self.size, j % self.size)                
                    self.orthogonalWhack(coords[0],coords[1])
                    if (int(refBoard) != int(self.board)):
                        self.sparseAdjacencyMatrix[int(refBoard),int(self.board)] = True
                        
                        
            sparse.save_npz(pathname+str(self.size)+"x"+str(self.size)+"transitions.npz",self.sparseAdjacencyMatrix.tocoo())
            file = open( pathname+str(self.size)+"x"+str(self.size)+"transitions.txt" , "w")
            file.write( str(self.sparseAdjacencyMatrix) )
            file.close()
        else :
            try:
                self.sparseAdjacencyMatrix = sparse.load_npz(pathname+str(self.size)+"x"+str(self.size)+"transitions.npz")
            except IOError as error:
                print ("File not readable for some reason")
        
def main(test = 0):
    
    if (test == 0):
        print ("Execute main as usual")
        lvl0 = BitBoard(2)

    if (test == 1):
        # This is the size comparison test
        print("====================== This is the size comparison test ======================")
        lvl0 = BitBoard(2, True, True)  
        lvl1 = BitBoard(4, True, True)    
        lvl0.printObjectSizeStatistics()
        lvl1.printObjectSizeStatistics()
        
    elif(test == 2):
        # This is the sparse matrix fill comparison test
        print("====================== This is the sparse matrix fill comparison test ======================")
        lvl0 = BitBoard(3, True, True)  
        lvl1 = BitBoard(3, True, True)
        lvl1.fillSparseAdjacencyMatrix()
        lvl1.printObjectSizeStatistics(lvl0)
        lvl1.printObjectSizeStatistics()
        print("====================== Matrix Contents ======================")
        print(lvl0.getSparseAdjacencyMatrix().toarray())
        print(lvl1.getSparseAdjacencyMatrix().toarray())
    
    elif (test == 3):
        #This is a matrix repr test
        print("====================== This is the board representation test ======================")
        lvl0 = BitBoard(5,False,False)
        lvl0.fillBoard()
        print ("Board as a bool matrix : ")
        lvl0.representBoardAsMatrix()
        print ("Board as a 1D bit vector : ")
        print (lvl0.getBitBoard())
    elif (test == 4):
        #This is a test for the whack function
        print("====================== This is a test for the board whacking function ======================")
        size = 4
        lvl0 = BitBoard (size, False, False)
        lvl0.fillBoard(full = True)
        for i in range (0,size):
            for j in range (0,size):
                placeholder = copy.deepcopy(lvl0)
                placeholder.orthogonalWhack(i,j)
                placeholder.representBoardAsMatrix()
                print ("\n")
        placeholder = copy.deepcopy(lvl0)
        # None should change
        placeholder.orthogonalWhack(4,1) 
        placeholder.representBoardAsMatrix()
        print("\n")
        lvl0.orthogonalWhack(1,1)
        lvl0.representBoardAsMatrix()
        print("\n")
        lvl0.orthogonalWhack(1,1)
        lvl0.representBoardAsMatrix()
    elif (test == 5):
        size = 4
        lvl0 = BitBoard(size,False,True)
        lvl0.findAllPossibleTransisitons()
    elif (test == 6):
        size = 3
        lvl0 = BitBoard(size,False,True)
        lvl0.assignCritterOnBoard(0,0)
        lvl0.assignCritterOnBoard(1,0)
        lvl0.assignCritterOnBoard(0,2)
        lvl0.assignCritterOnBoard(2,1)
        print("Starting State : ")
        lvl0.representBoardAsMatrix()
        print("\n")
        lvl0.findAllPossibleTransisitons()
        search = SearchAlgorithm.SearchAlgorithm(lvl0.getSparseAdjacencyMatrix().tolil())
        startNode = Node.Node (int(lvl0.getBitBoard()),None,0)
        endNode = Node.Node (0,None, -1)
        fin = search.BFS(startNode,endNode)
        solution = deque()
        step = 0
        lastSol = 0
        currSol = 0
        while (fin != None):
            solution.append(biv.BitVector(intVal = fin.getNumber(), size = (lvl0.getBoardSize())**2))
            fin = fin.getParent()
            
        if (len(solution) == 0):
            print("This has no solution")
            
        while (len(solution) != 0):
            print("Step: " + str(step))
            lvl0.representBoardAsMatrix(solution.pop())
            print("\n")
            step+=1

        
        
if __name__ == "__main__":
    print ("0 - Runs Main")
    print ("1 - Size Comparison test")
    print ("2 - Fill Size Comparison Test")
    print ("3 - Board Representation Test")
    print ("4 - Orthogonal Whack Test on a 4 x 4 board")
    print ("5 - Transitions test")
    print ("6 - Search Test")
    test = int(input())
    main(test)



#bv = biv.BitVector(intVal = 8)
#print (bv)

#for i in range (0, bv.size) :
#    print (bv[i])

