#!/usr/bin/python
# Copyright 2011, Wei Di.
# You are free to use, change, or redistribute the code in any 
# way you wish for non-commercial purposes, but please maintain 
# the name of the original author.
# This code comes with no warranty of any kind.

"""
    The module contains several helper functions
    related to tagging in nltk
    
    Author:: Wei Di (vanessa.wdi@gmail.com)
    http://imiloainf.wordpress.com/
    Date:: 2-15-2011
    Python Version: 2.6
"""

import nltk

def findtags(tag_prefix, tagged_text):
    """ Program to Find the Most Frequent selected Tags (such as NN) """
    """ An example:
    tagdict = findtags('NN', nltk.corpus.brown.tagged_words(categories='news'))
    >>> for tag in sorted(tagdict):
    ...     print tag, tagdict[tag]
    """
    cfd = nltk.ConditionalFreqDist((tag, word) for (word, tag) in tagged_text
                                  if tag.startswith(tag_prefix))
    return dict((tag, cfd[tag].keys()[:5]) for tag in cfd.conditions())


def find_tagged_phrase_3w(sentence, tag = ['V', 'TO', 'V']):
    """This is to search for Three-word Phrase """
    """ Original from nltk- process function
        The input "sentence" is a list, with each element a new list, that
        contains tuples (word, tag) for each word in the sentence.
        Notice that if you treat the whole text as one sentence, you
        can also use this program, however, at the boundary of the two true
        sentence, might be problems -- depend on your data
        we can use the string.split('.') to seperate the sentensces, or just
        put all the raw text in to it, since '.' wont' be recognitzed as a word
    """
    """ An example:
    from nltk.corpus import brown
    for tagged_sent in brown.tagged_sents():
        find_tagged_sents_3w(tagged_sent)

    spam3wP_AV, fd_spam3wP_AV = find_tagged_phrase_3w(totg_spam, tag = ['N', 'V', ['R','V']])
    """
    import nltk, pprint
    L_3wPhrase = [(w1, w2, w3)for (w1,t1), (w2,t2), (w3,t3) in nltk.trigrams(sentence)
                if (t1[0] in tag[0] and t2[0] in tag[1] and t3[0] in tag[2])]
    print "Your required searching tags are:" , tag
    fd_3wPhrase = nltk.FreqDist(L_3wPhrase)
    pprint.pprint(fd_3wPhrase.keys()[:min(10, len(fd_3wPhrase))])
    print "The length of all Phrase: ", len(L_3wPhrase)
    print "The size of the pharse set: ", len(fd_3wPhrase)
    return L_3wPhrase, fd_3wPhrase


def find_tagged_phrase_2w(sentence, tag = ['A','V']):
    import nltk, pprint
    L_2wPhrase = [(w1, w2)for (w1,t1), (w2,t2) in nltk.bigrams(sentence)
                if (t1.startswith(tag[0]) and t2.startswith(tag[1]))]
    fd_2wPhrase = nltk.FreqDist(L_2wPhrase)
    pprint.pprint(fd_2wPhrase.keys()[:min(10, len(fd_2wPhrase))])
    print "The length of all Phrase: ", len(L_2wPhrase)
    print "The size of the pharse set: ", len(fd_2wPhrase)
    return L_2wPhrase, fd_2wPhrase


def find_tagged_phrase_2w_filter(sentence, filter_a = lambda x: x[0]=='V', filter_b = lambda x: x[0]=='V'):
    """ Example:
    >>> filter_a = lambda x: x[0]=='N'   or filter_a = lambda x: x  --> this will give it always true
    >>> filter_b = lambda x: x[0]=='V'
    >>> spam2wP_NV, fd_spam2wP_NV = find_tagged_phrase_2w_filter(totg_spam, filter_a, filter_b)
    """
    import nltk, pprint
    L_2wPhrase = [(w1, w2) for (w1,t1), (w2,t2) in nltk.bigrams(sentence)
                  if (map(filter_a, t1)[0] and map(filter_b, t2)[0])]
    fd_2wPhrase = nltk.FreqDist(L_2wPhrase)
    pprint.pprint(fd_2wPhrase.keys()[:min(20, len(fd_2wPhrase))])
    print "The length of all Phrase: ", len(L_2wPhrase)
    print "The size of the pharse set: ", len(fd_2wPhrase)
    return L_2wPhrase, fd_2wPhrase
    
