#!/usr/bin/python
# Copyright 2011, Wei Di.
# You are free to use, change, or redistribute the code in any 
# way you wish for non-commercial purposes, but please maintain 
# the name of the original author.
# This code comes with no warranty of any kind.

"""
    The file is an implementation of the algorithm 
    of *the painters partition problem*
    posted at 
    http://www.ihas1337code.com/2011/04/the-painters-partition-problem.html
    
    Author:: Wei Di (vanessa.wdi@gmail.com)
    http://imiloainf.wordpress.com/
    Date:: 2-15-2011
    
    Note: To save the time, you may commet the print comment \
    in the cashed function, and do not use @time_dec"

"""



import functools
import pdb

def cached(func):
    cache = {}
    def template(*args): #: template is wrapper; func is wrapped
        key = str((func, )+args[1:])
        try:
          ret = cache[key]
        except KeyError:
          print "(&) un-recored key is %s" % key
          ret = func(*args)
          cache[key] = ret
        else:
          print "(#)found record key is %s " % key
          pass
        return ret

    functools.update_wrapper(template, func)
    return template



def time_dec(func):               # this is not necessary
    import time
    def wrapper(*arg, **kw):
        t = time.clock()
        res = func(*arg, **kw)
        print "The function ~ %s ~ cost:" % func.func_name, time.clock()-t
        return res
    return wrapper



@cached     # comment or non-comment this for non-dec/dec results
@time_dec
def partition(Alist,n,k):
    if n == 1:
        return Alist[0]
    if k == 1:     # only one part
        return sum(Alist[:n])

    # if not the base case:
    mlist = range(k-1, n-1)   # note here: we start from k-1, rather then 1 as posted in the original alg, see footnote1
    mlist.reverse()
    print mlist
    smallest = 10000
    for m in mlist:
        temp = max(partition(Alist, m, k-1), sum(Alist[m:n]))
        print "temp is ", temp
        if smallest > temp:
            print('Temp is better')
            smallest = temp
            print "Smallest is %f, and m is %d" % (smallest, m)
            print "n is %d, and k is %d" % (n, k)
    return smallest



###################################################
if __name__ == "__main__":
    """ Algorithm of *the painters partition problem*
    posted at http://www.ihas1337code.com/2011/04/the-painters-partition-problem.html)
    """
    import random
    import time
    
    n = 30              # no. of availabel Ai
    k = 5               # no of parts
    maxI = 500

    Blist = []
    
    for i in range(0,n):
        Blist.append(random.random() * maxI)
        
    #Alist = [100, 200, 300, 400, 500, 600, 700, 800, 900]
    #Alist = [300, 100, 200, 200, 130, 93, 50, 82, 270, 185]
    #Alist = [270.14180348516197, 481.91927298690047, 301.59281398069146, 293.80853208771816, 222.49451313775808, 298.14343079155316, 192.45057298633023, 287.82550708244423, 145.164751201379, 94.695664277178068, 93.364764127777562, 306.38658993430334, 328.32969449481442, 238.26549600469039, 44.912180597796834, 378.80196098321841, 438.3851854113874, 461.69050797314031, 421.2301115700912, 449.08656067893946]
    #n = len(Alist)      # no. of available Ai

    # we use the random part generate Alist, or we can just use this pre-generated list
    Alist = [461.54121991008839, 270.29996247402721, 195.64802511731244, 352.64169992720315, 137.81706065606357, 405.81435425393926, 424.74298259318357, 447.51948371333759, 294.90059176557992, 474.88243661606026, 289.84750537280297, 225.28155331557758, 330.12268931119451, 498.12891967678632, 458.47060897372802, 396.66254206511206, 41.186494098323699, 306.39155252035613, 243.22210098458342, 315.07367020573639, 422.5387878357576, 121.51781103092813, 365.74461039542388, 58.567146604258994, 110.23026843391426, 397.29148585528793, 166.26807460982772, 407.95654826682977, 50.303760108048102, 73.17924445615192]
    
    print "Alist is : \n", Alist

    # record the start time
    start_t = time.clock()

    # note that if n < len(Alist), the code still works, since it's recursive alg.
    final_cost = partition(Alist, n,k)    

    # record the final time
    end_t = time.clock()
    cost_t = end_t - start_t


    print "The cost time (dec) is %f: " % cost_t
    print "The cost (dec) is %f: " % final_cost


####### Results #########
##    Reuslts without decoration:
##        the cost time is 87.203112
##        the cost is 1823.762322
##    Reuslts with decoration:
##        the cost time is 4.010619
##        the cost is 1823.762322


######## FootNote 1 #########
##  In the original algorithm:
##      for (int j = 1; j <= n; j++)
##           best = min(best, max(partition(A, j, k-1), sum(A, j, n-1)));
##
##  we thought, k has to be smaller than the avialable Ai, i.e
##  m, which denote the partition for the current recursion, should
##  locate as the place in the Alist between (k-1, n), it should
##  not be even smaller than k-1,
##  so we start m from k-1, ranther than 1
