#!/usr/bin/python
# Copyright 2009, Di, Wei.
"""
The file is mainly for path alignment.
	Author:: Di, Wei (vanessa.wdi@gmail.com)
	Date: 2009-9-14
	Python Version: 2.6
"""

def align(P, Q, dist):
    print """P, Q are lists of coordinates. dist is a function. 
    Returned are I, J, and their closeness
    where I and J are each a lit of indices. """
    

    #a = (.2, 1.5)
    #b = (0.2,1.5)
    #dict_ab = dist(a,b)
    #print dict_ab 

    # INITIALIZE VARIABLES.
    NUM_ROWS = len(P)
    NUM_COLS = len(Q)
    print NUM_ROWS
    print NUM_COLS
    
    
    # Create the DP tables fill it with zeros
    DP_table = createZeroTable(NUM_ROWS, NUM_COLS) 
    move_table = createZeroTable(NUM_ROWS, NUM_COLS)
    printTable(DP_table,'DP_table')


    DP_table[0][0] = dist(P[0], Q[0])
    print dist(P[0],Q[0])
    
    ### fill in the first row and colum of the DP_talbe
    col_index = 1
    while col_index < NUM_COLS:
          DP_table[0][col_index] = max2(dist(P[0], Q[col_index]), DP_table[0][col_index-1])  
          move_table[0][col_index] = 1
          col_index = col_index + 1

    row_index = 1
    while row_index < NUM_ROWS:
          DP_table[row_index][0] = max2(dist(P[row_index], Q[0]), DP_table[row_index-1][0])
          move_table[row_index][0] = 2
          row_index = row_index + 1

    row_index = 1
    while row_index < NUM_ROWS:
          col_index = 1
          while col_index < NUM_COLS:
                left = DP_table[row_index][col_index-1]
                above = DP_table[row_index-1][col_index]
                left_above = DP_table[row_index-1][col_index-1]
                
                min_d3 = min3(left, above, left_above)
                if min_d3 == left: move_table[row_index][col_index] = 1
                if min_d3 == above: move_table[row_index][col_index] = 2
                if min_d3 == left_above: move_table[row_index][col_index] = 3
                 
                dis_curr_PQ = dist(P[row_index], Q[col_index])

                DP_table[row_index][col_index] = max2(min_d3, dis_curr_PQ)
                col_index = col_index + 1
          row_index =  row_index + 1



    printTable(DP_table, 'DP_table')
    printTable(move_table, 'move_table')



    ### ---  NOW TRACEBACK  ---- ###
    I = []
    J = []
    I.insert(0,NUM_ROWS-1)
    J.insert(0,NUM_COLS-1)
    next_move = 999

    row_index = NUM_ROWS-1
    col_index = NUM_COLS-1

    while next_move >0:
          next_move = move_table[row_index][col_index]
          print next_move
          
          if next_move == 1: 
                I.insert(0,row_index) 
                J.insert(0,col_index-1)
                col_index = col_index - 1
          if next_move == 2:
                I.insert(0, row_index-1)
                J.insert(0, col_index)
                row_index = row_index -1
          if next_move == 3:
                I.insert(0, row_index-1)
                J.insert(0, col_index-1)               
                row_index = row_index -1
                col_index = col_index -1
          if next_move == 0:
                print 'this is the end of traceback'
         
                  
    print 'This is the I_trace: '
    print I
    print 'This is the J_trace: '
    print J


  ### compute the closeness of the alignment ###
    dPQ = close_seq_align(P,Q,I,J,dist)
    return I, J, dPQ


############### SOME DEFs ################

def createZeroTable(NUM_ROWS, NUM_COLS):
       new_table = []
       row_index = 0
       while row_index < NUM_ROWS:
             new_table.append([])
             col_index = 0
             while col_index < NUM_COLS:
                   new_table[row_index].append(0)
                   col_index = col_index + 1
             row_index = row_index + 1
       return new_table


def min3(a, b, c):
    if ((a <=b) and (a <=c)): return a
    if ((b <=a) and (b <=c)): return b
    return c

def max2(a,b):
    if a >= b: return a
    else: return b

def printTable(table, tableName):
    print '--- Below is the filled in table ' + tableName
    s = ""
    for i in range(0, len(table)):
           for j in range(0, len(table[0])):
                 s = s + str(table[i][j]) + "\t"
           s = s + "\n"
    print s

def close_seq_align(P,Q,I,J,dist):
    num_step = len(I)
    d_PQ = 0
    for i in range(num_step):
          P_index = I[i]
          Q_index = J[i]
          d_PQ = max2(d_PQ, dist(P[P_index], Q[Q_index]))
    return d_PQ


##########################################
############ THE MAIN PROGRAM ############
##########################################

if __name__ == '__main__':
    from math import sqrt, cos, pi, sin
    
    ### ---  this is the dist used in the alignment --- ### 
    def dist(p, q):
        dx = q[0] - p[0]; dy = q[1] - p[1]
        return sqrt(dx*dx + dy*dy)

    P = zip([0., 2., 3., 6., 8.], [1.]*5)   # P is the list of paris
    Q = zip([0., 2., 5., 6., 8.], [0.]*5)
    #print 'This is the input 2 point sequence:'
    #print 'The P sequcence is: '
    #print P
    #print 'The Q sequecnce is: '
    #print Q
    
    I1, J1, dPQ1 = align(P, Q, dist)
    print I1 == [0, 1, 2, 3, 3, 4]
    print J1 == [0, 1, 1, 2, 3, 4]
    print 1.413 < dPQ1 < 1.415

    m = 9
    x = [-1. + 2.*float(i)/float(m) for i in range(m)]
    y = [1.- abs(xi) for xi in x]
    P = zip(x,y)
    n = 5
    x  = [-cos(pi*float(i)/float(n-1)) for i in range(n)]
    y  = [0.8*sin(pi*float(i)/float(n-1)) for i in range(n)]
    Q = zip(x, y)
    I2,J2, dPQ2 = align(P, Q, dist)
    print I2 == [0, 1, 2, 3, 4, 5, 6, 7, 8]
    print J2 == [0, 0, 1, 2, 2, 2, 2, 3, 4]
    print 0.358 < dPQ2 < 0.360
    

    print 'this is the dPQ1: ' + str(dPQ1)
    print 'this is the dPQ2: ' + str(dPQ2)   

