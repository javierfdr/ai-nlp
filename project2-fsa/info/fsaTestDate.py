# -*- coding: utf8 -*-
#!/pkg/ldc/bin/python2.5
#-----------------------------------------------------------------------------
# Name:        fsaTestDate.py
# Purpose:
#
# Author:      Horacio
#
# Created:     2013/09/09
# dmkmLabCase
#-----------------------------------------------------------------------------

import sys
import os
workingDir=os.getcwd()
sys.path.append( workingDir+"/jpbarrette-moman-5c5c2a1e4dea/finenight/python")
from fsa import *
import re

##functions

def alphabet():
    return re._alphanum.keys()+[' ']

def string2Fsa(s):
    states = map(lambda x:State('q'+str(x),{s[x]:'q'+str(x+1)}),range(len(s)))
    states.append(State('q'+str(len(s))))
    initialState = State('q0')
    finalStates = [State('q'+str(len(s)))]
    return Nfa(states, currentAlphabet, initialState, finalStates)
    
##global

currentAlphabet = alphabet()

months = ['January',
'February',
'March',
'April',
'May',
'June',
'July',
'August',
'September',
'October',
'November',
'December']

## building a set of FSA one for recognizing each month

fsaMonths=map(lambda x: string2Fsa(x),months)

## test these FSA:

for i in range(len(fsaMonths)):
    print fsaMonths[i].recognize(months[i])

## build a FSA from the union of these FSAs
    
unionMonths=fsaMonths[0]
for i in fsaMonths[1:]:
    unionMonths = unionMonths.union(i)

## test this FSA:

for i in range(len(months)):
    print unionMonths.recognize(months[i])


## minimizing and determinizing FSA and extending Alphabet

unionMonths = unionMonths.minimize()    
unionMonths = unionMonths.determinize()


## test this FSA:

for i in range(len(months)):
    print unionMonths.recognize(months[i])


