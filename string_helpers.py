#!/usr/bin/python
# Copyright 2011, Wei Di.
# You are free to use, change, or redistribute the code in any 
# way you wish for non-commercial purposes, but please maintain 
# the name of the original author.
# This code comes with no warranty of any kind.

"""
    Function about string manipulation.
    
    Author:: Wei Di (vanessa.wdi@gmail.com)
    http://imiloainf.wordpress.com/
    Date:: 4-09-2011
    Python Version: 2.6
"""



def anagram_checker(aStringList):
    """
    Question: You are given an array of strings and you are asked to
    display all the anagrams within the array. For those who don't know,
    two words are anagrams if they contain the same characters.
    aStringList = ['abc', 'abc', 'abelrt', 'act', 'act', 'aegt', 'gorw']
    Anagrams in an Array of Strings 
    http://www.mytechinterviews.com/anagrams-in-array-of-strings
    """
    hash_res = list()
    for e in aStringList:
        hash_res.append(sum(map(ord, list(e))))  # note that chr vs. ord

    temp = hash_res[:]
    sorted(temp)

    same_hr = [e for (i, e) in enumerate(temp) if i <len(temp)-1 and e == temp[i+1]]
    for h in same_hr:
        inx = []
        i_hr = hash_res.index(h)
        a1 = aStringList[i_hr]

        hash_res.remove(h)
        i_hr = hash_res.index(h)
        b1 = aStringList[i_hr]
     
        return a1 == b1
 

def reverse_word_string(givenStr):
    """everse a string as per the words, not
    the entire reverse. eg; "I am Sam" --> "Sam am I" """
    return " ".join([e[::-1] for e in givenStr[::-1].split(" ")])
    

# check if a phrase is a palindrome
# tested with Python24      vegaseat     10sep2006

def isPalindrome(phrase):
    """
    take a phrase and convert to all lowercase letters and
    ignore punctuation marks and whitespaces,
    if it matches the reverse spelling then it is a palindrome
    """
    phrase_letters = [c for c in phrase.lower() if c.isalpha()]
    print phrase_letters  # test
    return (phrase_letters == phrase_letters[::-1])




def get_palindromes(aString):
    """ Return all palindromes in str of minimum size 3 """
    length = len(aString) + 1
    
    found = []
    for i in xrange(0, length):
        for j in xrange(i+3, length):
            mid = i + ((j - i) / 2)
            if aString[i:mid] == aString[mid+1:j][::-1]: # In-efficient
                found.append(aString[i:j])
    return found    

def find_logest_palindromes(aString):
    """ http://programmingpraxis.com/2010/10/15/find-the-longest-palindrome-in-a-string/ """


def find_sub_string(aString, subS):
    return (subS in aString,)
    lens = len(subS)
    for i in xrange(0, len(aString)-lens):
        if aString[i:i+lens] == subS:
            return True, i

    return False, None
           

def print_all_permutations(aString):
    """ Given a string, print all the permutation of the string"""
    ls = list(aString)
    print ls
    import itertools
    for e in itertools.permutations(ls, len(ls)):
        print e

def print_all_permuations_swap(slist, start=None, end = None):
    """do this as the most popular strategy"""
    if not isinstance(slist, list):
        slist = list(slist)
    if start is None: start = 0
    if end is None: end = len(slist)
    import random

    if start == end-1:
        print "".join(slist)
        #yield "".join(slist)
    for i in xrange(start,end-1):
        for j in xrange(i+1, end):
            slist[i], slist[j] = slist[j], slist[i] # random.choice(sString[i:])
            print_all_permuations_swap(slist, i+1, end)
            slist[j], slist[i] = slist[i], slist[j] # random.choice(sString[i:])
    

def minimum_editing(word_a, word_b, cost= None):
    import numpy as np
    
    if cost == None:
        cost = {'s':1, 'd':1, 'i':1}

   #  word-a --> word-b
    lena= len(word_a)
    lenb= len(word_b)
    pathM = np.zeros((lenb+1, lena+1))

    for i in xrange(lena+1):
        pathM[0][i] = i*cost['d']
    for j in xrange(1, lenb):
        pathM[j][0] = j*cost['s']

    for i in xrange(1, lena+1):
        for j in xrange(1, lenb+1):
            if word_a[i-1] == word_b[j-1]:
                substitude_cost = 0
            else:
                substitude_cost = 1
            pathM[j][i] = min(pathM[j-1][i] + cost['d'],
                              pathM[j-1][i-1] + cost['s']*substitude_cost,
                              pathM[j][i-1] + cost['i'])

    i = lena; j = lenb

    path = list()
    path.insert(0, (j, i, None))
    while i>1 and j>1:
        if word_a[i-1] == word_b[j-1]:
            substitude_cost = 0
        else:
            substitude_cost = 1
        templs = [ pathM[j-1][i] + cost['d'],
                   pathM[j-1][i-1] + cost['s']*substitude_cost,
                   pathM[j][i-1] + cost['i'] ]
        ix = templs.index(min(templs))
        if ix == 0:
            j = j-1;
            tag = 'd'
        elif ix ==1:
            j=j-1; i = i-1
            tag = 's'
        else:
            i = i-1
            tag = 'i'
        path.insert(0, (j, i, tag))

    while i>1:
        i = i-1
        tag = 'i'
        path.insert(0, (j, i, tag))
    while j>1:
        j = j-1
        tag = 'd'
        path.insert(0, (j, i, tag))
        
    return pathM[lenb][lena], path, pathM
        


########################################################
if __name__ == "__main__":
    
    aStringList = ['abc', 'abc', 'abelrt', 'act', 'act', 'aegt', 'gorw']
    print anagram_checker(aStringList)

    string_1 = 'My name is Anurag Singh'
    string_res = reverse_word_string(string_1)
    print "The revsersed str is : ", string_res   # results = Singh Anurag is name My

    phrase1 = "A man, a plan, a canal, Panama!"  # example with punctuation marks
    if isPalindrome(phrase1):
        print '"%s" is a palindrome' % phrase1
    else:
        print '"%s" is not a palindrome' % phrase1

    phrase2 = "Madam in Eden I'm Adam"
    if isPalindrome(phrase2):
        print '"%s" is a palindrome' % phrase2
    else:
        print '"%s" is not a palindrome' % phrase2

    print get_palindromes('efeababaf')

    aString = " because it does not ensure that Filename"
    subS = "ensure"
    br = find_sub_string(aString, subS)
    print "test contain sub-string: ",  br



    print "=== @ Test the Permutation === "
    print "All combinations of a string \n"
    print_all_permutations("love")
    ip = print_all_permuations_swap("love", start=None, end = None)




    print "=== @ Test the minimum-editing === "
    cost = {'s':1, 'd':1, 'i':1}
    cost, path , pathM = minimum_editing('cohen', 'mccohn', cost)  #target-word by source-word
    print "The total cost is %f" % cost
    print "The moving path is : ", path
    print pathM   #(size is len-target-word by len-source-word)
