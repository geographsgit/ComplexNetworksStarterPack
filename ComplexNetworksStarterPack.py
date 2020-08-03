import numpy as np
import igraph as ig
import networkx as nx



class ComplexNetworksStarterPack:
	'''
	This class offers examples on how to build a network from data, compute some metrics and export the results
	'''

	def __init__(self):
		pass


	def plot_net(self,name, npixels):
		'''Network plotting
		:param g: graph
		:param name: name to save
		:param npixels: size of the figure in pixels
		'''

		print(' Plotting...')

		# The layout defines the 2D coordinates for the nodes
		# In case your nodes have predefined spatial coordinates, lyt must receive them as a list
		lyt = 'fr' #other preset options: 'kk','fr', 'rt', 'rt_circular', 'drl'

		layout = self.g_ig.layout(lyt)

		self.g_ig.vs["label_dist"] = 1

		# plotting network  -----------
		visual_style = {}
		#visual_style["vertex_size"] = g.vs["size"]
		visual_style["vertex_label"] = self.g_ig.vs["label"]
		visual_style["layout"] = layout
		visual_style["bbox"] = (npixels, npixels)
		visual_style["margin"] = 30

		# if you remove the file name, it loads the plot in the RAM memory, then one must use ig.show() to display it.
		ig.plot(self.g_ig, 'output/plot/' + lyt + '_' + name + '.png', **visual_style)




	def export_data(self, g, stat, data, graph_lib):
		'''Export metrics to the output folder
		:param g: graph
		:param stat: name of the metric
		:param data: data to be exported
		:param graph_lib: Either igraph or networkx
		'''

		stat_array = []

		# whether it is an igraph or a networkx graph
		if(graph_lib == 'igraph'):
			for i in range(len(data)):
				stat_array.append( ( float(g.vs['label'][i]), float(data[i]) ) )
		else:
			for key in data:
				stat_array.append( ( key, float(data[key]) ) )

		# sorting
		dtype = [('label', float), ('stat', float)]
		stat_array = np.array(stat_array, dtype=dtype)
		stat_array = np.sort(stat_array, order='label')

		# exporting
		file_out = open('output/metrics/' + stat + '.csv', 'w')
		for i in range(len(stat_array)):
			file_out.write(str( stat_array[i][0]) + ';' + str(stat_array[i][1]) + '\n')
		file_out.close()


	def build_network(self,file_name):
		''' 
		Build the network from input data, which is either an adjacency/weights matrix or an adjacency list 
		:param file_name: file name
		'''

		print(' Building the network...')

		# How to open using Adjacency/weights matrix
		#A = np.genfromtxt(file_name,delimiter=';') # semicolon separated data

		# Build the network from Adjacency matrix (igraph)
		#g_ig = ig.Graph.Weighted_Adjacency(A.tolist(), mode=ig.ADJ_MAX)

		# Build the network from Adjacency matrix (networkx)
		# g_nx = nx.from_numpy_matrix(A)


		# Adjacency list
		self.A_list = np.genfromtxt('input/' + file_name, delimiter=',') # comma separated data

		# Build the network (igraph library)
		self.g_ig = ig.Graph.TupleList(edges=self.A_list.tolist(), directed=False, vertex_name_attr='label', edge_attrs=None, weights=False)

		# Build the network (networkx library)
		self.g_nx = nx.Graph(self.A_list.tolist())

		# Number of nodes
		self.N = self.g_ig.vcount()


	def compute_metrics(self):
		'''
		Compute some network metrics
		'''

		print(' Metrics...')

		print('   STRENGTH')
		A = self.g_ig.get_adjacency()
		node_str = np.zeros(self.N)
		for i in range(self.N):
			node_str[i] = np.sum( A[i,:] )
		self.export_data(self.g_ig,'strength',node_str,'igraph')

		# Metrics from igraph

		print('   DEGREE')
		degrees = self.g_ig.degree()
		self.export_data(self.g_ig,'degree', degrees, 'igraph')

		print('   BETWEENNESS')
		betweenness = self.g_ig.betweenness(vertices=None, directed=False, cutoff=None)
		#betweenness = g_ig.betweenness(vertices=None, directed=False, cutoff=None, weights='weight')
		self.export_data(self.g_ig,'betweenness', betweenness, 'igraph')     

		print('   AUTHORITY')
		authority = self.g_ig.authority_score(weights=None, scale=True, return_eigenvalue=False)
		self.export_data(self.g_ig,'authority', authority, 'igraph')

		print('   CLUSTERING COEFF.')
		cluster_coeff = self.g_ig.transitivity_local_undirected(vertices=None, mode="zero", weights=None)
		#cluster_coeff = g_ig.transitivity_local_undirected(vertices=None, mode="zero", weights='weight')
		self.export_data(self.g_ig,'clusterCoeff', cluster_coeff, 'igraph')


		# Metrics from Networkx

		print('   CLOSENESS')
		closeness = nx.closeness_centrality(self.g_nx, u=None, distance=None, wf_improved=True)
		self.export_data(self.g_ig,'closeness', closeness, 'networkx')

		print('   EIGENVECTOR CENTRALITY')
		eig_centrality = nx.eigenvector_centrality(self.g_nx, max_iter=1000, tol=1e-06, nstart=None, weight=None)
		self.export_data(self.g_ig,'eig_centrality', eig_centrality, 'networkx')

		print('   HARMONIC CENTRALITY')
		harmonic_centrality = nx.harmonic_centrality(self.g_nx, nbunch=None, distance=None)
		self.export_data(self.g_ig,'harmonic_centrality', harmonic_centrality, 'networkx')

		print('   PAGERANK')
		pagerank = nx.pagerank(self.g_nx, alpha=0.85, personalization=None, max_iter=100, tol=1e-06, nstart=None, weight='weight', dangling=None)
		self.export_data(self.g_ig,'pagerank', pagerank, 'networkx')





# Execute the code
cnsp = ComplexNetworksStarterPack()

# Building the network from data
cnsp.build_network(file_name='A_list_toy_network.csv')

# Plotting the network
cnsp.plot_net(name='toy_network_plot', npixels=1000)

# Compute some metrics
cnsp.compute_metrics()