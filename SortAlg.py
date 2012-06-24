#!/usr/bin/python

# You are free to use, change, or redistribute the code in any 
# way you wish for non-commercial purposes, but please maintain 
# the name of the original author.
# This code comes with no warranty of any kind.

"""
=====================================
Basic Sorting & Searching algorithms
=====================================
Author:: Wei Di (vanessa.wdi@gmail.com)
         http://imiloainf.wordpress.com/
Date:: Jan 25, 2010
List::
  * Bubble Sort
  * Selection Sort
  * Quick Sort
  * Merge Sort
  * Insertion Sort

  * Binary Search

Introduction::
    This program is about several sorting algorithms, we relaize thme in
    python. It looks much simplerly than the version in C/C++
    Still, a lot of space to imporve.
    Note that, some algorithms if can be made by using the python comprehension
    Their efficiency can be improved a lot.

    If do test, please use
    
    import time
    start = time.time()
    ... do something
    finish = time.time()
    print "The exe time used is: " + str(finish -start)
    
"""

# BOBBLE-SORT
def BubbleSort_wd(AList):
"""
# BOBBLE SORT
"""
    N = len(AList)
    for i in range(N-1):
        for j in range(N-1-i):
            if AList[j+1]< AList[j]:
                AList[j+1], AList[j] = AList[j], AList[j+1]
    return AList



# SELECTION SORT
def SelectionSort_wd(AList):
"""
# SELECTION SORT
"""
    N = len(AList)
    for i in range(N):
        for j in range(i+1,N):
            if AList[j] < AList[i]:
                AList[j], AList[i] = AList[i], AList[j]
    return AList            


# QUICK-SORT: worst-case: n^2, but average-case: O(nlong(n))
"""
Quick sort is the currently fastest know sorting algorithm, and is
often the best practical choice for soring.

Steps:: 
    - Divide: Partition S[p..r] into two subarrays S[p..q-1] and S[q+1..r]
    such that each element of S[p..q-1] is less than or equal to S[q],
    which is, in turn, less than or equal to each element of S[q+1..r].
    Compute the index q as part of this partitioning procedure

    - Conquer: Sort the two subarrays S[p...q-1] and S[q+1..r] by recursive
    calls to quicksort.

    -Combine: Since the subarrays are sorted in place, no work is needed
    to combing them: the entire array S is now sorted. 
"""
def QuickSort_wd(AList):
    if len(AList)<=1:
        return AList
    pivot = AList[0]
    less = [e for e in AList if e < pivot]
    equal =[e for e in AList if e == pivot]
    greater = [ e for e in AList if e> pivot]
    return QuickSort_wd(less) + equal + QuickSort_wd(greater)



# MERGE SORT o(nlog(n))
def MergeSort_wd(AList):
"""
Merge Sort is divide-and-conque recursive algorithm
A reference: http://www.codecodex.com/wiki/Merge_sort
"""
    N = len(AList)
    if N==1: return AList
    else:
        half = N/2
        return MergeCombine_wd(MergeSort_wd(AList[:half]), MergeSort_wd(AList[half:]))
    
def MergeCombine_wd(LeftList, RightList):
    N1 = len(LeftList)
    N2 = len(RightList)
    print LeftList
    print RightList
    tag = True
    MergedList = []
    i = j = 0
    while tag:
        if LeftList[i] < RightList[j]:
            MergedList.append(LeftList[i])
            i+=1
        else:
            MergedList.append(RightList[j])
            j+=1
        tag = (i<N1) and (j<N2)
    if i == N1:
        MergedList.extend(RightList[j:])
    if j == N2:
        MergedList.extend(LeftList[i:])
    return MergedList


# INSERTION SORT
def InsertionSort_wd(AList):
"""
Insertion sort belongs to the O(n2) sorting algorithms. Unlike many
sorting algorithms with quadratic complexity, it is actually applied
in practice for sorting small arrays of data.
ref: http://www.algolist.net/Algorithms/Sorting/Insertion_sort
"""
    N = len(AList)
    for i in range(1,N):
        j = i
        while (AList[j-1] > AList[j]) and j>0:
            AList[j-1], AList[j] = AList[j], AList[j-1]
            j -=1
            print j
    return AList


def swap_wd(a, b):
    return b, a

# BINARY-SEARCH
def BinarySearch_wdi(SortedList, target, start, end):
"""
binary-search sort algorithm
"""
    if start == end:
        return start
    pivot_index = start + (end-start)/2
    pivot = SortedList[pivot_index]
    if target == pivot:
        return pivot_index
    if target < pivot:
        return BinarySearch_wdi(SortedList, target, start, pivot_index)
    else:
        return BinarySearch_wdi(SOrtedList, target, pivot_index, end)
    




# FOR ALGORITHM TESTING
if __name__ == "__main__":
    testList = [3, 4, 9, 9, 12, 1, -5]

    # TEST THE BULLBLE SORT
    sortedBlist = BubbleSort_wd(testList[:])
    print "The original list is:", testList
    print "The sorted list is:", sortedBlist
    print "please input your own list:\n"
      
    
    # TEST THE SELECTION SORT
    sortedBlist = SelectionSort_wd(testList[:])
    print "The original list is:", testList
    print "The selection sorted list is:", sortedBlist

    # TEST THE MERGESORT
    sortedBlist = MergeSort_wd(testList[:])
    print "The original list is:", testList
    print "The Merged sorted list is:", sortedBlist

    # TEST THE MERGESORT
    sortedBlist = QuickSort_wd(testList[:])
    print "The original list is:", testList
    print "The Quick sorted list is:", sortedBlist

    # TEST THE Insertion 
    sortedBlist = InsertionSort_wd(testList[:])
    print "The original list is:", testList
    print "The Insertion sorted list is:", sortedBlist
    

    index_target = BinarySearch_wdi(sortedBlist, -5, 0, len(sortedBlist))
    print index_target

##    inputList = raw_input()
##    iList = [float(e) for e in inputList.split(" ") if e.isalnum()]
##    sortedBlist = BubbleSort_wd(iList)
##    print "The sorted list from your input is:", sortedBlist  




