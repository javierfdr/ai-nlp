from __future__ import division

#---------------------------------------#
#     Project 2 - FSA                   #
#  Master in Artificial Intelligence    #
#  Natural Language Processing          #
#            UPC                        #
#                                       #
#    Alejandro Hernandez                #
#     Javier Fernandez                  #
#                                       #
# --------------------------------------#

import os
import sys
workingDir=os.getcwd()
sys.path.append( workingDir+"/info/fsa-osteele/FSA-1.0")

import math
import random
from reCompiler import *
from FSA import union

tfile = "/Users/javierfdr/devel/mai/nlp-practice/repo/nlp/project2-fsa/info/examples_birth_date.txt"

# defining constants
month_letters = ['January',
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

month_letters_short = ['Jan',
'Feb',
'Mar',
'Apr',
'May',
'Jun',
'Jul',
'Aug',
'Sep',
'Oct',
'Nov',
'Dec']

years = "[1-9]+([0-9]*)"
days = "(([0-2]?[0-9])|(30|31))"
months_nums = "(((0)?[1-9])|(10|11|12))"

def cat_or(l):
    return '|'.join(l)

def cat_scape_or(l):
    return "(\||\-)".join(l)

def months():
    return "("+"("+cat_or(month_letters)+")"+"|"+"("+cat_or(month_letters_short)+")"+")"

def bracket(w):
    return "\[\["+w+"\]\]"

def optional_bracket(w):
    return "(\[\[)?"+w+"(\]\])?"

def option_c():
    return "(c\.)?"+space()

def space():
    return "( )*"

def birth_date():
    return "birth_date\t"

def one_char_trash():
    return space()+".?"

# defining sub-expressions

def accepts(fsa,word):
    return fsa.accepts(word)

# [[[month_letters_regex][ ][days]]],[ ][[[years]]]
def mdy_matcher():
    regex_string = birth_date()+optional_bracket(months()+space()+days)+"(,)?"+space()+optional_bracket(years)+one_char_trash()
    print regex_string
    fsa = compileRE(regex_string)
    return fsa

def dmy_matcher():
    regex_string = birth_date()+optional_bracket(days+space()+months())+"(,)?"+space()+optional_bracket(years)+one_char_trash()
    print regex_string
    fsa = compileRE(regex_string)
    return fsa

def year_matcher():
    regex_string = birth_date()+option_c()+optional_bracket(years)+one_char_trash()
    print regex_string
    fsa = fsa = compileRE(regex_string)
    return fsa

def ymd_matcher():
    l = [years,months_nums,days]
    regex_string = birth_date()+optional_bracket(cat_scape_or(l))+one_char_trash()
    print regex_string
    fsa = fsa = compileRE(regex_string)
    return fsa

# Uniting FSA (union)
def get_union_fsa():
    mdy_fsa = mdy_matcher()
    #print accepts(mdy_fsa, "birth_date\t[[October 14]], [[1964]]")

    dmy_fsa = dmy_matcher()
    #print accepts(dmy_fsa, "birth_date\t[[2 July]], [[1973]]")

    y_fsa = year_matcher()
    #print accepts(y_fsa, "birth_date\t1510")

    ymd_fsa = ymd_matcher()
    #print accepts(ymd_fsa, "birth_date\t1945|01|10")

    union1_fsa = union(mdy_fsa,dmy_fsa)
    union2_fsa = union(y_fsa, ymd_fsa)
    union_fsa = union(union1_fsa,union2_fsa)

    union_fsa = union_fsa.minimized()
    union_fsa = union_fsa.determinized()


    return union_fsa

def view_fsa(fsa):
    fsa.view()

def test_file(file=tfile):
    f = open(file)
    lines = f.readlines()

    lines = map(str.strip,lines)

    fsa = get_union_fsa()

    total_words = len(lines)
    count = 0
    for line in lines:
         b = accepts(fsa,line)
         if b:
             count = count+1
         #else:
         #    print line

    print "Accuracy: "+str(count*100/total_words)+"% "


