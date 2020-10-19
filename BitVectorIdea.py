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
import networkx as nx
import matplotlib.pyplot as plt


class BitBoard:
    totalBitBoards = 0
    
    """
    getCounter() is used to return the total number of
    boards that were created throughout program's lifetime
    """ 
    @staticmethod
    def getCounter():
        BitBoard.totalBitBoards += 1
        return BitBoard.totalBitBoards
    
    """
    The constructor takes in a size : int, createAdjacency : bool and a 
    createSparseAdjacency : bool. Based on these, it will either create
    an adjacency matrix of type lil_matrix, np.array, both or it won't
    create either.
    """
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
        
    """
    representBoardAsMatrix(self : BitBoard , 
                           bitBoard = None : BitVector, 
                           printBoard = False : bool )
    either takes the BitBoard's own BitVector or the BitVector passed as
    an argument and displays it as a matrix. The conversion from BitVector
    to matrix representation is done by filling the matrix from left to
    right, top to bottom with the elements from the BitVector. 
    
    For example, BitVector "0 0 0 0 0 0 0 0 1" converted to a matrix looks
    as follows :
        0 0 0
        0 0 0
        0 0 1
    The matrix representation is returned as an np.array
    """
    def representBoardAsMatrix(self, bitBoard = None, printBoard = False ):
        if (bitBoard is None):
            matrixRepr = np.zeros((self.size,self.size), dtype = np.int8)
            for i in range (0,self.size):
                for j in range(0,self.size):
                    matrixRepr[i,j] = self.board[self.size*i + j]
            if (printBoard):
                print (matrixRepr)
            return matrixRepr
        
        elif (type(bitBoard) is biv.BitVector):
            matrixRepr = np.zeros((self.size,self.size), dtype = np.int8)
            for i in range (0,self.size):
                for j in range(0,self.size):
                    matrixRepr[i,j] = bitBoard[self.size*i + j]
            if (printBoard):
                print (matrixRepr)
            return matrixRepr
            
    """
    assignCritterOnBoard(self : BitBoard, x_pos : int, y_pos : int) assigns a
    1 at the specified x,y coordinates if a 0 is present there currently, 
    otherwise it assigns a 0. 
    
    Used especially for setting up the initial state of the board
    """
    def assignCritterOnBoard(self, x_pos, y_pos):
        self.board[x_pos*self.size + y_pos] ^= 1
    
    """
    fillBoard(self : BitBoard , full : bool) either fills the board 
    completely with 1's or, if full = False, it fills the board over 
    the main diagonal with 1's.
    """
    def fillBoard (self, full = False):
        for i in range (0, self.size):
            if (full == False):
                for j in range (i, self.size):
                    self.assignCritterOnBoard(i,j)
            else:
                for j in range (0, self.size):
                    self.assignCritterOnBoard(i,j)
    
    """
    getBitBoard (self : BitVector) returns the current BitVector board.
    """
    def getBitBoard(self):
        return self.board
    
    """
    setBitBoard(self : BitBoard, board : BitVector) sets the BitVector
    board of the BitBoard.
    """
    def setBitBoard (self, board):
        self.board = board

    
    """
    getAdjacencyMatrix(self : BitBoard) returns the np.array() adjacency 
    matrix .   
    """
    def getAdjacencyMatrix(self):
        return self.adjacencyMatrix

    """
    getSparseAdjacencyMatrix(self : BitBoard) returns the sparse adjacency
    matrix.
    """
    def getSparseAdjacencyMatrix(self):
        return self.sparseAdjacencyMatrix
    
    """
    getBoardSize(self : BitBoard) returns the side "length" of the board
    """
    def getBoardSize(self):
        return self.size
    
    """
    printObjectSizeStatistics(self : BitBoard, other = None : BitBoard) prints
    statistics with regards to the size in MB of the object. If only 1 object
    is passed, it returns its size; if 2 objects are passed, it returns the ratio
    of self / other
    """
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
    
    """
    fillSparseAdjacencyMatrix(self : BitBoard ,debug = False : bool) is used
    as a test method to grasp the size difference between a filled sparse matrix
    and an empty one.
    """
    def fillSparseAdjacencyMatrix(self,debug = False):
        for i in range (0, 2**(self.size**2)):
            if (debug):
                print("Filling Row " + str(i))
            for j in range (i, 2**(self.size**2)):
                #if (debug):
                    #print("Filling Column " + str(j))
                self.sparseAdjacencyMatrix[i,j] = True
    
    """
    isWhackable(self : BitBoard ,x_pos : int,y_pos : int) returns whether
    it is possible to act upon the board spot located at x,y.
    """
    def isWhackable(self,x_pos,y_pos):
        bitPos = x_pos*self.size + y_pos
        return self.board[bitPos] == 1
                
    """
    orthogonalWhack(self : BitBoard ,x_pos : int,y_pos : int) will toggle
    the cells surrounding and including x,y in an orthogonal manner if possible.
    
    For example, if the state is 
    0 1 0
    1 1 1
    0 1 0
    then acting upon the cell at (1,1) yields
    0 0 0 
    0 0 0
    0 0 0
    """
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
    
    """
    diagonalWhack(self : BitBoard ,x_pos : int,y_pos : int) will toggle
    the cells surrounding and including x,y in a diagonal manner if possible.
    
    For example, if the state is 
    1 0 1
    0 1 0
    1 0 1
    then acting upon the cell at (1,1) yields
    0 0 0 
    0 0 0
    0 0 0
    """
    def diagonalWhack(self,x_pos,y_pos):
        bitPos = x_pos*self.size + y_pos
        upperLeftBound = (x_pos - 1)*self.size
        upperRightBound = x_pos*self.size 
        lowerLeftBound = (x_pos + 1)*self.size
        lowerRightBound = (x_pos + 2)*self.size 
        if (( 0 <= bitPos) and 
            ( bitPos < self.size**2)):
            if (self.board[bitPos] == 1 ):
                ul = bitPos - self.size - 1
                ur = bitPos - self.size + 1
                dl = bitPos + self.size - 1
                dr = bitPos + self.size + 1
                if (( 0 <= ul) and ( ul < self.size**2) and (ul >= upperLeftBound)):
                    self.board[ul] ^= 1
                if (( 0 <= ur) and ( ur < self.size**2) and (ur < upperRightBound)):
                    self.board[ur] ^= 1
                if (( 0 <= dl) and ( dl < self.size**2) and (dl >= lowerLeftBound)):
                    self.board[dl] ^= 1
                if (( 0 <= dr) and ( dr < self.size**2) and (dr < lowerRightBound)):
                    self.board[dr] ^= 1
                self.board[bitPos] ^= 1
    
    """
    countOnes(self : BitBoard) returns the total number of cells equal to 1
    """
    def countOnes(self):
        return sum(bit == 1 for bit in self.board)
    
    """
    findAllPossibleTransisitons(self : BitBoard ,diagonalWhack = True : bool)
    will first create a new folder " FoundTransitions " if possible.
    
    For each possible board configuration, every possible bit equal to 1 is 
    acted upon via either the "orthogonalWhack" or "diagonalWhack" method. The
    sparse adjacency matrix is filled accordingly with 1's when a transition
    between 2 states is possible
    
    All transitions that were found in this manner are saved, in the 
    " FoundTransitions " folder. These can be reloaded for added speed;
    It takes under a second to find all possible transitions for a 2x2 and a 3x3.
    but it takes 1 minute 50 for a 4x4.
    """            
    def findAllPossibleTransisitons(self,diagonalWhack = True):
        dirname = os.path.dirname(__file__)
        pathname = os.path.join(dirname,"FoundTransitions\ ")
        
        if (not os.path.exists(pathname)):
            os.mkdir(pathname)  
        
        if (not diagonalWhack):
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
        else:
            if ( not os.path.isfile(pathname+"diagonal"+str(self.size)+"x"+str(self.size)+"transitions.npz")):
            
                for i in range(2**(self.size**2)-1, -1,-1):
                    refBoard = biv.BitVector(intVal = i, size = self.size**2)
                    for j in range (0,self.size**2):
                        self.board = copy.deepcopy(refBoard)
                        coords = (j//self.size, j % self.size)                
                        self.diagonalWhack(coords[0],coords[1])
                        if (int(refBoard) != int(self.board)):
                            self.sparseAdjacencyMatrix[int(refBoard),int(self.board)] = True
                            
                            
                sparse.save_npz(pathname+"diagonal"+str(self.size)+"x"+str(self.size)+"transitions.npz",self.sparseAdjacencyMatrix.tocoo())
                file = open( pathname+"diagonal"+str(self.size)+"x"+str(self.size)+"transitions.txt" , "w")
                file.write( str(self.sparseAdjacencyMatrix) )
                file.close()
            else :
                try:
                    self.sparseAdjacencyMatrix = sparse.load_npz(pathname+"diagonal"+str(self.size)+"x"+str(self.size)+"transitions.npz")
                except IOError as error:
                    print ("File not readable for some reason")
             
"""
convertBoardToString(value : int,boardSize : int ,bitBoard : BitVector) returns
a string representation of the matrix. 

This can be used for small sized graphs to show the transitions from one state
to another.
"""        
def convertBoardToString(value,boardSize,bitBoard):
    bitValue =  biv.BitVector(intVal = value, size = boardSize**2)
    arrVal = BitBoard.representBoardAsMatrix(bitBoard,bitValue)
    strVal = ""
    for i in range (0,boardSize):
        if (i > 0):
            strVal += "\n"
        for j in range (0, boardSize):
            strVal += (str(arrVal[i,j]) + " ")
    return strVal

"""
createGraph(gameBoard : BitBoard, 
            allNodes : List of <Node>,
            highlightNode = None : Node, 
            displayNumber = False : bool , 
            reverse = False : bool) 
creates a graph based on the child-parent relationships found in the list "allNodes".
If a highlightNode is passed, said node is colored in pink on the graph.
If displayNumber is False, the nodes will be displayed as an NxN matrix of 1's and 0's
Otherwise, it is displayed as a number.
If reverse is true, the edges of the graph are reversed 

This method can be used with both full solution graphs or with individual solution graphs.
"""
def createGraph (gameBoard, allNodes,highlightNode = None, displayNumber = False , reverse = False) :
    graph = nx.DiGraph()
    boardSize = gameBoard.getBoardSize()
    color_map = []

    for node in allNodes:
        if (node.getNumber() == 0):    
            color_map.append('green')
        elif (not(highlightNode is None ) and (node == highlightNode)):
            color_map.append('pink')
        else: 
            color_map.append('blue')
        if (displayNumber):
            graph.add_node(node.getNumber());
        else:    
            strVal = convertBoardToString(node.getNumber(),boardSize,gameBoard)
            graph.add_node(strVal);
    
    for node in allNodes:
        if (not(node.getParent() is None)):
            edgelabel = sum (bit == 1 for bit in biv.BitVector(intVal =  node.getNumber() ^
                                                                node.getParent().getNumber())) 
            if (displayNumber):
                graph.add_edge(node.getNumber(),
                               node.getParent().getNumber(), l = edgelabel)
            else:
                graph.add_edge(convertBoardToString(node.getNumber(),boardSize,gameBoard)
                       ,convertBoardToString(node.getParent().getNumber(),boardSize,gameBoard),l = edgelabel)
    
    labels = nx.get_edge_attributes(graph,'l')
    position = nx.kamada_kawai_layout(graph)

    if (reverse):
        graph = nx.DiGraph.reverse(graph)
    
    if (displayNumber):
        nx.draw_kamada_kawai(graph, node_color=color_map, with_labels=True)
    else:
        nx.draw_kamada_kawai(graph, node_color=color_map, with_labels=True, node_size=2000)
    
    nx.draw_networkx_edge_labels(graph,position, edge_labels = labels)
    plt.show()
    
        
"""
The main function contains several tests that showcase the several functions
that are available in the BitVector class as well as the non-class specific 
functions that deal with graphs and representations.
"""    
def main(test = 0):
    
    if (test == 0):
        print ("Execute main as usual")
        lvl0 = BitBoard(2)

    if (test == 1):
        print("====================== This is the size comparison test ======================")
        lvl0 = BitBoard(2, True, True)  
        lvl1 = BitBoard(4, True, True)    
        lvl0.printObjectSizeStatistics()
        lvl1.printObjectSizeStatistics()
        
    elif(test == 2):
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
        print("====================== This is the board representation test ======================")
        lvl0 = BitBoard(5,False,False)
        lvl0.fillBoard()
        print ("Board as a bool matrix : ")
        lvl0.representBoardAsMatrix()
        print ("Board as a 1D bit vector : ")
        print (lvl0.getBitBoard())
    
    elif (test == 4):
        print("====================== This is a test for the board whacking function ======================")
        size = 3
        lvl0 = BitBoard (size, False, False)
        lvl0.fillBoard(full = True)
        for i in range (0,size):
            for j in range (0,size):
                print ("\n Whack at " + str( (i,j) ) +"\n")
                placeholder = copy.deepcopy(lvl0)
                placeholder.orthogonalWhack(i,j)
                print (placeholder.representBoardAsMatrix())
                placeholder.representBoardAsMatrix()
        placeholder = copy.deepcopy(lvl0)
        # None should change
        placeholder.orthogonalWhack(4,1) 
        print("Used to show that it doesn't work out of bounds \n")
        print(placeholder.representBoardAsMatrix())
        lvl0.orthogonalWhack(1,1)
        print("Used to show that it doesn't act on a bit that is 0 \n")
        print(lvl0.representBoardAsMatrix())
        lvl0.orthogonalWhack(1,1)
        print("\n")
        print(lvl0.representBoardAsMatrix())
        
    elif (test == 5):
        print("====================== This is a test for finding all possible transitions ======================")
        size = 4
        lvl0 = BitBoard(size,False,True)
        lvl0.findAllPossibleTransisitons()
    
    elif (test == 6):
        print("====================== This is a test for the BFS function ======================")
        size = 3
        lvl0 = BitBoard(size,False,True)
        lvl0.assignCritterOnBoard(0,0)
        lvl0.assignCritterOnBoard(1,0)
        lvl0.assignCritterOnBoard(0,2)
        lvl0.assignCritterOnBoard(2,1)
        print("Starting State : ")
        lvl0.representBoardAsMatrix()
        print("\n")
        lvl0.findAllPossibleTransisitons(diagonalWhack=False)
        search = SearchAlgorithm.SearchAlgorithm(lvl0.getSparseAdjacencyMatrix().tolil())
        startNode = Node.Node (int(lvl0.getBitBoard()))
        endNode = Node.Node (0)
        fin = search.BFS(startNode,endNode)
        solution = fin[1]
        step = len(solution)-1
        if (len(solution) == 0):
            print("This has no solution")
            
        while (0 < step):
            print("Step: " + str(step))
            lvl0.representBoardAsMatrix(biv.BitVector( intVal = solution[step].getNumber(), size = lvl0.getBoardSize()**2),
                                              printBoard=True)
            print("\n")
            step-=1
            
    elif (test == 7):
        print("====================== This is a test for the reverse BFS function paired with orthogonal whacking ======================")
        size = 4
        lvl0 = BitBoard(size,False,True)
        lvl0.assignCritterOnBoard(2,2);
        lvl0.assignCritterOnBoard(1,3);
        lvl0.assignCritterOnBoard(1,1);
        lvl0.findAllPossibleTransisitons(diagonalWhack=False)
        search = SearchAlgorithm.SearchAlgorithm(lvl0.getSparseAdjacencyMatrix().tolil())
        startNode = Node.Node(45019) # starting from node Node.Node(1) fails
        endNode = Node.Node(0)
        highlightNode = Node.Node(int(lvl0.getBitBoard()))
        allNodes = search.reverseBFS(endNode)
        path = search.BFS(startNode,endNode)
        if (size < 4):
            createGraph(lvl0,allNodes,highlightNode,True)   
        
        if (len(path[1]) > 0):
            createGraph(lvl0,path[1],startNode,False,reverse = True)   
        
        print ("The number acceptable solutions is :" + str(len(allNodes)) + 
               " out of the possible " + str(2**(lvl0.getBoardSize()**2)))
    
    elif (test == 8):
        print("====================== This is a test for the reverse BFS function paired with diagonal whacking ======================")
        size = 3
        lvl0 = BitBoard(size,False,True)
        lvl0.assignCritterOnBoard(2,2);
        lvl0.assignCritterOnBoard(1,3);
        lvl0.assignCritterOnBoard(1,1);
        lvl0.findAllPossibleTransisitons(diagonalWhack=True)
        search = SearchAlgorithm.SearchAlgorithm(lvl0.getSparseAdjacencyMatrix().tolil())
        endNode = Node.Node(0)
        highlightNode = Node.Node(int(lvl0.getBitBoard()))
        allNodes = search.reverseBFS(endNode)
        if (size < 4):
            createGraph(lvl0,allNodes,highlightNode,False)   
        print ("The number acceptable solutions is :" + str(len(allNodes)) + 
               " out of the possible " + str(2**(lvl0.getBoardSize()**2)))
    
    elif (test == 9):
        size = 3
        lvl0 = BitBoard(size,False,False)
        lvl0.assignCritterOnBoard(2,2);
        lvl0.assignCritterOnBoard(1,3);
        lvl0.assignCritterOnBoard(1,1);
        search = SearchAlgorithm.SearchAlgorithm()
        currentNode = Node.Node(0)
        path = search.greedySearch( currentNode, lvl0, iterations = 500 )
        print (path)
        
if __name__ == "__main__":
    print ("0 - Runs Main - *EMPTY*")
    print ("1 - Size Comparison test")
    print ("2 - Fill Size Comparison Test")
    print ("3 - Board Representation Test")
    print ("4 - Orthogonal Whack Test on a 4 x 4 board")
    print ("5 - Transitions test")
    print ("6 - Search Test")
    print ("7 - Find all possible sollutions for a 4 x 4 board and attempt"
           + " to find path from node 45019")
    print ("8 - Find all possible solutions for a 3 x 3 board using the" 
           + " diagonal whack and highligh starting point")
    print ("9 - Greedy search algorithm for path - *NOT FUNCTIONAL* ")
    test = int(input())
    main(test)



