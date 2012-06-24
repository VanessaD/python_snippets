#!/usr/bin/python
# Copyright 2011, Wei Di.
# You are free to use, change, or redistribute the code in any 
# way you wish for non-commercial purposes, but please maintain 
# the name of the original author.
# This code comes with no warranty of any kind.

"""
The file is mainly for serialize and deserialize binary tree.

    Author:: Wei Di (vanessa.wdi@gmail.com)
    http://imiloainf.wordpress.com/
    Date:: 2-15-2011
    Python Version: 2.6

============
Method List
============

Method 1::
------------
    contains function:
        serialize_bt( pre-order serialize), de_serialize_bt

Method 2::
------------
    Contains functions:
        serialize_bt_p, de_serialize_bt_p
        
    Notes: since this one only use the parenthesis, it will lose the structure if there
    is only one children, so when reconstruct, no information can be recoverd (see example 2).
    To fix this, in the de-serialization part, we assume that if only one child, it will
    be the right child. 
    
    + Example 1, A tree below can be serialized as

                   12
                /      \
              10       18
              / \     /  \
             8  11   14  20
             
     Serialized results: ( 12 (10 (8 11) 18( 14 20) ) )


    + Example 2, A tree below can be serialized as

                   98
                /      \
              76       32
              / \     /  \
             51  27 None  4
                  \
                   3
             
     Serialized results: ( 98 ( 76 (51 27 ( 3 )) 32 (4) ) )


Method 3::
------------

    Contains functions:
        serialize_bt_p2, de_serialize_bt_p2
        
    Notes: This one will add None value to represnet the non-exist children, so when
    reconstructe, it will be able to discirminate the right/left children
    
    + Example 2, A tree below can be serialized as

                   98
                /      \
              76       32
              / \     /  \
             51  27 None  4
                  \
                   3
             
     Serialized results: ( 98 ( 76 (51 ( None None ) 27 ( None 3 (None None ) ) ) 32 ( None 4 ( None None ) ) )
    
"""
##############################
# Baisc Tree & Node Structure
##############################
class TreeNode():
    	def __init__(self, val=None, left = None, right = None):
    	  self.val = val
    	  self.left = left
    	  self.right = right


def build_tree(sequence, low, high):
    """
    Used to build a somehow 'balanced tree', if the input sequence
    is sorted, it will be a binary search tree
    """
    if low > high:
        return None
    if low == high:
        return TreeNode(sequence[low])
    mid = (low + high)/2
    node = TreeNode(sequence[mid])
    node.left = build_tree(sequence, low, mid -1)
    node.right = build_tree(sequence, mid + 1, high)
    return node

def printTreebyLevel(rootnode):
    """Print the tree by level"""
    thisL_n = [rootnode]
    while thisL_n:
        nextL_n = list()
        thisL_v = list()
        [(thisL_v.append(n.val), nextL_n.append(n.left), nextL_n.append(n.right)) for n in thisL_n if n]
        if thisL_v:
            print thisL_v, '\n'
        thisL_n = nextL_n

#############################
# Baisc Tree Implementation
#############################
def inorder_traverse(node, nodeList):
    if not node:
        return nodeList
    nodeList = inorder_traverse(node.left, nodeList)
    nodeList.append(node.val)
    nodeList = inorder_traverse(node.right, nodeList)
    return nodeList

def preorder_traverse(node,nodeList = list()):
    if not node:
        return nodeList
    nodeList.append(node.val)
    preorder_traverse(node.left, nodeList)
    preorder_traverse(node.right, nodeList)
    return nodeList


#############################################
#### Method-1 -- Serialize/de-Serialize   ###
#############################################
def serialize_bt(tree_node, sequence = list(), keyForNone = None):
    """ serialize_bt( pre-order serialize) """
    if not tree_node:
        return sequence.append(keyForNone)
    else:
        sequence.append(tree_node.val)
        serialize_bt(tree_node.left, sequence, keyForNone = None)
        serialize_bt(tree_node.right, sequence, keyForNone = None)
    return sequence

def de_serialize_bt(sequence, keyForNone = None):
    e = sequence.pop(0)
    if e == keyForNone:
        return
    else:
        node = TreeNode(e)
        node.left = de_serialize_bt(sequence, keyForNone)
        node.right = de_serialize_bt(sequence, keyForNone)
    return node
    


#############################################
#### Method-2 -- Serialize/de-Serialize   ###
#############################################
def serialize_bt_p(tree_node, sequence = list()):
    if not sequence:        
        sequence.append('(')
    if not tree_node:
        return sequence
    else:
        sequence.append(tree_node.val)
        sequence.append('(')
        serialize_bt_p(tree_node.left, sequence)
        serialize_bt_p(tree_node.right, sequence)
        sequence.append(')')
    return sequence

