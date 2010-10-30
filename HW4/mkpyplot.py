import idlsave
import matplotlib.pyplot as plt
import numpy as np
"""
This python code recreates a plot I am using in an upcoming paper that shows 
how stellar oxygen abundance varies with iron.  The stellar sample draws from 
both the thin and thick disks and some of the oxygen abundances are upper 
limits
"""

#Read in IDL save file. 
#It is an array of structures - one structure per star.
junk = idlsave.idlsave.read("HW4.sav")
#It returns a one element dictionary, so I grab the `stars` variable
stars = junk['stars']
stars.o_abund -= 8.7 #subtract the assumed solar abundance

nstars = stars.size
width = np.zeros(nstars)

#Pull out the width of the error bar.
#Is there a vectorized way to do this?
#I don't understand how to access elements in record arrays very well
for i in np.arange(nstars):
    width[i] = stars.o_err[i][1] - stars.o_err[i][0]
    if width[i] > 0.3:
        stars.o_abund[i] = stars.o_abund[i] + stars.o_err[i][1]

isuplim = (width > 0.3) #is the width of the error bar bigger than 0.3


#Put different stars in different buckets
#thick disk, thick disk -upperlim, thin disk, thin disk -upper limit
starstup = (stars[np.where((stars.pop_flag == 'dk') & ~isuplim )],
            stars[np.where((stars.pop_flag == 'dk') & isuplim )],
            stars[np.where((stars.pop_flag == 'dn') & ~isuplim )],
            stars[np.where((stars.pop_flag == 'dn') & isuplim )])
            
            

plt.clf()
f = plt.figure()
ax = f.add_subplot(111)

##Plot the data points
ax.plot(starstup[2].feh,starstup[2].o_abund,'bo',markersize=3)
ax.plot(starstup[3].feh,starstup[3].o_abund,'bv')
ax.plot(starstup[0].feh,starstup[0].o_abund,'ro')
ax.plot(starstup[1].feh,starstup[1].o_abund,'rv')

#Fit the non-upper limit points
x = np.linspace(-2,1,100)

dnfit = np.polyval(np.polyfit(starstup[2].feh,starstup[2].o_abund,1),x)
dkfit = np.polyval(np.polyfit(starstup[0].feh,starstup[0].o_abund,1),x)

ax.plot(x,dnfit,'-b' ,lw=2)
ax.plot(x,dkfit,'--r',lw=2)

ax.legend(('Thin Disk','Thin Disk UL','Thick Disk','Thick Disk UL','Thin Fit','Thick Fit'),loc='upper left')

ax.set_xlabel('[Fe/H]')
ax.set_ylabel('[O/H]')
ax.set_title('Dist. of O and Fe')
plt.show()
