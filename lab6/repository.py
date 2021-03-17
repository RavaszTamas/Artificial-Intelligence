# -*- coding: utf-8 -*-
"""
Created on Tue Apr  7 20:20:28 2020

@author: tamas
"""

from domain import Entry

class Repository():
    
    def __init__(self,fileName="balance-scale.data"):
        self.__fileName = fileName
        
    def getAllData(self):
        f = open(self.__fileName,"r")
        line = f.readline()
        entries=[]
        while line != "":
            params = line.split(",")
            newEntry = Entry(params[0],params[1:5])
            entries.append(newEntry)
            line = f.readline()
        
        return entries