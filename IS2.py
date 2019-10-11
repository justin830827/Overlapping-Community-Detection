import networkx as nx

def IS2(cluster,G):
	# Build a subgraph using input cluster
	cur = G.subgraph(cluster)
	# Calculate the current communication density
	W = float(2*nx.number_of_edges(cur)/nx.number_of_nodes(cur))
	increase = True
	# Continue iterate if there are any improvement of communication density 
	while increase:
		N = list(cur.nodes)
		# Use cluster as candidate set and find adjacent vertices. Append adjacent vertices to candidate set.
		for vertex in cur.nodes:
			adj = G.neighbors(vertex)
			N = list(set(N).union(set(adj)))
		# Iterate all vertex in candidate set to see if it improves communication density.
		for vertex in N:
			original_vertex = list(cur.nodes)
			if vertex in original_vertex:
				original_vertex.remove(vertex)
			else:
				original_vertex.append(vertex)
			if not original_vertex:
				new_cur_w=0
			else:
				new_cur = G.subgraph(original_vertex)
				new_cur_w = float(2 * nx.number_of_edges(new_cur) / nx.number_of_nodes(new_cur))
			cur_w = float(2 * nx.number_of_edges(cur) / nx.number_of_nodes(cur))
			if new_cur_w > cur_w:
				cur = new_cur.copy()
		new_W = float(2 * nx.number_of_edges(cur) / nx.number_of_nodes(cur))
		# If the new communication density do not increase, then it is converge.
		if new_W == W:
			increase = False
		else:
			W = new_W
	#Return new cluster
	return list(cur.nodes)