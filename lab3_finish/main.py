# -*- coding: utf-8 -*-
"""
Created on Fri Mar 13 18:04:47 2020

@author: tamas
"""

from evolutionaryController import EvolutionaryController
from hillClimbingController import HillClimbingController
from psoController import PSOController
import PyQt5 as qtpy
import sys
from Repository import PopulationRepository
from GUI import GUI
def main():
    app= qtpy.QtWidgets.QApplication(sys.argv)
    EARepository = PopulationRepository()
    PSORepository = PopulationRepository()
    eaController = EvolutionaryController(EARepository, 3, 100, 0.5, 1000)
    hcController = HillClimbingController(3,1000)
    psoController = PSOController(PSORepository,3,100,1000,1.0,1.1,2.1,10)
    gui = GUI(eaController,hcController,psoController)
    gui.show()
    sys.exit(app.exec_())

main()