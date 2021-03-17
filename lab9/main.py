# -*- coding: utf-8 -*-
"""
Created on Fri May 15 11:39:52 2020

@author: tamas
"""
from Repository import Repository
from Controller import Controller
from UI import Console

if __name__=="__main__":
    repo = Repository()
    contr = Controller(repo)
    console = Console(contr)
    console.run()