# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainWindows.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from Controller import Controller
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtCore import QObject
from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton
import sys
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import numpy as np

class MathPlotWidget(QWidget):
    def __init__(self,parent=None):
        QtWidgets.QWidget.__init__(self,parent)
        self.canvas = FigureCanvas(Figure())
        vertical_layout = QtWidgets.QVBoxLayout()
        vertical_layout.addWidget(self.canvas)
        self.canvas.axes = self.canvas.figure.add_subplot(111)
        self.setLayout(vertical_layout)

class MyGUI(QMainWindow):
    
    def __init__(self):
        super(MyGUI,self).__init__()
        self.__controller = Controller(5,100,0.3,10000)
        self.setupUi(self)
    def __executeEvolutionaryAlgorithm(self):
        self.__printResultEvolutionary( self.__controller.startEvolutionary())

    def __executeHillClimbing(self):
        return self.__controller.startHillClimbing()

    def __printHillClimbingResult(self,result):

        print("Final fitness (0 is the best value) = " + str(result[0]) + " after " + str(result[2]) + " iterations.")
        matrixToCheck = result[1]
        #print(matrixToCheck)
        for i in range(len(matrixToCheck)//2):
            for j in range(len(matrixToCheck)//2):
                print("("+str(matrixToCheck[i][j]) +","+str(matrixToCheck[i+len(matrixToCheck)//2][j])+") ",end="")
            print()

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
        
        self.mathPlotWidget.canvas.axes.clear()
        self.mathPlotWidget.canvas.axes.plot()
        
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        MainWindow.setMinimumSize(QtCore.QSize(800, 600))
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        
        #plot part to do create custom QWidget figurecanvas to make plot workable
        
        self.mathPlotWidget = MathPlotWidget(self.centralwidget)
        self.mathPlotWidget.setMinimumSize(QtCore.QSize(800, 350))
        self.mathPlotWidget.setObjectName("mathPlotWidget")
        self.verticalLayout_2.addWidget(self.mathPlotWidget)
        
        
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.evolutionaryAlgorithmButton = QtWidgets.QPushButton(self.centralwidget)
        self.evolutionaryAlgorithmButton.setObjectName("evolutionaryAlgorithmButton")
        self.evolutionaryAlgorithmButton.clicked.connect(self.__executeEvolutionaryAlgorithm)
        self.horizontalLayout.addWidget(self.evolutionaryAlgorithmButton)
        self.hillClimbingButton = QtWidgets.QPushButton(self.centralwidget)
        self.hillClimbingButton.setObjectName("hillClimbingButton")
        self.horizontalLayout.addWidget(self.hillClimbingButton)
        self.psoButton = QtWidgets.QPushButton(self.centralwidget)
        self.psoButton.setObjectName("psoButton")
        self.horizontalLayout.addWidget(self.psoButton)
        self.verticalLayout_2.addLayout(self.horizontalLayout)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem)
        self.formLayout_2 = QtWidgets.QFormLayout()
        self.formLayout_2.setObjectName("formLayout_2")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label.setObjectName("label")
        self.formLayout_2.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label)
        self.problemSizeLineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.problemSizeLineEdit.setObjectName("problemSizeLineEdit")
        self.formLayout_2.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.problemSizeLineEdit)
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_2.setObjectName("label_2")
        self.formLayout_2.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_2)
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setObjectName("label_3")
        self.formLayout_2.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.label_3)
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setObjectName("label_4")
        self.formLayout_2.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.label_4)
        self.numberOfIterationsLineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.numberOfIterationsLineEdit.setObjectName("numberOfIterationsLineEdit")
        self.formLayout_2.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.numberOfIterationsLineEdit)
        self.populationSizeLineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.populationSizeLineEdit.setObjectName("populationSizeLineEdit")
        self.formLayout_2.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.populationSizeLineEdit)
        self.probabilityMutationLineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.probabilityMutationLineEdit.setObjectName("probabilityMutationLineEdit")
        self.formLayout_2.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.probabilityMutationLineEdit)
        self.verticalLayout_2.addLayout(self.formLayout_2)
        self.verticalLayout_3.addLayout(self.verticalLayout_2)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 26))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        #QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Lab3"))
        self.evolutionaryAlgorithmButton.setText(_translate("MainWindow", "Run Evolutionary Algorithm"))
        self.hillClimbingButton.setText(_translate("MainWindow", "Run Hill Climbing"))
        self.psoButton.setText(_translate("MainWindow", "Run PSO"))
        self.label.setText(_translate("MainWindow", "Number of matrix rows:"))
        self.label_2.setText(_translate("MainWindow", "Population size:"))
        self.label_3.setText(_translate("MainWindow", "Probablity of mutation:"))
        self.label_4.setText(_translate("MainWindow", "Number of iterations:"))

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = MyGUI()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

