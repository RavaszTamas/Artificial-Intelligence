from model import Definition,membershipFunctionFactory,FuzzySystem,membershipFunctionFactoryCut
from controller import Controller
from view import View
import matplotlib as mpl
'''
temperature = Definition()
temperature.addFunction('very cold', membershipFunctionFactory(-30, -30, -20, 5))
temperature.addFunction('cold', membershipFunctionFactory(-5, 0,0, 10))
temperature.addFunction('normal', membershipFunctionFactory(5, 10, 15, 20))
temperature.addFunction('warm', membershipFunctionFactory(15, 20,20, 25))
temperature.addFunction('hot', membershipFunctionFactory(25, 30, 35, 35))
print(temperature.fuzzifyInput(17))
'''

'''

fu  = membershipFunctionFactoryCut(10,15,25,30,0.9)

ints = [i for i in range(0,30)]

fints = [ fu(i) for i in range(0,30)]

mpl.pyplot.plot(ints, fints, label='loss value vs iteration')
print(fints)
fu  = membershipFunctionFactoryCut(10,15,25,30,1)

ints = [i for i in range(0,30)]

fints = [ fu(i) for i in range(0,30)]



mpl.pyplot.plot(ints, fints, label='loss value vs iteration')

mpl.pyplot.show()
'''

if __name__=="__main__":
    
    fuzzySystem = FuzzySystem("problem.in")
    
    controller = Controller(fuzzySystem)
        
    controller.start()
    