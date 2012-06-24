#!/usr/bin/python
# Copyright 2011, Wei Di.
# You are free to use, change, or redistribute the code in any 
# way you wish for non-commercial purposes, but please maintain 
# the name of the original author.
# This code comes with no warranty of any kind.

"""
    Basic Helper function relating to nltk.
    
    Author:: Wei Di (vanessa.wdi@gmail.com)
    http://imiloainf.wordpress.com/
    Date:: 2-15-2011
    Python Version: 2.6
"""

from __future__ import division
from operator import itemgetter

def generateFeture(tokens_message, fd_aDict, defaultBaseValue=None):
    if defaultBaseValue == None:
        defaultBaseValue = 1.0/sum(fd_aDict.values())
    return[fd_aDict.get(t, defaultBaseValue) for t in tokens_message]


def filterAlist(aList):
   """
    ('!', '$','!!','$$','!!!','$$$')
    """
    import nltk
    from nltk.corpus import stopwords
    stopwords = nltk.corpus.stopwords.words('english')
    specialSet1 = ('!', '$','!!','$$','!!!','$$$')
    specialSet2 = ('.', ',', ';','a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z', 'subject')
    specialSet3 = ('-', ':','=','"')
    ComnineSet = stopwords[:]
    ComnineSet.extend(list(specialSet2))
    ComnineSet.extend(list(specialSet3))
    return [w.lower() for w in aList if w.lower() in specialSet1 or w.lower() not in ComnineSet]

def delStopwords(tokens):
    import nltk
    from nltk.corpus import stopwords
    stopwords = nltk.corpus.stopwords.words('english')
    nonStopWords = [w for w in tokens if w.lower() not in stopwords]
    return nonStopWords, float(len(nonStopWords)) / len(tokens)


def fWDict(aDict, outfile):
    f = open(outfile, "w")
    for i,k in enumerate(aDict.keys()):
        f.write(repr(k))
##        for n in aDict[i]:
        f.write(' %s'%(repr(aDict.values()[i])))
        f.write('\n')
    f.close()
    return 0
