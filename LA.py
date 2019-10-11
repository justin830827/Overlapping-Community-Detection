import networkx as nx
from weight import * 

def LA(G):
	clusters = []
	vertex = orderVertex(G)
	# vertex = G.nodes
	for v in vertex:
		add = False
		#current=G.subgraph(v)
		#print(list(current.edges))
		
		for j in range(len(clusters)):
			#tmp=clusters[j].copy()
			#U=nx.compose(tmp,current)
			U = clusters[j] + [v]
			#print(list(G.subgraph(U)))
			#print (nx.density(G.subgraph(U)),nx.density(G.subgraph(clusters[j])))
			UW = float(2 * nx.number_of_edges(G.subgraph(U)) / nx.number_of_nodes(G.subgraph(U)))
			W = float(2 * nx.number_of_edges(G.subgraph(clusters[j])) / nx.number_of_nodes(G.subgraph(clusters[j])))
			if UW > W:
				clusters[j] += [v]
				add = True
		if add == False:
			clusters.append([v])
		print(len(clusters))
	
	return clusters

