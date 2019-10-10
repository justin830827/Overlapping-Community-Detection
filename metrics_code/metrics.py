"""
This script does the following three things:
    (1) Calculate performance metrics: recall, precision, F-measure, specificity and RAND Index
    (2) Calculate performance metrics: Normalized Mutual Information
    (3) Calculate performance metrics: Density, ClusteringCoeff, Conductance, FlakeODF, FOMD, TPR, CutRatio, Cohesiveness, Separability

    NOTE1: The performance and goodness metrics will be output in two separate files
    NOTE2: This does pairwise comparison of nodes in communities so does not scale to large graphs

To run this code, execute: python metrics.py <graph_file> <groundtruth_file> <communities_file> <output_file>
where:
   	<graph_file> the file containing the edge list of the graph,
   	<groundtruth_file> is the file containing the ground truth communities,
    <communities_file> is the file containing the communities identified with the community detection algorithm
    <output_file> is the file prefix for the metrics results (two files will be created <output_file>.pmetrics.csv and <output_file>.gmetrics.csv
e.g., python metrics.py graph.txt ground_truth.txt communities.txt results
"""

import sys, os, inspect
import numpy
import math
import itertools
import time

""" Includes path to networkx package """
cmd_subfolder = os.path.realpath(os.path.abspath(os.path.join(os.path.split(inspect.getfile( inspect.currentframe() ))[0],"networkx")))
if cmd_subfolder not in sys.path:
    sys.path.insert(0, cmd_subfolder)
import networkx as nx

if not len(sys.argv)==5:
    print("python metrics.py <graph_file> <groundtruth_file> <communities_file> <output_file>")
    exit()

graphFile = open(sys.argv[1], "r")
groundTruth = open(sys.argv[2],'r')
foundCluster = open(sys.argv[3],'r')


""" Check if graph is 0-based or 1-based: we convert to 0-based """
minV = 1    # used to check if graphFile is 0-based or 1-based
for line in graphFile:  # Must loop over file since igraph doesn't work with isolated nodes
    u,v = [int(v) for v in line.split()]
    if u==0 or v==0:
        minV = 0
        break
graphFile.seek(0)


""" Reading Graph and creating object"""
numV, numEdges = [int(n) for n in graphFile.readline().split()]
graphObj = nx.Graph()
graphObj.add_nodes_from(range(numV)) # 0-based IDs
edges = []
for line in graphFile:  # Must loop over file since igraph doesn't work with isolated nodes
    edges.append(tuple([int(v)-minV for v in line.split()]))
graphObj.add_edges_from(edges)
graphFile.close()


sumGroudTruth = 0
sumFoundCluster = 0
sumBoth = 0
clusterOverlapTable = {}
groundTruthLines = groundTruth.readlines()
groundTruthLines = [line.strip() for line in groundTruthLines]
groundTruth.close() 
foundClusterLines = foundCluster.readlines()
foundClusterLines = [line.strip() for line in foundClusterLines]
foundCluster.close()
groundTruthSize = [0]*len(groundTruthLines)
foundClusterSize = [0]*len(foundClusterLines)
numberOfFoundCluster = len(foundClusterLines)
foundClusters = [None]*len(foundClusterLines)
groundTruths = [None]*len(groundTruthLines)

""" For printing out status """
NUM_PRINTS = 5
if len(groundTruths) < NUM_PRINTS:
    NUM_PRINTS = len(groundTruths)-1
if len(foundClusters) < NUM_PRINTS:
    NUM_PRINTS = len(foundClusters)-1

if NUM_PRINTS == 0:
    NUM_PRINTS = 1

INTERVAL_G = int(len(groundTruths)/NUM_PRINTS)
if len(groundTruths)%NUM_PRINTS==0:
    INTERVAL_G = INTERVAL_G + 1
MAXPRINT_G = INTERVAL_G*NUM_PRINTS

INTERVAL_F = int(len(foundClusters)/NUM_PRINTS)
if len(foundClusters)%NUM_PRINTS==0:
    INTERVAL_F = INTERVAL_F + 1
