# -*- coding: utf-8 -*-
"""
Created on Tue Apr  7 20:20:28 2020

@author: tamas
"""


class Repository():
    
    def __init__(self,fileName="bdate2.txt"):
        self.__fileName = fileName
        
    def getAllData(self):
        f = open(self.__fileName,"r")
        line = f.readline()
        entries=[]
        while line != "":
            if line.strip() != "":
                params = line.strip().split()
                params = list(map(float, params))
                entries.append(params)
            line = f.readline()
        
        return entries