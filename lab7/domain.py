# -*- coding: utf-8 -*-
"""
Created on Tue Apr  7 20:19:41 2020

@author: tamas
"""

class InvalidInputDataException(Exception):
    pass

class Entry():
    
    def __init__(self,theClass,Attributes):
        self.__attributes = []
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