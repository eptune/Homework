import idlsave
import matplotlib.pyplot as plt
import matplotlib.mlab as mlab
import numpy as np
import matplotlib
from matplotlib.ticker import MultipleLocator, FormatStrFormatter
"""
Code to reproduce the plot in the homework prompt.
"""

#Parameters
lntk = 2 #line thickness

#Read in data using CSV2REC
#Usually csv2rec takes the first row to by the names of the records.
#It starts from the begining when I specify their names manually.
#Therefore, I need to skip the first row.
goog = mlab.csv2rec("google_data.csv",names=('MJD','Value'),skiprows=1)
yahoo = mlab.csv2rec("yahoo_data.csv",names=('MJD','Value'),skiprows=1)
temp = mlab.csv2rec("ny_temps.csv",names=('MJD','High'),skiprows=1)

f = plt.figure()
ax = f.add_subplot(111)
ax.set_xlim((49e3,55.6e3))
ax2 = ax.twinx() #create a new axis

#set all the minor grids that are not included by default
ax.yaxis.set_minor_locator(MultipleLocator(20))
ax.xaxis.set_minor_locator(MultipleLocator(200))
ax2.yaxis.set_minor_locator(MultipleLocator(10))

##Plot the data points
ax.plot(yahoo['MJD'],yahoo['Value'],'-',color='indigo',lw=lntk)
ax.plot(goog['MJD'],goog['Value'],'-b',lw=lntk)
ax2.plot(temp['MJD'],temp['High'],'--r',lw=lntk)

#Set the title
ax.set_title('New York Temperature, Google, and Yahoo!',fontsize='xx-large',family='times',weight='bold')

#label the axes
ax.set_xlabel('Date (MJD)',size='large')
ax.set_ylabel('Value (Dollars)',size='large')
ax2.set_ylabel(r'Temperature ($^{\circ}$F)',size='large')

#set the limits of the second axes
ax2.set_ylim((-150,100))

#plot the legend using the lines from both axes.
axline = ax.get_lines()
ax2line = ax2.get_lines()
leg = ax.legend((axline[0],axline[1],ax2line[0]),('Yahoo! Stock Value','Google Stock Value','NY Mon. High Temp'),loc='center left')

#make the legend frame invisible
legframe = leg.get_frame()
legframe.set_visible(False)

#make the text in the legend smaller
for t in leg.get_texts():
    t.set_fontsize('medium')


plt.show()
