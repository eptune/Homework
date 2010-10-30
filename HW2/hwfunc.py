#Home work #2 code for Erik Petigura 18605957
#
#
#
#


import numpy as np
import matplotlib.pyplot as plt
import scipy as sp
from scipy.optimize import leastsq
from scipy.interpolate import spline

a,alpha,k = 2.,-0.75,0.1 #assign values to parameters
sig = 0.1 # sigma of the noise
npts = 100
x = np.linspace(0,4,npts) #independant variable
xspline = np.linspace(0,4,npts*10) #independant variable

### THE SIGNAL ###
y = a*sp.exp(alpha*x) + k

### THE NOISE ###
ynoise = y + sp.random.normal(0,sig,npts) 

def resid(par):
  return model(par)-ynoise

def model(par):
  return par[0]*sp.exp(par[1]*x) + par[2]

def fitter():
  par0 = [1,-.1,.2]

  fitpar = leastsq(resid,par0)
  plt.plot(x,ynoise,'bo')
  plt.plot(x,model(fitpar[0]))

  spy = spline(x,ynoise,xspline)
  plt.plot(xspline,spy)

  deg = [0,1,2]
  for i in deg:
    plt.plot(x,np.polyval(np.polyfit(x,ynoise,i),x))

  plt.legend(('signal','exp','spline','const','lin','quad'))



def denoise():
  #LOAD UP THE IMAGE
  img = plt.imread("moonlanding.png")#array is (y,x)
  imgshape = img.shape
  mask = np.ones(imgshape)

  fimg = np.fft.fft2(img)

  #Got this by trial and error.  
  #Not as good as example, but better than original image
  killy = (60,570)
  killx = (50,440)
  
  mask[killx[0]:killx[1],::] = 0
  mask[::,killy[0]:killy[1]] = 0


  plt.imshow(mask)  
  ffimg = fimg
  ffimg[np.where(mask < 1)] = 0. + 0j

#  plt.imshow(abs(ffimg))
#  plt.imshow(mask)


  #compute the inverse fft, killing any complex component

  recimg = abs(np.fft.ifft2(ffimg))

  plt.imshow(recimg)


def my_matrixinv(mat):
  width = mat.shape[0]
  det = np.linalg.det
  if det == 0 :
    print "det = 0; matrix not invertable"
    

  identity = sp.identity(width)
  inv = sp.linalg.solve(mat,identity)

  return inv
    


