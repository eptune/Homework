def fitter():

    import numpy as np
    import matplotlib.pyplot as plt
    import scipy as sp

    ### THE SIGNAL ###
    x = np.linspace(0,4,100) #independant variable
    a,alpha,k = 2.,-0.75,0.1 #assign values to parameters
    y = a*sp.exp(alpha*x) + k

    plt.hist(x,y)

    ### THE NOISE ###

    ynoise = 


