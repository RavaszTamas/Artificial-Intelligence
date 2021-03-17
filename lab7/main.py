# -*- coding: utf-8 -*-
"""
Created on Tue Apr  7 13:36:06 2020

@author: tamas
"""
from controller import Controller
from repository import Repository
from ui import Console

def main():
    repo = Repository("bdate2.txt")
    contr = Controller(repo)
    console = Console(contr)
    console.run()
main()