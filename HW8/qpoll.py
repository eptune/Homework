#!/bin/env python

#make sure the correct path is loaded
import sys
path = sys.path
#fail=True
#for l in path:
#    if l.find('/Homework/') != -1:
#        print l
#        fail = False
#if fail:
sys.path.append('../')

import HW5.poll # now can access as a package
import argparse
from datetime import datetime
import sqlite3

parser = argparse.ArgumentParser(description='Polling Function')

parser.add_argument('-C', action='store', default='',
                    dest='state',
                    help='Pop a chart of current state')

parser.add_argument('-N', action='store_true', default=False,
                    dest='newinfo',
                    help='Added new information to database')

#default time value for new data is now
now   = datetime.now()
start = datetime(now.year,1,1)
days  = float((now-start).days)

#parser.add_argument('-n', action='store', dest='npts',type=int,
#                    help='Number of Points to Plots')

parser.add_argument('-t', action='store', default=days,
                    type=float,
                    dest='time',
                    help='Days since Jan 1')

parser.add_argument('-d', action='store', default=0,
                    type=int,
                    dest='dem',
                    help='Democratic Polling Data')

parser.add_argument('-r', action='store', default=0,
                    type=int,
                    dest='rep',
                    help='Republican Polling Data')

parser.add_argument('-i', action='store', default=0,
                    type=int,
                    dest='ind',
                    help='Independent Polling Data')


results  = parser.parse_args()
state  = results.state
newinfo= results.newinfo
time   = results.time
dem    = results.dem
rep     = results.rep
ind    = results.ind

p = HW5.poll.Poller()
p.makedb()

if newinfo:
    conn = sqlite3.connect('poll.db')
    cur = conn.cursor()
    cmd = 'INSERT INTO poll (day,state,dem,gop,ind) VALUES (%f,"%s",%i,%i,%i) '\
        % (time,state,dem,rep,ind)
    print cmd

#    cur.execute(cmd)
#    conn.commit()
#    cur.close()
#    conn.close()

if state is not '':
    p.reload()
    p.chart(state)


