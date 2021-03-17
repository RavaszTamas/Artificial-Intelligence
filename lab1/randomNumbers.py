# -*- coding: utf-8 -*-

import numpy
import matplotlib.pyplot as plt
"""
Spyder Editor

This is a temporary script file.
"""
while True:
    print("""
          1 - exponential
          2 - normal
          0 - exit
          """)
    
    '''
    n = 10
    p = 0.3
    s = numpy.random.binomial(n,p,100)
    plt.ylabel("binomial")
    plt.plot(s,'ro')
    plt.show()
    '''
    n = int(input())
    if n == 1:
        print("Enter lambda value:")
        lam = int(input())
        print("Enter number of points:")
        num = int(input())
    
        s = numpy.random.exponential(lam,num)
        plt.ylabel("exponential")
        #count, bins, ignored = plt.hist(s, 50, normed=True)
        plt.plot(s,'ro')
        plt.show()
        
    elif n == 2:
        print("Enter mu value:")
        mu = int(input())
        print("Enter sigma value:")
        sigma = int(input())
        print("Enter number of points:")
        num = int(input())
    
        s = numpy.random.normal(mu, sigma, num)
        plt.ylabel("normal")
        
        #count, bins, ignored = plt.hist(s, 50, normed=True)
        plt.plot(s,'ro')#, 1/(sigma * numpy.sqrt(2 * numpy.pi)) *numpy.exp( - (bins - mu)**2 / (2 * sigma**2) ),linewidth=2, color='r')
        plt.show()
    elif n == 0:
        break