def de_serialize_bt_p(sequence):
    Stack = list()
    node_sequence = [TreeNode(e) for e in sequence]
    for (i, e) in enumerate(node_sequence):
        if e.val !=')':
            Stack.append(e);
        else:
            if Stack[len(Stack)-1].val == '(':
                del Stack[len(Stack)-1]
            else:
                # print "current stack:", "at stage", i, ' ---', [s.val for s in Stack]
                node_r = Stack[len(Stack)-1]
                del Stack[len(Stack)-1]
                if Stack[len(Stack)-1].val != '(':
                   node_l = Stack[len(Stack)-1]
                   del Stack[len(Stack)-1]
                   del Stack[len(Stack)-1]    # delte the '('
                   Stack[len(Stack)-1].left = node_l
                   Stack[len(Stack)-1].right = node_r
                   # print "current stack:", "at stage", i, ' ---', [s.val for s in Stack]
                else:
                    if len(Stack) == 1:
                        return node_r
                    del Stack[len(Stack)-1]    # delte the '('
                    Stack[len(Stack)-1].right = node_r
                    Stack[len(Stack)-1].left = None
    return Stack[1]

#############################################
#### Method-3 -- Serialize/de-Serialize   ###
#############################################

def serialize_bt_p2(tree_node, sequence = list(),keyForNone = None):
    if not sequence:        
        sequence.append('(')
    if not tree_node:
        sequence.append(keyForNone)
    else:
        sequence.append(tree_node.val)
        sequence.append('(')
        serialize_bt_p2(tree_node.left, sequence,keyForNone)
        serialize_bt_p2(tree_node.right, sequence,keyForNone)
        sequence.append(')')
    return sequence

def de_serialize_bt_p2(sequence):
    Stack = list()
    node_sequence = [TreeNode(e) for e in sequence]
    for (i, e) in enumerate(node_sequence):
        if e.val !=')':
            Stack.append(e);
        else:
            node_r = Stack[len(Stack)-1]
            del Stack[len(Stack)-1]
            node_l = Stack[len(Stack)-1]
            del Stack[len(Stack)-1]
            del Stack[len(Stack)-1]    # delte the '('
            Stack[len(Stack)-1].left = node_l
            Stack[len(Stack)-1].right = node_r
    return Stack[1]




#############################################
####                Test                  ###
#############################################

