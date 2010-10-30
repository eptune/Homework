import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import idlsave
    
"""
Create a generic brushing program
"""

def draw():


    #read in IDL save file. 
    #It is an array of structures - one structure per star.
    junk = idlsave.idlsave.read("HW4.sav")
    #It returns a one element dictionary, so I grab the `stars` variable
    stars = junk['stars']
    stars = stars[np.where(stars.vmag > 0)] #throw out the sun
    stars.o_abund -= 8.7 #subtract the assumed solar abundance


    #plot the variables
    f = plt.figure()
    f.add_subplot(2,2,1) 
    plt.scatter(stars.feh,stars.o_abund,c='b',marker='o')

    f.add_subplot(2,2,2) 
    plt.scatter(stars.teff,stars.o_abund,c='b',marker='o')

    f.add_subplot(2,2,3) 
    plt.scatter(stars.vsini,stars.o_abund,c='b',marker='o')

    f.add_subplot(2,2,4) 
    plt.scatter(stars.vmag,stars.o_abund,c='b',marker='o')

    #pull their axes into list and label them
    axlist = f.get_axes()
    xtitles = ('[Fe/H]', 'Teff','Vsini','Vmag')
    ytitles = ('[O/H]','[O/H]','[O/H]','[O/H]')
    for i in np.arange(4):
        axlist[i].set_ylabel(ytitles[i])
        axlist[i].set_xlabel(xtitles[i])

    #Draw the plots
    plt.draw()

    #Instanciate a Brusher class
    test = Brusher(f,stars,axlist)
    print '<c> to clear buffers'
    return test

class Brusher:
    def __init__(self,f,stars,axlist):
        self.stars = stars
        self.figure = f
        self.axlist = axlist
        oncid = f.canvas.mpl_connect('button_press_event',self.onclick)
        offcid = f.canvas.mpl_connect('button_release_event',self.offclick)
        keycid = f.canvas.mpl_connect('key_press_event',self.onkey)
        self.corner1 = self.corner2 = None
        

    #When canvas is clicked, save poistion as corner1
    def onclick(self,event):
        print 'clicked on'
        self.corner1 = np.array([event.xdata,event.ydata])
        self.clickax = event.inaxes

    
    #when mouse button is released, save position as corner 2 and draw a box
    def offclick(self,event):
        print 'clicked off'
        self.corner2 = np.array([event.xdata,event.ydata])
        #draw the rectangle.

        if self.corner1 != None:
            self.ll = np.min([(self.corner1[0],self.corner2[0]),
                         (self.corner1[1],self.corner2[1])],axis=1)
            self.shape = np.abs(self.corner1-self.corner2)

            self.rec = matplotlib.patches.Rectangle(self.ll,self.shape[0],
                                                    self.shape[1],
                                                    color='gray',alpha=0.7)
            event.inaxes.add_patch(self.rec) #This is the current axes
            plt.draw()
            
    #If 'c' is pressed, redraw figure
    def onkey(self,event):
        if event.key == 'c':
            plt.clf()
            test = draw()
    
    #Will change the color of a specified axis.
    def changecolor(self,axindex):
        changeax = self.axlist[axindex]
        coll = changeax.collections[0]
        coll.set_facecolor('green')
        plt.draw()







    