MAXPRINT_F = INTERVAL_F*NUM_PRINTS



""" Get in pairwise associations (TP, FP, TN, FN) """

vertexGroundTruthPairs = set()
vertexFoundClusterPairs = set()

i=0
loop_count = 1
start = time.time()
for line in groundTruthLines:
    if i%INTERVAL_G==0 and not i>=MAXPRINT_G:
        #print("PAIRWISE (GROUND TRUTHS): "+str(loop_count)+" of "+str(NUM_PRINTS)+". Runtime = "+str(round(time.time()-start,2)))
        loop_count+=1
    column = line.strip().split()
    groundTruths[i] = set([int(x)-minV for x in column])
    for S in list(itertools.combinations(sorted(column), 2)):
        vertexGroundTruthPairs.add(S)
    size = float(len(column))
    groundTruthSize[i] = size
    sumGroudTruth = sumGroudTruth+(size*math.log((size/numV)))    
    i+=1
  

i=0
loop_count = 1
start = time.time()
for line in foundClusterLines:
    if i%INTERVAL_F==0 and not i>=MAXPRINT_F:
        #print("PAIRWISE (FOUND COMMUNITIES): "+str(loop_count)+" of "+str(NUM_PRINTS)+". Runtime = "+str(round(time.time()-start,2)))
        loop_count+=1
    column = line.strip().split()
    foundClusters[i] = set([int(x)-minV for x in column])
    for S in list(itertools.combinations(sorted(column), 2)):
        vertexFoundClusterPairs.add(S)
    size = float(len(column))
    foundClusterSize[i] = size
    sumFoundCluster = sumFoundCluster+(size*math.log((size/numV)))   
    i+=1


""" PERFORMANCE METRICS """

TruePositive = float(len(vertexGroundTruthPairs.intersection(vertexFoundClusterPairs)))
FalsePositive = float(len(vertexFoundClusterPairs.difference(vertexGroundTruthPairs)))
FalseNegative = float(len(vertexGroundTruthPairs.difference(vertexFoundClusterPairs)))
#TrueNegative = (choose(numV,2))-(TruePositive+FalsePositive+FalseNegative)
TrueNegative = (numV*(numV-1)/2)-(TruePositive+FalsePositive+FalseNegative)

Recall = TruePositive/(TruePositive+FalseNegative)
Precision = TruePositive/(TruePositive+FalsePositive)
FMeasure = (2*Precision*Recall)/(Precision+Recall)
Specificity = TrueNegative/(TrueNegative+FalsePositive)
RANDIndex = (TruePositive+TrueNegative)/(TruePositive+FalsePositive+FalseNegative+TrueNegative)
    


""" NMI calculation (from paper: Normalized Mutual Information to evaluate overlapping community finding algorithms) """
def h(w,n):
	if w>0:
		return -w*math.log(w/n,2)
	else:
		return 0

def hstar(comm1,comm2):
	b=float(len(list(set(comm2)-set(comm1))))
	c=float(len(list(set(comm1)-set(comm2))))
	d=float(len(list(set(comm1)&set(comm2))))
	a=numV-b-c-d

	l1=float(len(comm2))
	l0=numV-l1

	k1=float(len(comm1))
	k0=numV-k1

	H=h(a,numV) + h(b,numV) + h(c,numV) + h(d,numV) - h(l1,numV) - h(l0,numV) 
	
	if h(a,numV)+h(d,numV) >=h(b,numV) + h(c,numV):
		Hstar=H
	else:
		Hstar=h(k1,numV)+h(k0,numV)

	return Hstar


HX=0
for comm in groundTruths:
    lc = float(len(comm))
    HX += h(lc,numV) + h(numV-lc,numV)

HY=0
for comm in foundClusters:
    lc = float(len(comm))
    HY += h(lc,numV) + h(numV-lc,numV)


