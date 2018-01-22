print("STARTING FIRE ENGINE COMPANY LOCATION PROGRAM..")
def get_node_perc_covered(G, yet_to_cover):
	totnodes = 0.0
	covered_nodes = 0.0
	for n in G.nodes():
		totnodes = totnodes + 1 
		if(yet_to_cover[n] == 0):
			covered_nodes = covered_nodes + 1 
			
	perc_nodes_covered = float(covered_nodes*100)/float(totnodes) 
	return(perc_nodes_covered)
	
def get_pop_perc_covered(G, yet_to_cover):
	totpop = 0.0
	covered_pop = 0.0
	for n in G.nodes():
		totpop = totpop + G.node[n]['node_pop']
		if(yet_to_cover[n] == 0):
			covered_pop = covered_pop + G.node[n]['node_pop']
			
	perc_pop_covered = float(covered_pop*100)/float(totpop)
	return(perc_pop_covered)

def get_num_engines(G):
	ncount = 0	
	for n in G.nodes():
		if(G.node[n]['EngineLoc'] == 1):
			ncount = ncount + 1
			
	return(ncount)
	
def get_next_location(G, SP_Lengths, cover, yet_to_cover, HEUR):
	pop_wt_array = [0 for i in range(nnodes+1)]
	node_wt_array = [0 for i in range(nnodes+1)]
	composite_wt_array = [0 for i in range(nnodes+1)]
	
	for n1 in G.nodes():
		pop_wt_array[n1] = 0
		node_wt_array[n1] = 0
		composite_wt_array[n1] = 0
		for n2 in G.nodes():
			if((cover[n1][n2] == 1) and (yet_to_cover[n2] == 1)):
				pop_wt_array[n1] = pop_wt_array[n1] + G.node[n2]['node_pop']
				node_wt_array[n1] = node_wt_array[n1] + 1
				
		composite_wt_array[n1] = (node_wt_array[n1])*(pop_wt_array[n1])
	best_node = -1
	best_pop_wt = 0
	best_node_wt = 0
	best_composite_wt = 0
	for n in G.nodes():
		if (G.node[n]['EngineLoc'] == -1):
			if((HEUR == 1) and (pop_wt_array[n] > best_pop_wt)):
				best_pop_wt = pop_wt_array[n]
				best_node = n
			elif((HEUR == 2) and (node_wt_array[n] > best_node_wt)):
				best_node_wt = node_wt_array[n]
				best_node = n
			elif((HEUR == 3) and (composite_wt_array[n] > best_composite_wt)):
				best_composite_wt = composite_wt_array[n]
				best_node = n
	if(best_node == -1):
		for n in G.nodes():
			if ((best_pop_wt == 0)and (yet_to_cover[n] == 1)):
				print('SCENARIO WHERE 0 POP NODE IS BEST POP..')
				best_node = n
	return(best_node)
	
def get_num_to_cover(G, yet_to_cover):
	num_to_cover = 0
	for n in G.nodes():
		index = int(n)
		if(yet_to_cover[index] == 1):
			num_to_cover = num_to_cover + 1
			
	return(num_to_cover)
		
def get_fro_node(G, e):
	for n in G.nodes():
		if (int(n) == int(e[0])):
			return(n)
	return(-1)
	
def get_to_node(G, e):
	for n in G.nodes():
		if (int(n) == int(e[1])):
			return(n)
	return(-1)
	

import networkx as nx
G = nx.read_adjlist("adj-matrix-phillie.txt",create_using = nx.DiGraph(),nodetype = int)

print("Finished creating graph..")

print("PRINTING NODES...")
print(G.nodes())
print("PRINTING EDGES")
print(G.edges())


# START READING NODE WEIGHTS (= # FIRE INCIDENTS AT NODE)
F1 = open('Neigh-node-pops.txt')
for line in F1:
	line.rstrip()
	parts = line.split('	')
	cur_node = int(parts[0])
	cur_pop = int(parts[1])
	cur_X = float(parts[2])
	cur_Y = float(parts[3]) 
	cur_fnum = int(parts[4])
	for n in G.nodes():
		if(int(n) == cur_node):
			G.node[n]['node_pop'] = cur_pop
			G.node[n]['num_fires'] = cur_fnum
			G.node[n]['Xcor'] = cur_X
			G.node[n]['Ycor'] = cur_Y
			G.node[n]['EngineLoc'] = -1 
