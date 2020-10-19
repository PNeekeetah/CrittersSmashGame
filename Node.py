# -*- coding: utf-8 -*-
"""
Created on Sat Oct 10 21:00:45 2020

@author: Nikita Popescu
"""

class Node:
    
    """
    Constructor (self : Node, number : int) assigns the object a number equal to
    number.
    """
    def __init__ (self, number):
        self.number = number
        self.parent = None
        self.children = []
    
    """
    getNumber(self : Node) returns the number assigned to this node
    """
    def getNumber(self):
        return self.number
    
    """
    getParent(self : Node) returns the node's parent
    """
    def getParent(self):
        return self.parent
    
    """
    setParent(self : Node, node : Node) sets "node" as the object's parent
    """
    def setParent (self, node):
        self.parent = node;
    
    """
    getChildren(self : Node) returns the children list of the node
    """
    def getChildren(self):
        return self.children
    
    """
    addChild( self : Node, child : Node) adds the node "child" to the children
    list of the object
    """
    def addChild (self, child):
        self.children.append(child)
    
    """
    Equality is determined based on whether the numbers are the same.
    """
    def __eq__ (self, other):
        if (isinstance(other, Node)):
            return (self.getNumber() == other.getNumber())
        return NotImplementedError
    
    """
    Inequality is determined based on whether the numbers are different.
    """
    def __ne__(self,other):
        eq = self.__eq__(other)
        if eq is NotImplementedError:
            return NotImplementedError
        return (not eq)