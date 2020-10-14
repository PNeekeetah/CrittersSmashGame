# -*- coding: utf-8 -*-
"""
Created on Sat Oct 10 21:00:45 2020

@author: Nikita
"""

class Node:
    
    def __init__ (self, number):
        self.number = number
        self.parent = None
        self.children = []
    
    def getNumber(self):
        return self.number
    
    def getParent(self):
        return self.parent
    
    def setParent (self, node):
        self.parent = node;
    
    def getChildren(self):
        return self.children
    
    def addChild (self, child):
        self.children.append(child)
    
    def __eq__ (self, other):
        if (isinstance(other, Node)):
            return (self.getNumber() == other.getNumber())
        return NotImplementedError
    
    def __ne__(self,other):
        eq = self.__eq__(other)
        if eq is NotImplementedError:
            return NotImplementedError
        return (not eq)