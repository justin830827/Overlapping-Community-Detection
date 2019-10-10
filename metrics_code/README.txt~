The notion of “good” communities will be tested using the following performance metrics:
	-Separability: captures the intuition that good communities are well-separated from the rest of the network.
	-Density: builds on the intuition that good communities are well connected.
	-Cohesiveness: characterizes the internal structure of the community. Intuitively, a good community should be internally well and evenly connected, i.e., it should be relatively hard to split a community into two subcommunities.
	-Clustering coefficient: is a measure of the degree to which the nodes in a graph tend to cluster together.

The conformance of the identified communities to the ground truth communities will be tested using the following performance metrics:
	-Precision
	-Recall
	-F-measure
	-Specificity
	-RAND Index
	-Normalized Mutual Information


To run these codes, execute the following commands:
	python metrics.py <graph_file> <groundtruth_file> <communities_file> <output_file>
where,
	-graph_file is the file containing the edge list of the graph with the first line specifying number of nodes and number of edges
	-groundtruth_file is the file containing the ground truth communities, communities_file is the file containing the communities identified with the community detection algorithm
	-output_file is the prefix of the file where the performance metrics and goodness metrics will be written -- <output_file>.pmetrics.csv and <output_file>.gmetrics.csv respectively.
The average metrics will also be printed to the console.

An example dataset you can use to test these codes, is included in the folder. These include:
	A graph - graph.txt
	The ground truth communities of the graph - ground_truth.txt
	The communities found from a community detection algorithm - communities.txt

The command python metrics.py graph.txt ground_truth.txt communities.txt results will print the results to the screen and also write some of the results to files results.pmetrics.csv and results.gmetrics.csv.
