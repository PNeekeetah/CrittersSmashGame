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
        self.nodesThatReachEnd = []
        if ((sparseAdjacency is None) or 
            (type(sparseAdjacency) != sparse.lil_matrix)):
            print ("No adjacency matrix is currently used")
            sparseAdjacency = None
        else:
            self.sparseAdjacency = sparseAdjacency
            
        self.adjacencyIsTransposed = False
            
        #self.queue = queue.Queue()
        """
        if (not (sparseAdjacency is None) and 
            not (type(sparseAdjacency) != sparse.lil_matrix)):
            shape = (sparse.lil_matrix(self.sparseAdjacency)).get_shape()
            self.visited = np.zeros(shape[0], dtype = bool)
        """
    def setSparseAdjacencyMatrix(self, sparse):
        if (type(sparse) == sparse.lil_matrix):
            self.sparseAdjacency = copy.deepcopy(sparse)

    def transposeAdjacency (self):
        if (isinstance(self.sparseAdjacency, sparse.lil_matrix)):
            self.sparseAdjacency = self.sparseAdjacency.transpose()
            self.adjacencyIsTransposed = self.adjacencyIsTransposed ^ True;
        else:
            print ("No matrix to invert")
            
    """
    def BFS (self, startNode, endNode):
        #print("Distance from origin is : " + str(startNode.getOriginDistance()) )        
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
        else:
            return None        
    """
    
    # If there exists a path between start and finish, returns true + path    
    def BFS (self, startNode, endNode):
        shape = (sparse.lil_matrix(self.sparseAdjacency)).get_shape()
        visited = np.zeros(shape[0], dtype = bool)
        waiting = queue.Queue()
        waiting.put(startNode)
        path = []
        while (not waiting.empty()):        
            currentNode = waiting.get()

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
                    waiting.put(newNode)            
            visited[int(currentNode.getNumber())] = True
        return (False, [])
    
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
    
    def getAllNodesThatReachEnd(self):
        return self.nodesThatReachEnd
        
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
        beginNode = Node.Node(0)
        endNode = Node.Node(2)
        final = algo.BFS(beginNode,endNode)
        for node in final[1]:
            print("Node " + str(node.getNumber()))
            
        
if (__name__ == "__main__"):
    test = 3
    main(test)
    
    