#print('PRINTING NODE POP, NUM_FIRES, XCOR, YCOR, EngineLocIndicator')	
#for n in G.nodes():
#	print(n, G.node[n]['node_pop'],G.node[n]['num_fires'], G.node[n]['Xcor'],G.node[n]['Ycor'], G.node[n]['EngineLoc'])

# END READING NODE WEIGHTS

#CREATE EDGE LENGTHS
for e1 in G.edges():
	#print(e1[0],e1[1]) 
	i = get_fro_node(G, e1)
	#print(e1[0],e1[1], i)
	j = get_to_node(G, e1)
	#print(e1[0],e1[1], j)
	
	
	xdiff = G.node[i]['Xcor'] - G.node[j]['Xcor']
	xdiff2 = xdiff*xdiff
	ydiff = G.node[i]['Ycor'] - G.node[j]['Ycor']
	ydiff2 = ydiff*ydiff
	dist = pow((xdiff2+ydiff2),0.5)
	G.edge[i][j]['weight'] = dist 
	
# FINISH CREATING EDGE LENGTHS
#for e in G.edges():
	#print(e[0],e[1],G.edge[e[0]][e[1]]['weight'])

	
SP_Lengths = nx.shortest_path_length(G,weight='weight')
#for n1 in G.nodes():
#	for n2 in G.nodes():
#		print(n1,n2,SP_Lengths[n1][n2])
MINS = int(input("Enter response time limit in mins (4-24 mins recommended):"))
SPEED = int(input("Enter fire engine speed: (20mph-heavy-traffic to 40-mph-light traffic conditions:)"))
DIST_THRESHOLD = float(float(SPEED*MINS)/60.0)
print(DIST_THRESHOLD)

# DEVELOP MATRIX FOR SET COVERING PROBLEM
nnodes = len(G.nodes())
cover = [[0 for i in range(nnodes+1)] for j in range(nnodes+1)]
yet_to_cover = [1 for i in range(nnodes+1)]
for n1 in G.nodes():
	#print('yet to cover for',n1, yet_to_cover[n1])
	for n2 in G.nodes():
		cover[n1][n2] = 0
		#print(n1,n2,SP_Lengths[n1][n2])
		if(SP_Lengths[n1][n2] <= DIST_THRESHOLD):
			cover[n1][n2] = 1
		#print(n1, n2, cover[n1][n2])

print('USER PLEASE SELECT A HEURISTIC TO SOLVE THE PROBLEM')
print('ENTER 1 IF HEURISTIC GUIDED BY POPULATION')
print('ENTER 2 IF HEURISTIC GUIDED BY # OF TERRITORIES COVERED')
print('ENTER 3 IF A COMBINATION OF POPULATION AND # TERRITORIES TO BE USED')
HEUR = int(input("ENTER HEURISTIC NUMBER VALUE(1-3):"))

num_to_cover = get_num_to_cover(G, yet_to_cover)
print('num_to_cover=',num_to_cover)

while (num_to_cover > 0) :
	n = get_next_location(G, SP_Lengths, cover, yet_to_cover, HEUR)
	print('LOCATE NEXT ENGINE COMPANY AT NODE...', n)
	G.node[n]['EngineLoc'] = +1
	ncount = get_num_engines(G)
	print(ncount,' ENGINE COMPANIES CURRENTLY...')	
	for n1 in G.nodes():
		if(cover[n][n1] == 1):
			yet_to_cover[n1] = 0
	pop_perc_covered = get_pop_perc_covered(G, yet_to_cover)
	print('POP PERC COVERED = ', pop_perc_covered)
	node_perc_covered = get_node_perc_covered(G, yet_to_cover)
	print('NODE PERC COVERED = ', node_perc_covered)
	num_to_cover = get_num_to_cover(G, yet_to_cover)
	print('num_to_cover=',num_to_cover)

ncount = get_num_engines(G)
print(ncount,' ENGINE COMPANIES CURRENTLY...')		
print('TIME THRESHOLD, ENGINE SPEED(mph), HEUR_VALUE,NUM_ENGINE_LOCS ')
print(MINS, SPEED,HEUR ,ncount)