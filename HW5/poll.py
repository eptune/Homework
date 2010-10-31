import sqlite3
import numpy as np
import matplotlib.mlab as mlab
import os
import matplotlib.pyplot as plt
import pylab
import webbrowser

class Poller:
    def __init__(self):
        """
        Initialize class and define variables that variables common to
        multiple methods.
        """


        self.dbfile = ['polls.db']
        self.conn = sqlite3.connect(self.dbfile[0])
        self.cur  = self.conn.cursor()
        self.partyarr = np.array(['Democrat','Republican','Independent'])

    def reload(self):
        self.conn = sqlite3.connect(self.dbfile[0])
        self.cur  = self.conn.cursor()

            
    def makedb(self):
        """
        reads data in from `candidate_names.txt`, `senate_polls.csv`, and 
        `stateabbr.txt` and stores them in `polls.db`
        """

        for file in self.dbfile:
            if os.path.exists(file):
                os.system('rm '+ file)

        self.reload()

        #load the data from csv into database.
        ################ NAMES ########################
        self.cur.execute('CREATE TABLE names (state TEXT, dem TEXT, gop '+
                         'TEXT, ind TEXT, incum TEXT)')
        names  = mlab.csv2rec('candidate_names.txt')
        for line in names:
            self.cur.execute('INSERT INTO names (state,dem,gop,ind,'+
                             'incum) VALUES '+str(line))

        ################# POLL DATA ####################

        self.cur.execute('CREATE TABLE poll (day float, state text, dem int, '+
                         'gop int, ind int)')
        poll  = mlab.csv2rec('senate_polls.csv')
        for line in poll:
            line = (line['day'],line['state'],line['dem']
                    ,line['gop'],line['ind'])
            self.cur.execute('INSERT INTO poll (day,state,dem,gop,ind)'+
                              ' VALUES '+str(line))
        ################## STATE ABBREVIATIONS  ########        

        self.cur.execute('CREATE TABLE abbr (full TEXT, code TEXT)')
        abbr  = mlab.csv2rec('stateabbr.txt',delimiter='\t')
        for line in abbr:
            self.cur.execute('INSERT INTO abbr (full,code) VALUES '+ str(line))

        self.conn.commit()
        self.cur.close()
#        self.conn.close()
    
    def candidates(self,state):
        """
        Return (dem-name,gop-name,ind-name,incumbent party) for `state`.
        """
        cmd = 'select names.dem,names.gop,names.ind,names.incum from names LEFT JOIN abbr on names.state = abbr.code where abbr.full = "'+state+'";'
        self.cur.execute(cmd)
        cand = np.array((self.cur.fetchall())[0])
        for i in range(len(cand)):
            cand[i] = cand[i].strip()

        return cand

    def polldat(self,state):
        """
        Returns the time series poll data as (day, dem, gop, ind)
        """

        cmd = "select poll.day,poll.dem,poll.gop,poll.ind from poll LEFT JOIN abbr on poll.state = abbr.full LEFT JOIN names on abbr.full = names.state where poll.state = '"+state+"';"
        self.cur.execute(cmd)
        data = np.array( (self.cur.fetchall() ) )
        return data

    def chart(self,state,save=False):
        """
        Plots the output of poll dat.  Will save to tempchart.png.
        """
        coarr = ('blue','red','purple')
        candidates = self.candidates(state)
        incum = candidates[3]
        candidates = candidates[0:3]
        incumidx =np.where(self.partyarr == incum) #who is the incumbent
        plt.clf()

        data = self.polldat(state)        
        for i in np.arange(3):
            if candidates[i] == '':
                candidates[i] = 'No '+self.partyarr[i]
            plt.plot(data[:,0],data[:,i+1],color=coarr[i])

        plt.title('Senate Race in '+state+'   Incumbent: '+incum)    
        plt.ylabel('Poll')
        plt.xlabel('Days Since Jan, 1 2010')
        plt.legend(candidates,loc='lower left')
        plt.show()
        if save:
            pylab.savefig('tempchart.png')
            

    def webdisplay(self,state):
        """
        Generate a simple webpage with the candidates, their photos, their
        polling info and whether polls expect their to be a switch
        """

        #make image
        htmlfile = 'temp.html'
        cand = self.candidates(state)

        html = '<html><body><h1>Race in '+state
        data = self.polldat(state)
        data = data[0,1:4]
        iincum =  (np.where(self.partyarr == cand[3]))[0][0]
        ileader = np.argmax(data)
        if iincum == ileader:
            html = html+': Incumbent Expected to Win</h1>'
        else:
            html = html+': Incumbent Expected to Lose</h1>'
        html = html+'Candidates:<p>'

        
        for i in range(len(self.partyarr)):
            html = html +'<BR><BR>'+self.partyarr[i]+':'+cand[i]+'<BR>'
            if cand[i] is not '':
                html = html+'<img src="candidates/'+cand[i]+'.gif"/>'

        plt.cla()
        self.chart(state,save=True)
        html = html+'<BR><img src="tempchart.png"/></p></html></body>'

        f = open(htmlfile,'w')
        f.writelines(html)
        f.close()
        webbrowser.open(os.path.abspath(".")+'/'+htmlfile)
        
        
    def shift(self):
        """
        Print the expected gain/loss of each party.
        """
        nincum = np.zeros(3) #dem,gop,ind
        nnew = np.zeros(3) #dem,gop,ind

        rec = mlab.csv2rec('senate_polls.csv')
        states = np.unique(rec.state)
        
        for state in states:
            data = self.polldat(state)
            data = data[0,1:4]
            candidates = self.candidates(state)
            iincum =  (np.where(self.partyarr == candidates[3]))[0][0]
            ileader = np.argmax(data)

            nnew[ileader]  = nnew[ileader] +1 
            nincum[iincum] = nincum[iincum] + 1
            

        shift = nnew - nincum

        print 'Expected Shift in Senate Party Balance'
        print self.partyarr
        print shift


