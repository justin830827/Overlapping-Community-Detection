import networkx as nx
import operator

def weight(c):
    return float(2 * nx.number_of_edges(c) / nx.number_of_nodes(c))
# order the vertex by pagerank
def orderVertex(g):
    d = nx.pagerank(g)
    sorted_v = list(map(lambda x: x[0],sorted(d.items(), key = operator.itemgetter(1), reverse=True)))
    return sorted_v