if __name__ == "__main__":

    ###### """ Example 1 """ ######
    """
        Example 1, A tree below can be serialized as

                   12
                /      \
              10       18
              / \     /  \
             8  11   14  20
             
         Serialized results: ( 12 (10 (8 11) 18( 14 20) ) )
    """
    print("\n \n  ====== Example 1  ======  ")
    sequence1 = [8, 10, 11, 12, 14, 18, 20]
    tree1 = build_tree(sequence1, 0, len(sequence1) -1)
    print "The original tree 1: \n", printTreebyLevel(tree1)

    
    inorderT2_result = inorder_traverse(tree1, [])
    preorderT2_result = preorder_traverse(tree1, [])

    """ Test on Tree 1 for method 1 """
    m1_tree1_seq = serialize_bt(tree1,[], keyForNone = None)
    m1_tree1_reconT = de_serialize_bt(m1_tree1_seq[:], keyForNone = None)
    print " \n $ Serialized results (Tree 1 - Method 1): \n ", m1_tree1_seq
    print " \n $ De-serialized Tree (Tree 1 - Method 1): \n ", printTreebyLevel(m1_tree1_reconT)

    """ Test on Tree 1 for method 2 """
    m2_tree1_seq = serialize_bt_p(tree1,[])
    m2_tree1_reconT = de_serialize_bt_p(m2_tree1_seq[:])
    print " \n $ Serialized results (Tree 1 - Method 2): \n", m2_tree1_seq
    print " \n $  De-serialized Tree (Tree 1 - Method 2): \n ", printTreebyLevel(m2_tree1_reconT)

    """ Test on Tree 1 for method 3 """
    m3_tree1_seq = serialize_bt_p2(tree1,[], keyForNone = None)
    m3_tree1_reconT = de_serialize_bt_p2(m3_tree1_seq[:])
    print " \n $ Serialized results (Tree 1 - Method 2): \n", m3_tree1_seq
    print " \n $ De-serialized Tree (Tree 1 - Method 2): \n ", printTreebyLevel(m3_tree1_reconT)


    ######       """ Example 2 """    ###### 
    # note that we use differnet way to build the tree
    """
        Example 2, A tree below can be serialized as

                   98
                /      \
              76       32
              / \     /  \
             51  27 None  4
                  \
                   3
             
         Serialized results: ( 98 ( 76 (51 27 ( 3 )) 32 (4) ) )
     """
    
    print(" \n \n ====== Example 2  ====== ")
    sequence2 = ['(', 98, '(', 76, '(', 51, 27 , '(', 3, ')', ')', 32, '(', 4, ')', ')', ')']
    tree2 = de_serialize_bt_p(sequence2[:])
    print "The original tree 2: \n", printTreebyLevel(tree2)
    
    inorderT2_result = inorder_traverse(tree2, [])
    preorderT2_result = preorder_traverse(tree2, [])

    """ Test on Tree 2 for method 1 """
    m1_tree2_seq = serialize_bt(tree2,[], keyForNone = None)
    m1_tree2_reconT = de_serialize_bt(m1_tree2_seq[:], keyForNone = None)
    print " \n $ Serialized results (Tree 2 - Method 1): \n ", m1_tree2_seq
    print " \n $ De-serialized Tree (Tree 2 - Method 1): \n ", printTreebyLevel(m1_tree2_reconT)

    """ Test on Tree 2 for method 2 """
    m2_tree2_seq = serialize_bt_p(tree2,[])
    m2_tree2_reconT = de_serialize_bt_p(m2_tree2_seq[:])
    print " \n $ Serialized results (Tree 2 - Method 2): \n  ", m2_tree2_seq
    print " \n $ De-serialized Tree (Tree 2 - Method 2): \n ", printTreebyLevel(m2_tree2_reconT)

    """ Test on Tree 2 for method 3 """
    m3_tree2_seq = serialize_bt_p2(tree2,[], keyForNone = None)
    m3_tree2_reconT = de_serialize_bt_p2(m3_tree2_seq[:])
    print " \n $ Serialized results (Tree 2 - Method 3): \n ", m3_tree2_seq
    print " \n $ De-serialized Tree (Tree 2 - Method 3): \n ", printTreebyLevel(m3_tree2_reconT)

    
    ######       """ Example 3 """    ###### 
    # note that we use differnet way to build the tree
    """
        Example 2, A tree below can be serialized as

             98
               \    
               76     
                 \
                 51
             
         Serialized results: ( 98 ( 76 ( 51 ) ) )
    """
    print("\n \n  ======  Example 3  ======  ")
    sequence3 = ['(', 98, '(', 76, '(', 51, ')', ')', ')']
    tree3 = de_serialize_bt_p(sequence3[:])
    print "The original tree 3: \n", printTreebyLevel(tree3)
    
    """ Test on Tree 3 for method 1 """
    m1_tree3_seq = serialize_bt(tree3,[], keyForNone = None)
    m1_tree3_reconT = de_serialize_bt(m1_tree3_seq[:], keyForNone = None)
    print " \n $ Serialized results (Tree 3 - Method 1): \n ", m1_tree3_seq
    print " \n $ De-serialized Tree (Tree 3 - Method 1): \n ", printTreebyLevel(m1_tree3_reconT)

    """ Test on Tree 3 for method 2 """
    m2_tree3_seq = serialize_bt_p(tree3,[])
    m2_tree3_reconT = de_serialize_bt_p(m2_tree3_seq[:])
    print " \n $ Serialized results (Tree 3 - Method 2): \n", m2_tree3_seq
    print " \n $ De-serialized Tree (Tree 3 - Method 2): \n ", printTreebyLevel(m2_tree3_reconT)

    """ Test on Tree 3 for method 3 """
    m3_tree3_seq = serialize_bt_p2(tree3,[], keyForNone = None)
    m3_tree3_reconT = de_serialize_bt_p2(m3_tree3_seq[:])
    print " \n $ Serialized results (Tree 3 - Method 3): \n ", m3_tree3_seq
    print " \n $ De-serialized Tree (Tree 3 - Method 3): \n ", printTreebyLevel(m3_tree3_reconT)


#############################################
####            Test  Part II             ###
#############################################
    
    ######   Show an Example for Writing to File     #####
    # """ we write the results of Tree 2 by method 1 """ #
    path_file_name = 'C:/TEMP/workfile'
    f = open(path_file_name, 'w')
    for e in m1_tree2_seq:
        f.write(str(e) + ' ')
    f.close()

    with open(path_file_name, 'r') as f:
        read_data = f.read()
    seq_r = read_data.split()   # correspond to m1_tree2_seq
    for (i, e) in enumerate(seq_r):
        if e == 'None':
            seq_r[i] = None
        elif e.isalnum():
            seq_r[i] = int(e)
        
        
    m2t2_r = de_serialize_bt(seq_r[:])
    print " \n $ r/w example - Serialized (Tree 2 - Method 1): \n  ", seq_r
    print " \n $ r/w Example - De-serialized (Tree 2 - Method 1): \n ", printTreebyLevel(m2t2_r)

