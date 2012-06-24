#!/usr/bin/python
# Copyright 2011, Wei Di.
# You are free to use, change, or redistribute the code in any 
# way you wish for non-commercial purposes, but please maintain 
# the name of the original author.
# This code comes with no warranty of any kind.

"""
    This is the module document contains several helper
    functions relating to building the Graph for phrase.
    
    Author:: Wei Di (vanessa.wdi@gmail.com)
    http://imiloainf.wordpress.com/
    Date:: 2-15-2011
    Python Version: 2.6
"""

from __future__ import division
import pprint

def build_Fre_Graph(fd_Praphse, a_graph={}):
    """
    To build a graph using dict mapping the relation
    between node(word) that has connection
    """
    keys =  fd_Praphse.keys()
    nr_keys = len(keys)
    lenphrase = len(keys[0])
    for akey in keys:
        fre = fd_Praphse[akey]
        print akey, ':', str(fre)
        for j_w in range(len(akey)-1):
            w=akey[j_w]
            addStuf = akey[j_w+1],
            addStuf *= fre
            if a_graph.has_key(w):
                a_graph[w]= a_graph[w] + addStuf
            else:
                a_graph.setdefault(w, addStuf)
    """ To build a graph with frequencies between node """
    max_weight = 0
    anothG=dict()
    for e in a_graph:
        w = a_graph[e]
        set_w = set(w)
        anothG[e] = dict()
        for s in set_w:
            nr = w.count(s)
            anothG[e].setdefault(s, nr)
            if nr>max_weight:
                max_weight = nr

    pprint.pprint(a_graph)
    pprint.pprint(anotherG)

    return a_graph, anothG, max_weight


def build_Graph_draw(anotherG, max_weight = None, nr = 20):
    import networkx as nx
    G = nx.Graph()
    keyofG = anotherG.keys()
    Sub_keyofG = keyofG[:nr]
    G.add_nodes_from(Sub_keyofG)

    if not max_weight:
        max_weight = 0.0
        print max_weight
        for k in Sub_keyofG:
            branch = anotherG[k]   # k = 'here'
            print branch.values()
            max_weight = max(max(branch.values()), max_weight)
    print max_weight
    for k in Sub_keyofG:
        branch = anotherG[k]   # k = 'here'
        maxb = max(branch.values())
        for k_branch in branch:
            if not G.has_node(k_branch):
                G.add_node(k_branch)
                weight = branch[k_branch]/max_weight
                pre_edge = G.get_edge_data(k,k_branch)
                if pre_edge:
                    weight += pre_edge
                G.add_edge(k,k_branch, {'weight':weight})
                
    for n, nbrs in G.adjacency_iter():
        for nbr,eatter in nbrs.items():
            data = eatter['weight']
            print(n, nbr, data)
    return G, max_weight


def draw_Graph(G, figPathName='GraphPlot', verbo = None, **kwargs):
    import matplotlib.pyplot as plt
    import networkx as nx
    nx.draw(G)
    plt.savefig(figPathName + '_1.png')
    print "Graph Figure 1 saved at: " + figPathName + '_1.png'
    if verbo:
        print "Close the showed figure, to continue...."
        plt.show()
    Gcc=nx.connected_component_subgraphs(G)[0]
    pos=nx.spring_layout(Gcc)
    plt.axis('off')
    nx.draw_networkx_nodes(Gcc,pos,node_size = kwargs.get('node_size', 20))
    nx.draw_networkx_edges(Gcc,pos,alpha= kwargs.get('alpha', 0.4))
    plt.savefig(figPathName + '_2.png')
    print "Graph Figure 2 saved at: " + figPathName + '_2.png'
    if verbo:
        print "Close the showed figure, to continue...."
        plt.show()
