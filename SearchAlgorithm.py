# -*- coding: utf-8 -*-
"""
Created on Sat Oct 10 09:46:29 2020

@author: Nikita Popescu
"""

import queue
from collections import deque 
from scipy import sparse
import BitVector as biv
import numpy as np
import copy
import Node
import random


class SearchAlgorithm:
    
    """
    Constructor(self: SearchAlgorithm, sparseAdjacency : sparse.lil_matrix) takes
    in a sparse matrix or nothing if one will be set later.
    """
    def __init__(self, sparseAdjacency = None):
        self.nodesThatReachEnd = []
        if ((sparseAdjacency is None) or 
            (type(sparseAdjacency) != sparse.lil_matrix)):
            print ("No adjacency matrix is currently used")
            sparseAdjacency = None
        else:
            self.sparseAdjacency = sparseAdjacency    
        self.adjacencyIsTransposed = False
    
    """
    setSparseAdjacencyMatrix(self : SearchAlgorithm, sparse : sparse.lil_matrix)
    takes a sparse matrix for use when performing a BFS or a reverse BFS
    """    
    def setSparseAdjacencyMatrix(self, sparse):
        if (type(sparse) == sparse.lil_matrix):
            self.sparseAdjacency = copy.deepcopy(sparse)

    """
    transposeAdjacency(self : SearchAlgorithm) is used to reverse the connections
    of the resulting graph. To reverse the connections, the adjacency matrix is 
    transposed.
    """
    def transposeAdjacency (self):
        if (isinstance(self.sparseAdjacency, sparse.lil_matrix)):
            self.sparseAdjacency = self.sparseAdjacency.transpose()
            self.adjacencyIsTransposed = self.adjacencyIsTransposed ^ True;
        else:
            print ("No matrix to invert")
            
    
    """
    BFS (self : SearchAlgorithm, startNode : Node, endNode : Node) takes in
    the starting node and the end node and returns a path that ties the 2.
    """
    def BFS (self, startNode, endNode):
        shape = (sparse.lil_matrix(self.sparseAdjacency)).get_shape()
        visited = np.zeros(shape[0], dtype = bool)
        waiting = deque()
        waiting.append(startNode)
        path = []
        currentNode = None
        while (len(waiting) > 0  ):        
            currentNode = waiting.popleft()

            # Check if current node is the last node
            if ( currentNode == endNode ):
                trace = currentNode
                while (not(trace is None)):
                    path.append(trace)
                    trace = trace.getParent()
                return (True, path)
            
            # Check all other nodes connected to this node
            nonzero = sparse.find(self.sparseAdjacency[currentNode.getNumber()])
            connections = nonzero[1]
            for connection in connections:
                if (visited[connection] == False):
                    newNode = Node.Node(int(connection))
                    newNode.setParent(currentNode)
                    # Check whether a similar node was added beforehand to queue
                    if (sum(node.getNumber() == newNode.getNumber() for node in waiting) == 0): 
                        waiting.append(newNode)
            visited[int(currentNode.getNumber())] = True
        print ("Total visited nodes until failure " + 
               str(sum(element == True for element in visited)) )
        return (False, path)
    """
    def greedySearch(self, currentNode, level, iterations = 500):
        path = []
        iteration = 0
        saveBoard = BitBoard.getBitBoard(level)
        size = BitBoard.getBoardSize(level)
        while (iteration < iterations):
            minBoard = BitBoard.getBitBoard(level)
            currBoard = BitBoard.getBitBoard(level)
            minLevel = size**2
            minCandidates = []
            for i in range (size**2):
                row = i // size
                col = i % size
                whackable = BitBoard.isWhackable(level, row, col)
                if (whackable):
                    BitBoard.orthogonalWhack(level,row,col)
                    totalOn = BitBoard.countOnes(level)
                    if (totalOn < minLevel ):
                        minCandidates.clear()
                        minBoard = BitBoard.getBitBoard(level)
                        minLevel = totalOn
                        saveRow = row
                        saveCol = col
                    if (totalOn == minLevel):
                        minCandidates.append(BitBoard.getBitBoard(level))
                    
                    BitBoard.setBitBoard(level,currBoard)
            
            totalMinCand = len(minCandidates)
            isInList = False
            if ( totalMinCand >= 1):
                potential = (minCandidates[random.randint(0, totalMinCand -1)])
                for conf in path:
                    if (potential == conf):
                        isInList = True
                if (not isInList):
                    path.append(potential)
                    
            BitBoard.setBitBoard(level,path[-1])
            iteration += 1
        return path
      """
        
    """
    reverseBFS (self : SearchAlgorithm, endNode : Node) finds all the nodes connected
    to endNode. A typical use case is to assign endNode as Node.Node(0) and then
    show all reachable states from there. 
    
    The list that is returned contains all solvable states  of the state space.
    """
    def reverseBFS (self, endNode):
        self.transposeAdjacency()
        shape = (sparse.lil_matrix(self.sparseAdjacency)).get_shape()
        visited = np.zeros(shape[0], dtype = bool)
        waiting = queue.Queue()
        waiting.put(endNode)
        while (not waiting.empty()):        
            currentNode = waiting.get()
            if (visited[int(currentNode.getNumber())] == True):
                continue
            # Check all nodes connected to this node
            nonzero = sparse.find(self.sparseAdjacency[currentNode.getNumber()])
            connections = nonzero[1]
            for connection in connections:
                if (visited[connection] == False):
                    newNode = Node.Node(int(connection))
                    currentNode.addChild(newNode)
                    newNode.setParent(currentNode)
                    waiting.put(newNode)            
            visited[int(currentNode.getNumber())] = True
            self.nodesThatReachEnd.append(currentNode)
        self.transposeAdjacency()
        return self.nodesThatReachEnd
    
    """
    getAllNodesThatReachEnd(self : SearchAlgorithm) returns all the nodes that
    reached the end if they were previously found.
    """
    def getAllNodesThatReachEnd(self):
        return self.nodesThatReachEnd
        
def main(test = 0):
  
    if (test == 0):
        print ("Run main as usual")
        
    elif(test == 1):
        print("Quick test for stack and queue functionality")
        Q = queue.Queue()
        S = deque()    
        size = 10
        for i in range (0,size):
            Q.put(i)
            S.append(i)
            
        print ("Queue")
        while (not Q.empty()):
            print(Q.get())
                    
        print ("Stack")
        while ( len(S) > 0):
            print(S.pop())        
    
    elif (test == 2):
        print ("Test for setting an adjacency matrix")
        matrix = np.array([[0,1,0],
                           [1,0,1],
                           [0,1,0]])
        
        sMatrix = sparse.lil_matrix(matrix)
        print(sMatrix)
        startNode = 2
        print ("\n")
        print ("Shows starting node connections")
        print (sMatrix[startNode])
        #for element in sMatrix[startNode]:
        #   print (element)
        print (sMatrix.get_shape())
        algo = SearchAlgorithm(sMatrix)
        
    elif (test == 3):
        print ("Quick test that shows the path between a Node with number 0 " + 
               " and a Node with number 2.")
        matrix = np.array([[0,1,0],
                           [1,0,1],
                           [0,1,0]])
        
        sMatrix = sparse.lil_matrix(matrix)
        algo = SearchAlgorithm(sMatrix)
        beginNode = Node.Node(0)
        endNode = Node.Node(2)
        final = algo.BFS(beginNode,endNode)
        for node in final[1]:
            print("Node " + str(node.getNumber()))
            
        
if (__name__ == "__main__"):
    test = 3
    main(test)
    
    
