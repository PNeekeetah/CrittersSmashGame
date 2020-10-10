# -*- coding: utf-8 -*-
"""
Created on Sat Oct 10 21:00:45 2020

@author: Nikita
"""

class Node:
    
    def __init__ (self, number, parent,originDistance):
        self.number = number
        self.parent = parent
        self.originDistance = originDistance
    
    def getParent(self):
        return self.parent
    
    def getNumber(self):
        return self.number
    
    def getOriginDistance(self):
        return self.originDistance
