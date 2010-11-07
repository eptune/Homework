#!/usr/bin/env python

from random import uniform
from math import sqrt
from time import time
from math import pi
import numpy as np
#import numexpr
import multiprocessing
from threading import Thread

def plotloop():
    """
    Calls all 3 benchmarking options and plots the performance curve.
    """

    types = ['Simple','Process','Thread']
    ndartsarr,timearr,ratearr = {},{},{}

    for type in types:
        print "Benchmarking %s Method" % type
        ndartsarr[type],timearr[type],ratearr[type] = benchmark(type=type)

    import matplotlib.pylab as plt

    f = plt.figure( figsize=(6,6) )
    
    f.subplots_adjust(hspace=0.0001)
    f.subplots_adjust(left=0.18)
    ax1 = plt.subplot(211)
    ax1.set_ylabel('Rate (Darts/S)')
    ax1.set_xticklabels('',visible=False)

    ax2 = plt.subplot(212,sharex=ax1)
    ax2.set_xlabel('Number of darts')
    ax2.set_ylabel('Execution Time (s)')

    for type in types:
        ax1.semilogx(ndartsarr[type],ratearr[type],'o-',label=type)
        ax2.loglog(ndartsarr[type],timearr[type],'o-',label=type)

    ax2.legend(loc='best')

    plt.show()
    
def benchmark(type='Simple'):
    """
    Wrapper around mcpi.
    Can excute using one of the follwing methods:

    Simple - Execute as fast as possible using single core.
    Process - Execute using two processors
    Thread  - Execute using 2*num_cpu threads.

    sim_time - sets the minimum time we spend on a given ndarts. 

    """
    npts = 11
    ndartsarr = np.array(np.logspace(1,7,num=npts,base=10),dtype=int)
    timearr = np.empty(npts)
    ratearr = np.empty(npts)
    sim_time = 1 # Time to simulate each x point

    ncpu = multiprocessing.cpu_count()
    if type is 'Process':
        pool = multiprocessing.Pool(ncpu)

    for i in range(npts):
        times,rates = [],[]        

        while_start_time = time()        
        elapsed_time = 0
        while elapsed_time < sim_time:
            if type is 'Process':
                start_time = time()
                ndarts = [ndartsarr[i]/ncpu]*ncpu
                l = pool.map(mcpi,ndarts)
                looptime = time()- start_time
            elif type is 'Simple':
                start_time = time()
                mcpi(ndartsarr[i])
                looptime = time() -start_time

            elif type is 'Thread':
                start_time = time()
                nthread = ncpu*2
                ndarts = [ndartsarr[i]/nthread]*nthread

                threadlist = []
                for n in ndarts:
                    current = mcpi_thread(n)
                    threadlist.append(current)
                    current.start()

                for thread in threadlist:
                    thread.join()

                looptime = time() -start_time


            times.append(looptime),rates.append(ndartsarr[i]/looptime)
            elapsed_time = time() - while_start_time
        
        timearr[i] = np.array(times).mean()
        ratearr[i] = np.array(rates).mean()
        print"""
Number of Darts    : %d
Execution Time (s) : %f
Darts / s          : %f
""" % (ndartsarr[i],timearr[i],ratearr[i])


    return (ndartsarr,timearr,ratearr)

def mcpi(ndarts,verbose=False):    
    """
    Runs the Monte Carlo based calculation of pi.
    Verbose - prints out the results.
    """
    ninside = 0
    for n in range(ndarts):
        x,y = uniform(0,1),uniform(0,1)
        if sqrt((x-0.5)**2 + (y-0.5)**2) <=0.5:
            ninside += 1

    pi_approx = 4*ninside / float(ndarts)
    error = (pi_approx - pi) / pi



    if verbose:
        print """
Pi Approx          : %f
Error              : %f
N Darts            : %d
Execution Time (s) : %f
Darts / s          : %f
""" % (pi_approx,error,ndarts,looptime,dartrate)

class mcpi_thread(Thread):
    def __init__(self,ndarts):
        Thread.__init__(self)
        self.ndarts  = ndarts

    def run(self):
        mcpi(self.ndarts)
        