HYX_list=[]
for comm1 in foundClusters:
	HstarYX_list=[]
	for comm2 in groundTruths:
		HstarYX=hstar(comm1,comm2)
		HstarYX_list.append(HstarYX)
	
	HYiX=min(HstarYX_list)
	HYX_list.append(HYiX)

HYX=sum(HYX_list)

I=HY-HYX
NMI=I/max(HX,HY)




#print("PMETRICS: DONE!")
   

pmFile = open(sys.argv[4]+".pmetrics.csv", "w") # output performance metrics file
pmFile.write("TP,FP,FN,TN,Recall,Precision,F-Measure,Specificity,RAND,NMI\n")
pmFile.write(str(int(TruePositive)))
pmFile.write(","+str(int(FalsePositive)))
pmFile.write(","+str(int(FalseNegative)))
pmFile.write(","+str(int(TrueNegative)))
pmFile.write(","+str(round(Recall,8)))
pmFile.write(","+str(round(Precision,8)))
pmFile.write(","+str(round(FMeasure,8)))
pmFile.write(","+str(round(Specificity,8)))
pmFile.write(","+str(round(RANDIndex,8)))
pmFile.write(","+str(round(NMI,8))+"\n")
pmFile.close()





""" GOODNESS METRICS """

gmFile = open(sys.argv[4]+".gmetrics.csv", "w") # output goodness metrics file
gmFile.write("CommunityID,Density,ClusteringCoeff,Conductance,FlakeODF,FOMD,TPR,CutRatio,Cohesiveness,Separability\n")

allDensity = 0.0
allClusteringCoeff = 0.0
allConductance = 0.0
allFlakeODF = 0.0
allFOMD = 0.0
allTPR = 0.0
allCR = 0.0
allCohesive = 0.0
allSep = 0.0

loop_count = 1
median_degree = numpy.median(graphObj.degree(graphObj.nodes()).values()) # used for FOMD metric
start = time.time()
for i in range(len(foundClusters)):
    """ Print Status """
    if i%INTERVAL_F==0 and not i>=MAXPRINT_F:
        #print("GMETRICS: "+str(loop_count)+" of "+str(NUM_PRINTS)+". Runtime = "+str(round(time.time()-start,2)))
        loop_count+=1
    
    singleDensity = 0.0
    singleClusteringCoeff = 0.0
    singleConductance = 0.0
    singleFlakeODF = 0.0
    singleFOMD = 0.0
    singleTPR = 0.0
    singleCR = 0.0
    singleCohesive = 0.0
    singleSep = 0.0

    column = foundClusters[i]
    vertexList = list(column)
    commSubgraph = graphObj.subgraph(vertexList)
    vCount = len(commSubgraph.nodes())
    
    inner_edges = [0]*vCount # holds inner community edges for ith vertex
    neighbors = [0]*vCount  # holds neighborhood size of ith vertex
    for j in range(vCount):
        v = vertexList[j]
        inner_edges[j] = len(set(graphObj.neighbors(v)) & set(vertexList))
        neighbors[j] = len(graphObj.neighbors(v))
    
    ms = float(len(commSubgraph.edges()))  # edges inside the subgraph
    cs = 0.0    # edges with one vertex outside of the subgraph
    for v in vertexList:
        cs += len(set(graphObj.neighbors(v)) - set(vertexList))

    
    """ Density """
    if vCount>1:
        singleDensity = nx.density(commSubgraph)
    	allDensity += singleDensity
    else:
        singleDensity = 1
    	allDensity = allDensity+1


    """ Clustering Coefficient """
    singleClusteringCoeff = nx.transitivity(commSubgraph)
    allClusteringCoeff = allClusteringCoeff+singleClusteringCoeff

    
    """ Conductance """
    if ms==0 and cs==0:
        singleConductance = 1
    else:
        singleConductance = cs/(2*ms+cs)
    allConductance += singleConductance


    """ FlakeODF """
    count = 0.0
    for j in range(vCount):
        if inner_edges[j] < neighbors[j]/2.0:   # check whether less edges pointing inside the subgraph than outside
            count += 1
    singleFlakeODF = count/vCount
    allFlakeODF += singleFlakeODF


    """ FOMD (Fraction Over Median Degree) """
    count = 0.0
    for j in range(vCount):
        if inner_edges[j] > median_degree:   # check whether interal degree larger than median
            count += 1
    singleFOMD = count/vCount
    allFOMD += singleFOMD

    
    """ TPR (Triangle Participation Ratio) """
    count = 0.0
    for v in vertexList:
        local_neighbors = list(set(graphObj.neighbors(v)) & set(vertexList))
        connected = False
        for j in range(len(local_neighbors)-1):
            for k in range(j,len(local_neighbors)):
                if graphObj.has_edge(local_neighbors[j], local_neighbors[k]):
                    connected = True
                    count += 1
                    break;
            if connected == True:
                break
    singleTPR = count/vCount
    allTPR += singleTPR
        

    """ CR (Cut Ratio) """
    singleCR = cs/(vCount*(numV-vCount))
    allCR += singleCR
    
    
    """ Cohesiveness (normalized edge cut)"""
    if vCount == 1:
        singleCohesive = 1
    elif not nx.is_connected(commSubgraph):
        singleCohesive = 0
    else:
        singleCohesive = float(len(nx.minimum_edge_cut(commSubgraph)))/(vCount-1)
    allCohesive += singleCohesive
    
    
    """ Separability (normalized edge cut)"""
    if cs == 0:
        singleSep = ms
    else:
        singleSep = ms/cs
    allSep += singleSep
    
    
    gmFile.write(str(i+1))
    gmFile.write(","+str(round(singleDensity,8)))
    gmFile.write(","+str(round(singleClusteringCoeff,8)))
    gmFile.write(","+str(round(singleConductance,8)))
    gmFile.write(","+str(round(singleFlakeODF,8)))
    gmFile.write(","+str(round(singleFOMD,8)))
    gmFile.write(","+str(round(singleTPR,8)))
    gmFile.write(","+str(round(singleCR,8)))
    gmFile.write(","+str(round(singleCohesive,8)))
    gmFile.write(","+str(round(singleSep,8)))
    gmFile.write("\n")
    
    

