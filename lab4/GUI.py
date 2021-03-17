# -*- coding: utf-8 -*-
"""
Created on Thu Mar 19 15:12:28 2020

@author: tamas
"""
import PyQt5 as qtpy
import sys
from PyQt5.QtWidgets import QMainWindow
from PyQt5.uic import loadUi
from evolutionaryController import EvolutionaryController
from hillClimbingController import HillClimbingController
from psoController import PSOController
from acoController import ACOController

import numpy as np
from Domain import ACOProblem

from Repository import PopulationRepository
from matplotlib.ticker import MaxNLocator
from multiprocessing import Process
from os import getpid
from Worker import Worker
import matplotlib.pyplot as plt


class GUI(QMainWindow):
    
    def __init__(self, evolutionaryController,hillClimbingController,psoController,acoController):
        super(GUI,self).__init__()
        loadUi("mainWindows.ui",self)
        
        self.problemSizeLineEdit.setValidator(qtpy.QtGui.QIntValidator(1,2147483647))
        self.populationSizeLineEdit.setValidator(qtpy.QtGui.QIntValidator(1,2147483647))
        self.probabilityMutationLineEdit.setValidator(qtpy.QtGui.QDoubleValidator(0.0,1.0,50))
        self.numberOfIterationsLineEdit.setValidator(qtpy.QtGui.QIntValidator(1,2147483647))
        self.wLineEdit.setValidator(qtpy.QtGui.QDoubleValidator(0.0,100.0,50))
        self.c1LineEdit.setValidator(qtpy.QtGui.QDoubleValidator(0.0,100.0,50))
        self.c2LineEdit.setValidator(qtpy.QtGui.QDoubleValidator(0.0,100.0,50))
        self.neighbourhoodSizeLineEdit.setValidator(qtpy.QtGui.QIntValidator(1,2147483647))
        self.numberOfAntsLineEdit.setValidator(qtpy.QtGui.QIntValidator(1,2147483647))
        self.alphaLineEdit.setValidator((qtpy.QtGui.QDoubleValidator(0.0,2147483647.0,50)))
        self.betaLineEdit.setValidator((qtpy.QtGui.QDoubleValidator(0.0,2147483647.0,50)))
        self.rhoLineEdit.setValidator(qtpy.QtGui.QDoubleValidator(0.0,1.0,50))
        self.probabilityQ0LineEdit.setValidator(qtpy.QtGui.QDoubleValidator(0.0,1.0,50))

        self.evolutionaryAlgorithmButton.clicked.connect(self.__executeEvolutionaryAlgorithm)
        self.hillClimbingButton.clicked.connect(self.__executeHillClimbing)
        self.psoButton.clicked.connect(self.__executePSO)
        self.acoButton.clicked.connect(self.__executeACO)
        self.stopButton.clicked.connect(self.__stopProcess)
        self.testButton.clicked.connect(self.__performTests)
        self.printTestResultButton.clicked.connect(self.__printPreviousTestResult)
        self.__evolutionaryController = evolutionaryController
        self.__hillClimbingController = hillClimbingController
        self.__psoController = psoController
        self.__acoController = acoController

        self.threadpool = qtpy.QtCore.QThreadPool()

        self.__printPreviousTestResult()
        self.stopButton.setEnabled(False)
    
    
    def __enableButtons(self):
        self.evolutionaryAlgorithmButton.setEnabled(True)
        self.hillClimbingButton.setEnabled(True)
        self.psoButton.setEnabled(True)
        self.stopButton.setEnabled(False)
        self.testButton.setEnabled(True)
        self.acoButton.setEnabled(True)
        self.printTestResultButton.setEnabled(True)

    def __disableButtons(self):
        self.evolutionaryAlgorithmButton.setEnabled(False)
        self.hillClimbingButton.setEnabled(False)
        self.psoButton.setEnabled(False)
        self.stopButton.setEnabled(True)
        self.testButton.setEnabled(False)
        self.acoButton.setEnabled(False)
        self.printTestResultButton.setEnabled(False)

    def __stopProcess(self):
        self.__evolutionaryController.interuptProcess()
        self.__hillClimbingController.interuptProcess()
        self.__psoController.interuptProcess()
        self.__acoController.interuptProcess()

        self.stopButton.setEnabled(False)

    def __executeHillClimbing(self):
        self.__readInputHillClimbing()
        
        worker = Worker(self.__hillClimbingController.startHillClimbing)
        worker.signals.result.connect(self.__printHillClimbingResult)
        worker.signals.progress.connect(self.__printHillClimbingPartial)
        worker.signals.finished.connect(self.__enableButtons)

        self.__disableButtons()
        
        self.threadpool.start(worker)

    def __executeACO(self):
        self.__readInputACO()
        
        worker = Worker(self.__acoController.startACO)
        worker.signals.result.connect(self.__printACOResult)
        worker.signals.progress.connect(self.__printACOPartialResult)
        worker.signals.finished.connect(self.__enableButtons)

        self.__disableButtons()
        
        self.threadpool.start(worker)

        
    def __executePSO(self):
        self.__readInputPSO()
        
        worker = Worker(self.__psoController.startPSO)
        worker.signals.result.connect(self.__printPSOResult)
        worker.signals.progress.connect(self.__printPSOPartial)
        worker.signals.finished.connect(self.__enableButtons)

        self.__disableButtons()

        self.threadpool.start(worker)

    def __printACOPartialResult(self,result):
        self.resultLabel.setText("Fitness (0 is the best value) = " + str(result[0].fitness()) + " after " + str(result[1]) + " iterations.")
        matrixToCheck = result[0].getPath()
        self.matrixDisplayTableWidget.clear()
        header = self.matrixDisplayTableWidget.horizontalHeader()
        header.setSectionResizeMode( qtpy.QtWidgets.QHeaderView.Stretch )

        self.matrixDisplayTableWidget.setRowCount(len(matrixToCheck)//2)
        self.matrixDisplayTableWidget.setColumnCount(len(matrixToCheck)//2)
        for i in range(len(matrixToCheck)//2):
            for j in range(len(matrixToCheck)//2):
                cell = qtpy.QtWidgets.QTableWidgetItem(str(matrixToCheck[i][j]+1) +","+str(matrixToCheck[i+len(matrixToCheck)//2][j]+1))
                cell.setTextAlignment( qtpy.QtCore.Qt.AlignHCenter )
                self.matrixDisplayTableWidget.setItem(i,j, cell )

    def __printACOResult(self,result):
        self.resultLabel.setText("Fitness (0 is the best value) = " + str(result[0].fitness()) + " after " + str(result[1]) + " iterations.")
        matrixToCheck = result[0].getPath()
        self.matrixDisplayTableWidget.clear()
        header = self.matrixDisplayTableWidget.horizontalHeader()
        header.setSectionResizeMode( qtpy.QtWidgets.QHeaderView.Stretch )

        self.matrixDisplayTableWidget.setRowCount(len(matrixToCheck)//2)
        self.matrixDisplayTableWidget.setColumnCount(len(matrixToCheck)//2)
        for i in range(len(matrixToCheck)//2):
            for j in range(len(matrixToCheck)//2):
                cell = qtpy.QtWidgets.QTableWidgetItem(str(matrixToCheck[i][j]+1) +","+str(matrixToCheck[i+len(matrixToCheck)//2][j]+1))
                cell.setTextAlignment( qtpy.QtCore.Qt.AlignHCenter )
                self.matrixDisplayTableWidget.setItem(i,j, cell )
        self.mathPlotWidget.canvas.axes.clear()
        self.mathPlotWidget.canvas.axes.plot(result[2], label="Best solution until that iteration")
        self.mathPlotWidget.canvas.axes.plot(result[3], label="Best solution for that iteration")
        self.mathPlotWidget.canvas.axes.legend()
        self.mathPlotWidget.canvas.axes.set_title('The best fitness for each iteration')
        self.mathPlotWidget.canvas.axes.yaxis.set_major_locator(MaxNLocator(integer=True))
        self.mathPlotWidget.canvas.axes.xaxis.set_major_locator(MaxNLocator(integer=True))

        self.mathPlotWidget.canvas.draw()


    def __printPSOPartial(self,result):
        
        self.resultLabel.setText("Fitness (0 is the best value) = " + str(result[0].fitness) + " after " + str(result[1]) + " iterations.")
        matrixToCheck = result[0].position
        self.matrixDisplayTableWidget.clear()
        header = self.matrixDisplayTableWidget.horizontalHeader()
        header.setSectionResizeMode( qtpy.QtWidgets.QHeaderView.Stretch )

        self.matrixDisplayTableWidget.setRowCount(len(matrixToCheck)//2)
        self.matrixDisplayTableWidget.setColumnCount(len(matrixToCheck)//2)
        for i in range(len(matrixToCheck)//2):
            for j in range(len(matrixToCheck)//2):
                cell = qtpy.QtWidgets.QTableWidgetItem(str(matrixToCheck[i][j]+1) +","+str(matrixToCheck[i+len(matrixToCheck)//2][j]+1))
                cell.setTextAlignment( qtpy.QtCore.Qt.AlignHCenter )
                self.matrixDisplayTableWidget.setItem(i,j, cell )


    def __printPSOResult(self,result):
        
        self.resultLabel.setText("Final fitness (0 is the best value) = " + str(result[0].fitness) + " after " + str(result[1]) + " iterations.")
        matrixToCheck = result[0].position
        self.matrixDisplayTableWidget.clear()
        header = self.matrixDisplayTableWidget.horizontalHeader()
        header.setSectionResizeMode( qtpy.QtWidgets.QHeaderView.Stretch )

        self.matrixDisplayTableWidget.setRowCount(len(matrixToCheck)//2)
        self.matrixDisplayTableWidget.setColumnCount(len(matrixToCheck)//2)
        for i in range(len(matrixToCheck)//2):
            for j in range(len(matrixToCheck)//2):
                cell = qtpy.QtWidgets.QTableWidgetItem(str(matrixToCheck[i][j]+1) +","+str(matrixToCheck[i+len(matrixToCheck)//2][j]+1))
                cell.setTextAlignment( qtpy.QtCore.Qt.AlignHCenter )
                self.matrixDisplayTableWidget.setItem(i,j, cell )

        self.mathPlotWidget.canvas.axes.clear()
        self.mathPlotWidget.canvas.axes.plot(result[2])
        self.mathPlotWidget.canvas.axes.set_title('The best fitness for each iteration')
        self.mathPlotWidget.canvas.axes.yaxis.set_major_locator(MaxNLocator(integer=True))
        self.mathPlotWidget.canvas.axes.xaxis.set_major_locator(MaxNLocator(integer=True))

        self.mathPlotWidget.canvas.draw()

        
    def __executeEvolutionaryAlgorithm(self):
        
        self.__readInputEvolutionary()
        worker = Worker(self.__evolutionaryController.startEvolutionary)
        worker.signals.result.connect(self.__printResultEvolutionary)
        worker.signals.progress.connect(self.__printResultEvolutionaryPartial)
        worker.signals.finished.connect(self.__enableButtons)

        self.__disableButtons()
        
        self.threadpool.start(worker)
    def __readInputACO(self):
        problemSize = 3

        try:
            problemSize = int(self.problemSizeLineEdit.text())
            if problemSize <= 0:
                raise Exception
        except :
            problemSize=3
        numberOfIterations = 10000
        try:
            numberOfIterations = int(self.numberOfIterationsLineEdit.text())
            if numberOfIterations <= 0:
                numberOfIterations = 10000
        except :
            numberOfIterations=10000
        numberOfAnts = 5
        try:
            numberOfAnts = int(self.numberOfAntsLineEdit.text())
            if numberOfAnts <= 0:
                numberOfAnts = 5
        except :
            numberOfAnts=5
        alpha = 1.9
        try:
            alpha = float(self.alphaLineEdit.text())
            if alpha <= 0.0:
                raise Exception
        except :
            alpha=1.9
        beta = 0.9
        try:
            beta = float(self.betaLineEdit.text())
            if beta <= 0.0:
                raise Exception
        except :
            beta=0.9
            
        rho = 0.3
        try:
            rho = float(self.rhoLineEdit.text())
            if rho <= 0.0:
                raise Exception
            if rho >= 1.0:
                raise Exception
        except :
            rho=0.3
            
        q0 = 0.3
        try:
            q0 = float(self.probabilityQ0LineEdit.text())
            if q0 <= 0.0:
                raise Exception
            if q0 >= 1.0:
                raise Exception
        except :
            q0=0.3
        newProblem = ACOProblem(problemSize, numberOfIterations, numberOfAnts, alpha, beta, rho, q0)
        self.__acoController.setProblem(newProblem)

    def __readInputHillClimbing(self):
        problemSize = 3

        try:
            problemSize = int(self.problemSizeLineEdit.text())
            if problemSize <= 0:
                raise Exception
        except :
            problemSize=3
            
        numberOfIterations = 10000
        try:
            numberOfIterations = int(self.numberOfIterationsLineEdit.text())
            if numberOfIterations <= 0:
                numberOfIterations = 10000
        except :
            numberOfIterations=10000
        probabilityMutation = 0.3
        try:
            probabilityMutation = float(self.probabilityMutationLineEdit.text())
            if probabilityMutation <= 0.0:
                raise Exception
            if probabilityMutation >= 1.0:
                raise Exception
        except :
            probabilityMutation=0.3


        self.__hillClimbingController.setMatrixSize(problemSize)
        self.__hillClimbingController.setNumberOfIterations(numberOfIterations)


    def __readInputEvolutionary(self):
        problemSize = 3

        try:
            problemSize = int(self.problemSizeLineEdit.text())
            if problemSize <= 0:
                raise Exception
        except :
            problemSize=3
            
        populationSize = 100
        try:
            populationSize = int(self.populationSizeLineEdit.text())
            if populationSize <= 0:
                raise Exception
        except :
            populationSize=100
            
        probabilityMutation = 0.3
        try:
            probabilityMutation = float(self.probabilityMutationLineEdit.text())
            if probabilityMutation <= 0.0:
                raise Exception
            if probabilityMutation >= 1.0:
                raise Exception
        except :
            probabilityMutation=0.3
        numberOfIterations = 10000
        try:
            numberOfIterations = int(self.numberOfIterationsLineEdit.text())
            if numberOfIterations <= 0:
                numberOfIterations = 10000
        except :
            numberOfIterations=10000


        self.__evolutionaryController.setMatrixSize(problemSize)
        self.__evolutionaryController.setPopulationNumber(populationSize)
        self.__evolutionaryController.setprobabilityMutation(probabilityMutation)
        self.__evolutionaryController.setNumberOfIterations(numberOfIterations)


    def __readInputPSO(self):
        problemSize = 3

        try:
            problemSize = int(self.problemSizeLineEdit.text())
            if problemSize <= 0:
                raise Exception
        except :
            problemSize=3
            
        populationSize = 100
        try:
            populationSize = int(self.populationSizeLineEdit.text())
            if populationSize <= 0:
                raise Exception
        except :
            populationSize=100
            
        numberOfIterations = 10000
        try:
            numberOfIterations = int(self.numberOfIterationsLineEdit.text())
            if numberOfIterations <= 0:
                numberOfIterations = 10000
        except :
            numberOfIterations=10000


        w = 1.0
        try:
            w = float(self.wLineEdit.text())
            if w <= 0.0:
                raise Exception
        except :
            w=1.0


        c1 = 1.1
        try:
            c1 = float(self.c1LineEdit.text())
            if c1 <= 0.0:
                raise Exception
        except :
            c1=1.1

        c1 = 1.1
        try:
            c1 = float(self.c1LineEdit.text())
            if c1 <= 0.0:
                raise Exception
        except :
            c1=1.1

        c2 = 2.0
        try:
            c2 = float(self.c1LineEdit.text())
            if c2 <= 0.0:
                raise Exception
        except :
            c2=2.0

        neighbourHoodSize = 10
        try:
            neighbourHoodSize = int(self.neighbourhoodSizeLineEdit.text())
            if neighbourHoodSize <= 0:
                neighbourHoodSize = 10
        except :
            neighbourHoodSize = 10

        self.__psoController.setMatrixSize(problemSize)
        self.__psoController.setPopulationNumber(populationSize)
        self.__psoController.setNumberOfIterations(numberOfIterations)
        self.__psoController.setInertiaCoefficient(w)
        self.__psoController.setSocialLearningCoefficient(c1)
        self.__psoController.setCognitiveLearningCoefficient(c2)
        self.__psoController.setNeighbourHoodSize(neighbourHoodSize)
    def __printHillClimbingPartial(self,result):

        self.resultLabel.setText("Fitness (0 is the best value) = " + str(result[0]) + " after " + str(result[2]) + " iterations.")
        matrixToCheck = result[1]
        self.matrixDisplayTableWidget.clear()
        header = self.matrixDisplayTableWidget.horizontalHeader()
        header.setSectionResizeMode( qtpy.QtWidgets.QHeaderView.Stretch )

        self.matrixDisplayTableWidget.setRowCount(len(matrixToCheck)//2)
        self.matrixDisplayTableWidget.setColumnCount(len(matrixToCheck)//2)
        for i in range(len(matrixToCheck)//2):
            for j in range(len(matrixToCheck)//2):
                cell = qtpy.QtWidgets.QTableWidgetItem(str(matrixToCheck[i][j]) +","+str(matrixToCheck[i+len(matrixToCheck)//2][j]))
                cell.setTextAlignment( qtpy.QtCore.Qt.AlignHCenter )
                self.matrixDisplayTableWidget.setItem(i,j, cell )

    def __printHillClimbingResult(self,result):

        
        '''
        print("Final fitness (0 is the best value) = " + str(result[0]) + " after " + str(result[2]) + " iterations.")
        matrixToCheck = result[1]
        #print(matrixToCheck)
        for i in range(len(matrixToCheck)//2):
            for j in range(len(matrixToCheck)//2):
                print("("+str(matrixToCheck[i][j]) +","+str(matrixToCheck[i+len(matrixToCheck)//2][j])+") ",end="")
            print()
        '''
        self.resultLabel.setText("Final fitness (0 is the best value) = " + str(result[0]) + " after " + str(result[2]) + " iterations.")
        matrixToCheck = result[1]
        self.matrixDisplayTableWidget.clear()
        header = self.matrixDisplayTableWidget.horizontalHeader()
        header.setSectionResizeMode( qtpy.QtWidgets.QHeaderView.Stretch )

        self.matrixDisplayTableWidget.setRowCount(len(matrixToCheck)//2)
        self.matrixDisplayTableWidget.setColumnCount(len(matrixToCheck)//2)
        for i in range(len(matrixToCheck)//2):
            for j in range(len(matrixToCheck)//2):
                cell = qtpy.QtWidgets.QTableWidgetItem(str(matrixToCheck[i][j]) +","+str(matrixToCheck[i+len(matrixToCheck)//2][j]))
                cell.setTextAlignment( qtpy.QtCore.Qt.AlignHCenter )
                self.matrixDisplayTableWidget.setItem(i,j, cell )
        self.mathPlotWidget.canvas.axes.clear()
        self.mathPlotWidget.canvas.axes.plot(result[3])
        self.mathPlotWidget.canvas.axes.set_title('The best fitness for each iteration')
        self.mathPlotWidget.canvas.axes.yaxis.set_major_locator(MaxNLocator(integer=True))
        self.mathPlotWidget.canvas.axes.xaxis.set_major_locator(MaxNLocator(integer=True))

        self.mathPlotWidget.canvas.draw()
        self.stopButton.setEnabled(False)

    def __printResultEvolutionaryPartial(self,result):

        '''
        
        print("Final fitness (0 is the best value) = " + str(result[0]) + " after " + str(result[2]) + " iterations.")
        matrixToCheck = result[1]
        #print(matrixToCheck)
        for i in range(len(matrixToCheck)//2):
            for j in range(len(matrixToCheck)//2):
                print("("+str(matrixToCheck[i][j]) +","+str(matrixToCheck[i+len(matrixToCheck)//2][j])+") ",end="")
            print()
        '''
        
        
        self.resultLabel.setText("Fitness (0 is the best value) = " + str(result[0]) + " after " + str(result[2]) + " iterations.")
        matrixToCheck = result[1]

        self.matrixDisplayTableWidget.clear()
        header = self.matrixDisplayTableWidget.horizontalHeader()
        header.setSectionResizeMode( qtpy.QtWidgets.QHeaderView.Stretch )

        self.matrixDisplayTableWidget.setRowCount(len(matrixToCheck)//2)
        self.matrixDisplayTableWidget.setColumnCount(len(matrixToCheck)//2)
        for i in range(len(matrixToCheck)//2):
            for j in range(len(matrixToCheck)//2):
                cell = qtpy.QtWidgets.QTableWidgetItem(str(matrixToCheck[i][j]) +","+str(matrixToCheck[i+len(matrixToCheck)//2][j]))
                cell.setTextAlignment( qtpy.QtCore.Qt.AlignHCenter )
                self.matrixDisplayTableWidget.setItem(i,j, cell )


    def __printResultEvolutionary(self,result):

        '''
        
        print("Final fitness (0 is the best value) = " + str(result[0]) + " after " + str(result[2]) + " iterations.")
        matrixToCheck = result[1]
        #print(matrixToCheck)
        for i in range(len(matrixToCheck)//2):
            for j in range(len(matrixToCheck)//2):
                print("("+str(matrixToCheck[i][j]) +","+str(matrixToCheck[i+len(matrixToCheck)//2][j])+") ",end="")
            print()
        '''
        
        
        self.resultLabel.setText("Final fitness (0 is the best value) = " + str(result[0]) + " after " + str(result[2]) + " iterations.")
        matrixToCheck = result[1]

        self.matrixDisplayTableWidget.clear()
        header = self.matrixDisplayTableWidget.horizontalHeader()
        header.setSectionResizeMode( qtpy.QtWidgets.QHeaderView.Stretch )
        
        self.matrixDisplayTableWidget.setRowCount(len(matrixToCheck)//2)
        self.matrixDisplayTableWidget.setColumnCount(len(matrixToCheck)//2)
        for i in range(len(matrixToCheck)//2):
            for j in range(len(matrixToCheck)//2):
                cell = qtpy.QtWidgets.QTableWidgetItem(str(matrixToCheck[i][j]) +","+str(matrixToCheck[i+len(matrixToCheck)//2][j]))
                cell.setTextAlignment( qtpy.QtCore.Qt.AlignHCenter )
                self.matrixDisplayTableWidget.setItem(i,j, cell )

        self.mathPlotWidget.canvas.axes.clear()
        self.mathPlotWidget.canvas.axes.plot(result[3])
        self.mathPlotWidget.canvas.axes.set_title('The best fitness for each iteration')
        self.mathPlotWidget.canvas.axes.yaxis.set_major_locator(MaxNLocator(integer=True))
        self.mathPlotWidget.canvas.axes.xaxis.set_major_locator(MaxNLocator(integer=True))

        self.mathPlotWidget.canvas.draw()
        
        plt.plot(result[3])
        plt.savefig('books_read.png')

        
    def __performTests(self):
        EARepository = PopulationRepository()
        PSORepository = PopulationRepository()
        acoProblem = ACOProblem(7, 1000, 40, 1.9, 0.9, 0.05, 0.5)

        self.__evolutionaryController = EvolutionaryController(EARepository, 7, 40, 0.5, 1000)
        self.__hillClimbingController = HillClimbingController(7,1000)
        self.__psoController = PSOController(PSORepository,7,100,50,0.5,1.1,1.5,10)
        self.__acoController = ACOController(acoProblem)
        
        self.__readInputEvolutionary()
        self.__readInputHillClimbing()
        self.__readInputPSO()
        self.__readInputACO()
        
        worker = Worker(self.__doTheTests)
        #worker.signals.result.connect(self.__printTestResults)
        worker.signals.finished.connect(self.__enableButtons)

        self.__disableButtons()
        
        self.threadpool.start(worker)

    def __printPreviousTestResult(self):
        resultEA = np.loadtxt("earesult.txt")
        resultEAAVGSTANDDEV = np.loadtxt("earesult_avg_standdev.txt")
        resultHC = np.loadtxt("hcresult.txt")
        resultHCAVGSTANDDEV = np.loadtxt("hcresult_avg_standdev.txt")
        resultPSO = np.loadtxt("psoresult.txt")
        resultPSOAVGSTANDDEV = np.loadtxt("psoresult_avg_standdev.txt")
        resultACO = np.loadtxt("acoresult.txt")
        resultACOAVGSTANDDEV = np.loadtxt("acoresult_avg_standdev.txt")

        self.mathPlotWidget.canvas.axes.clear()
        self.mathPlotWidget.canvas.axes.plot(resultEA, label="Evolutionary average")
        self.mathPlotWidget.canvas.axes.plot(resultHC, label="Hill climbing average")
        self.mathPlotWidget.canvas.axes.plot(resultPSO, label="PSO climbing average")
        self.mathPlotWidget.canvas.axes.plot(resultACO, label="ACO climbing average")
        self.mathPlotWidget.canvas.axes.legend()
        self.mathPlotWidget.canvas.axes.set_title('The test for best fitness average for each iteration')
        self.mathPlotWidget.canvas.axes.yaxis.set_major_locator(MaxNLocator(integer=True))
        self.mathPlotWidget.canvas.axes.xaxis.set_major_locator(MaxNLocator(integer=True))
        self.mathPlotWidget.canvas.draw()

        self.resultLabel.setText("Average Fitness EA, standard deviation EA = " + "{0:.2f}".format(resultEAAVGSTANDDEV[0]) +","+"{0:.2f}".format(resultEAAVGSTANDDEV[1]) +
            " Average Fitness Hill cimbing, standard deviation Hill climbing = " + "{0:.2f}".format(resultHCAVGSTANDDEV[0]) +","+"{0:.2f}".format(resultHCAVGSTANDDEV[1])+
            " Average Fitness PSO, standard deviation PSO = " + "{0:.2f}".format(resultPSOAVGSTANDDEV[0]) +","+"{0:.2f}".format(resultPSOAVGSTANDDEV[1]) +
            " Average Fitness PSO, standard deviation PSO = " + "{0:.2f}".format(resultACOAVGSTANDDEV[0]) +","+"{0:.2f}".format(resultACOAVGSTANDDEV[1]))


    def __doTheTests(self,progress_callback):

        self.__evolutionaryController.setTesting(True)
        self.__hillClimbingController.setTesting(True)
        self.__psoController.setTesting(True)
        self.__acoController.setTesting(True)


        resultOfEA = self.__evolutionaryController.performTests()
        resultOfHC = self.__hillClimbingController.performTests()
        resultOfPSO = self.__psoController.performTests()
        resultOfACO = self.__acoController.performTests()
        print("start tests")
        self.__evolutionaryController.setTesting(False)
        self.__hillClimbingController.setTesting(False)
        self.__psoController.setTesting(False)
        self.__acoController.setTesting(False)
        print("finish tests")

        result = (resultOfEA,resultOfHC,resultOfPSO,resultOfACO)
        self.mathPlotWidget.canvas.axes.clear()
        self.mathPlotWidget.canvas.axes.plot(result[0][0], label="Evolutionary average")
        self.mathPlotWidget.canvas.axes.plot(result[1][0], label="Hill climbing average")
        self.mathPlotWidget.canvas.axes.plot(result[2][0], label="PSO average")
        self.mathPlotWidget.canvas.axes.plot(result[3][0], label="ACO average")
        self.mathPlotWidget.canvas.axes.legend()
        self.mathPlotWidget.canvas.axes.set_title('The test for best fitness average for each iteration')
        self.mathPlotWidget.canvas.axes.yaxis.set_major_locator(MaxNLocator(integer=True))
        self.mathPlotWidget.canvas.axes.xaxis.set_major_locator(MaxNLocator(integer=True))
        self.mathPlotWidget.canvas.draw()

        s = "Average Fitness EA, standard deviation EA = " + "{0:.2f}".format(result[0][1]) +","+"{0:.2f}".format(result[0][2]) + " Average Fitness Hill cimbing, standard deviation Hill climbing = " + "{0:.2f}".format(result[1][1]) +","+"{0:.2f}".format(result[1][2])+" Average Fitness PSO, standard deviation PSO = " + "{0:.2f}".format(result[2][1]) +","+"{0:.2f}".format(result[2][2])+" Average Fitness ACO, standard deviation ACO = " + "{0:.2f}".format(result[3][1]) +","+"{0:.2f}".format(result[3][2])
        self.resultLabel.setText("Average Fitness EA, standard deviation EA = " + "{0:.2f}".format(result[0][1]) +","+"{0:.2f}".format(result[0][2]) +
            " Average Fitness Hill cimbing, standard deviation Hill climbing = " + "{0:.2f}".format(result[1][1]) +","+"{0:.2f}".format(result[1][2])+
            " Average Fitness PSO, standard deviation PSO = " + "{0:.2f}".format(result[2][1]) +","+"{0:.2f}".format(result[2][2]) +
            " Average Fitness ACO, standard deviation ACO = " + "{0:.2f}".format(result[3][1]) +","+"{0:.2f}".format(result[3][2]))


        np.savetxt("earesult.txt",result[0][0],delimiter=",")
        np.savetxt("earesult_avg_standdev.txt",[result[0][1],result[0][2]],delimiter=",")
        np.savetxt("hcresult.txt",result[1][0],delimiter=",")
        np.savetxt("hcresult_avg_standdev.txt",[result[1][1],result[1][2]],delimiter=",")
        np.savetxt("psoresult.txt",result[2][0],delimiter=",")
        np.savetxt("psoresult_avg_standdev.txt",[result[2][1],result[2][2]],delimiter=",")
        np.savetxt("acoresult.txt",result[3][0],delimiter=",")
        np.savetxt("acoresult_avg_standdev.txt",[result[3][1],result[3][2]],delimiter=",")

        plt.plot(result[0][0], label="Evolutionary average")
        plt.plot(result[1][0], label="Hill climbing average")
        plt.plot(result[2][0], label="PSO climbing average")
        plt.plot(result[3][0], label="PSO climbing average")
        plt.legend()
        plt.title('The best fitness average for each iteration')
        plt.savefig('test_fresh.png')
        outF = open("resultString.txt", "w")
        outF.write(s)
        outF.close()

    def __averageForEachGeneration(self,resultEA):
        averages = []
        length = len(resultEA)
        for j in range(len(resultEA[0])):
            s = 0
            for i in range(len(resultEA)):
                s += resultEA[i][j]
            averages.append(s/length)
        return averages

    def __printTestResults(self,result):
        if result == None:
            return
        self.resultLabel.setText(
            "Average Fitness EA, standard deviation EA = " + "{0:.2f}".format(result[0][1]) +","+"{0:.2f}".format(result[0][2]) +
            " Average Fitness Hill cimbing, standard deviation Hill climbing = " + "{0:.2f}".format(result[1][1]) +","+"{0:.2f}".format(result[1][2])+
            " Average Fitness PSO, standard deviation PSO = " + "{0:.2f}".format(result[2][1]) +","+"{0:.2f}".format(result[2][2])
            )

        self.mathPlotWidget.canvas.axes.clear()
        self.mathPlotWidget.canvas.axes.plot(result[0][0], label="Evolutionary average")
        self.mathPlotWidget.canvas.axes.plot(result[1][0], label="Hill climbing average")
        self.mathPlotWidget.canvas.axes.plot(result[2][0], label="PSO climbing average")
        self.mathPlotWidget.canvas.axes.legend()
        self.mathPlotWidget.canvas.axes.set_title('The best fitness average for each iteration')
        self.mathPlotWidget.canvas.axes.yaxis.set_major_locator(MaxNLocator(integer=True))
        self.mathPlotWidget.canvas.axes.xaxis.set_major_locator(MaxNLocator(integer=True))
        self.mathPlotWidget.canvas.draw()

        plt.plot(result[0][0], label="Evolutionary average")
        plt.plot(result[1][0], label="Hill climbing average")
        plt.plot(result[2][0], label="PSO climbing average")
        plt.legend()
        plt.title('The best fitness average for each iteration')
        plt.savefig('books_read.png')


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
