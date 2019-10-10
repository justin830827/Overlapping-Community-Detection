import networkx as nx

def IS2(cluster,G):
	cur = G.subgraph(cluster)
	W = float(2*nx.number_of_edges(cur)/nx.number_of_nodes(cur))
	increase = True
	while increase:
		print ("-----------------------------------------")
		N = cluster
		for vertex in cur.nodes:
			adj = G.neighbors(vertex)
			N = list(set(N).union(set(adj)))
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
		if new_W == W:
			increase = False
		else:
			W = new_W
	return list(cur.nodes)