gmFile.close()


print('True Positive:\t'+str(round(TruePositive,8)))
print('False Positive:\t'+str(round(FalsePositive,8)))
print('False Negative:\t'+str(round(FalseNegative,8)))
print('True Negative:\t'+str(round(TrueNegative,8)))
print('Recall:\t'+str(round(Recall,8)))
print('Precision:\t'+str(round(Precision,8)))
print('F-Measure:\t'+str(round(FMeasure,8)))
print('Specificity:\t'+str(round(Specificity,8)))
print('RAND Index:\t'+str(round(RANDIndex,8)))
print('Normalized Mutual Information:\t'+ str(round(NMI,4)))
    
avgDensity = allDensity/numberOfFoundCluster
print("Avg Density:\t"+str(round(avgDensity,8)))
avgClusteringCoeff = allClusteringCoeff/numberOfFoundCluster
print("Avg Clustering Coefficient:\t"+str(round(avgClusteringCoeff,8)))
avgConductance = allConductance/numberOfFoundCluster
print("Avg Conductance:\t"+str(round(avgConductance,8)))
avgFlakeODF = allFlakeODF/numberOfFoundCluster
print("Avg FlakeODF:\t"+str(round(avgFlakeODF,8)))
avgFOMD = allFOMD/numberOfFoundCluster
print("Avg FOMD:\t"+str(round(avgFOMD,8)))
avgTPR = allTPR/numberOfFoundCluster
print("Avg TPR:\t"+str(round(avgTPR,8)))
avgCR = allCR/numberOfFoundCluster
print("Avg CR:\t"+str(round(avgCR,8)))
avgCohesive = allCohesive/numberOfFoundCluster
print("Avg Cohesive:\t"+str(round(avgCohesive,8)))
avgSep = allSep/numberOfFoundCluster
print("Avg Separability:\t"+str(round(avgSep,8)))
