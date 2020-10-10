# -*- coding: utf-8 -*-
"""
Created on Sat Oct 10 09:46:29 2020

@author: Nikita
"""

import queue
from collections import deque 
from scipy import sparse
import BitVector as biv
import numpy as np
import copy
import Node

class SearchAlgorithm:
    
    def __init__(self, sparseAdjacency = None):
        if ((sparseAdjacency is None) or 
            (type(sparseAdjacency) != sparse.lil_matrix)):
            print ("No adjacency matrix is currently used")
            sparseAdjacency = None
        else:
            self.sparseAdjacency = sparseAdjacency
            
        self.queue = queue.Queue()
        self.visited = None
        if (not (sparseAdjacency is None) and 
            not (type(sparseAdjacency) != sparse.lil_matrix)):
            shape = (sparse.lil_matrix(self.sparseAdjacency)).get_shape()
            self.visited = np.zeros(shape[0], dtype = bool)
        
    def setSparseAdjacencyMatrix(self, sparse):
        if (type(sparse) == sparse.lil_matrix):
            self.sparseAdjacency = copy.deepcopy(sparse)
    
    def BFS (self, startNode, endNode):
        self.visited[int(startNode.getNumber())] = True
        if ( int(startNode.getNumber()) == int(endNode.getNumber()) ):
            return startNode
        nonzero = sparse.find(self.sparseAdjacency[startNode.getNumber()])
        connections = nonzero[1]
        for connection in connections:
            if (self.visited[connection] == False):
                newNode = Node.Node(int(connection),startNode,startNode.getOriginDistance()+1)
                self.queue.put(newNode)
        if (not self.queue.empty()):
            return self.BFS(self.queue.get(),endNode)
            
            
        
        # if (self.visited[startNode] == False):
        #     transitions = self.sparseAdjacency[startNode]
        #     for element in transitions:
        #         self.queue.put(element[1])
        #     self.visited[startNode] = True;    
            
        
def main(test = 0):
  
    if (test == 0):
        print ("Run main as usual")
        
    elif(test == 1):
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
        matrix = np.array([[0,1,0],
                           [1,0,1],
                           [0,1,0]])
        
        sMatrix = sparse.lil_matrix(matrix)
        print(sMatrix)
        startNode = 2
        print ("\n")
        print (sMatrix[startNode])
        #for element in sMatrix[startNode]:
        #   print (element)
        print (sMatrix.get_shape())
        algo = SearchAlgorithm(sMatrix)
        
    elif (test == 3):
        matrix = np.array([[0,1,0],
                           [1,0,1],
                           [0,1,0]])
        
        sMatrix = sparse.lil_matrix(matrix)
        algo = SearchAlgorithm(sMatrix)
        beginNode = Node.Node(0,None,0)
        endNode = Node.Node(2,None,-1)
        final = algo.BFS(beginNode,endNode)
        while (final != None):
            print(final.getNumber())
            final = final.getParent()
            
        
if (__name__ == "__main__"):
    test = 3
    main(test)
    
    
