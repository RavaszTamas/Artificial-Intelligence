# -*- coding: utf-8 -*-
"""
Created on Tue Apr  7 20:19:41 2020

@author: tamas
"""

class InvalidInputDataException(Exception):
    pass

class Node():
    def __init__(self,label=None,isLeaf=False):
        self.__label = label
        self.__isLeaf = isLeaf
        self.__children = {}
    def setLabel(self,label):
        if label == "":
            raise ValueError("Not a valid label")
        self.__label = label

    def setIsLeaf(self,value):
        self.__isLeaf = value
    
    def getLabel(self):
        return self.__label
    
    def isLeaf(self):
        return self.__isLeaf
    
    def addChild(self,key,newChild):
        if newChild.getLabel() == "":
            raise ValueError("Not a valid label")

        self.__children[key] = newChild
    
    def getChildren(self):
        return self.__children
    
    def __str__(self):
        s = ""
        s += str(self.__label) + "\n"
        s += str(self.__children)
        return s
class Entry():
    
    def __init__(self,theClass,Attributes):
        self.__attributes = {"first":int(Attributes[0]),"second":int(Attributes[1]),"third":int(Attributes[2]),"fourth":int(Attributes[3])}
        self.__theClass = theClass
    
    def getClass(self):
        return self.__theClass
    
    def getAttributes(self):
        return self.__attributes
    
    def getValue(self,key):
        return self.__attributes[key]
    
    def __str__(self):
        return str(self.__theClass)
    def __repr__(self):
        return str(self)