# -*- coding: utf-8 -*-
#!/pkg/ldc/bin/python2.5
#-----------------------------------------------------------------------------
# Name:        auxiliar.py
#
# Author:      Horacio
#
# Created:     2013/09/10
# auxiliar scripts for labo 
#-----------------------------------------------------------------------------

user = 'horacioWindowsLSI'

import re
from string import *
import sys
from nltk import *

def importingBrownCorpusFromNLTK(outF):
    "importing tagged brown corpus from NLTK and writing on a file OutF"
    outF = open(outF,'w')
    from nltk.corpus import brown
    brown_news_tagged = brown.tagged_words(categories='news',simplify_tags=True)
    print 'size', len(brown_news_tagged)
    for i in brown_news_tagged:
        outF.write(i[0]+'\t'+i[1]+'\n')
    outF.close()

def getWordsFromFile(inF):
    "get a list of words from a text file"
    lines = map(lambda x:x.replace('\n','').lower(),open(inF).readlines())
    words=[]
    for line in lines:
        for word in line.split():
            words.append(word)
    print len(words),'words read'
    return words

def getTaggedWordsFromFile(inF):
    "get a list of pairs <word,POS> from a text file"
    lines = map(lambda x:x.replace('\n','').lower(),open(inF).readlines())
    words=[]
    for line in lines:
        word,pos = line.split('\t')
        words.append((word,pos))
    print len(words),'tagged words read'
    return words

def getTaggedWordsFromFileTuple(inF):
    "get a list of pairs <word,POS> from a text file"
    lines = map(lambda x:x.replace('\n','').lower(),open(inF).readlines())
    tagged_words=[]
    words = []
    for line in lines:
        word,pos = line.split('\t')
        tagged_words.append((word,pos))
        words.append(word)
    print len(words),'tagged words read'
    return (words,tagged_words)

def getTagsFromTaggedWords(l):
    "from a list of tagged words build a list of tags"
    return map(lambda x:x[1],l)

def countNgrams(l,inic,end=0):
    """
    From a list l (of words or pos), an inic position and an end position
    a tuple(U,B,T) of dics corresponding to unigrams, bigrams and trigrams are built
    """
    if end == 0:
        end = len(l)
    U={}
    B={}
    T={}
    U[(l[inic])]=1
    if (l[inic+1]) not in U:
        U[(l[inic+1])]=1
    else:
        U[(l[inic+1])]+=1
    B[(l[inic],l[inic+1])]=1
    for i in range(inic+2,end):
        if (l[i]) not in U:
            U[(l[i])]=1
        else:
            U[(l[i])]+=1
        if (l[i-1],l[i]) not in B:
            B[(l[i-1],l[i])] = 1
        else:
            B[(l[i-1],l[i])] +=1
        if (l[i-2],l[i-1],l[i]) not in T:
            T[(l[i-2],l[i-1],l[i])] = 1
        else:
            T[(l[i-2],l[i-1],l[i])] +=1
    return (U,B,T)
      
##importing tagged brown corpus from NLTK
##importingBrownCorpusFromNLTK("../corpus/taggedBrown.txt")

#taggedWords = getTaggedWordsFromFile("../corpus/taggedBrown.txt")
#enWords = getWordsFromFile("../corpus/en.txt")
#esWords = getWordsFromFile("../corpus/es.txt")
#tags = getTagsFromTaggedWords(taggedWords)
