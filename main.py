'''
Implementation Paper: 
Efficient Identification of Overlapping Communities

Team member:
Wen-Han Hu (whu24)
Yang-Kai Chou (ychou3)
'''

import networkx as nx
import numpy as np
import sys
from LA import *
from IS2 import *

def main():
    # Read the data from file 
    file = sys.argv[1] # Note file needs to have the complete path to file
    g = nx.Graph()
    with open(file) as f:
        next(f)
        for line in f:
            line = line.split()
            g.add_edge(int(line[0]),int(line[1]))
    # print ("number of nodes",len(g))

    clusters = LA(g)
    final_clusters = []
    for cluster in clusters:
        final_clusters.append(IS2(cluster, g))
    print (final_clusters)
    print (len(final_clusters))

if __name__ == "__main__":
    main()