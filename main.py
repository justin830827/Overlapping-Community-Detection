'''
Implementation Paper: 
Efficient Identification of Overlapping Communities

Team member:
Wen-Han Hu (whu24)
Yang-Kai Chou (ychou3)
'''

import networkx as nx
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
    # Run the first part of algorithm
    clusters = LA(g)
    final_clusters = []
    # Run the second part of algorithm
    for cluster in clusters:
        final_clusters.append(IS2(cluster, g))
    # Remove duplicate cluster
    final_without_duplicates = []
    for fc in final_clusters:
        fc = sorted (fc)
        if fc not in final_without_duplicates:
            final_without_duplicates.append(fc)
    # Write to file
    with open("output.txt", 'w') as f:
        for fwd in final_without_duplicates:
            line = " ".join(map(str, fwd))
            f.write(line + '\n')


if __name__ == "__main__":
    main()