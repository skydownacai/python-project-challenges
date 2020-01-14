import numpy as np

import networkx as nx

import matplotlib.pyplot as plt
'''
思路:

	这个火灾模拟实际上是对图进行计算和变动。
	
	火灾的演变过程，诸如火的传播实际上就是一个图进行边的删减
	
	那么由于火灾图模型使用的图是无向图，那么我们可以构造一个无向图的类，每个边集点集与权重构成的图 就是一个无向图实例
	
	那么为了可式化无向图，我们可以对无向图类添加一个可式化方法，使得每个图都能可式化出来。
	
	同时为了计算 连通个数,我们添加了一个方法, UnDirectGraph.connected_componet() 用于计算。
	
	火灾模拟系统输入一个图，并且根据概率，对图的边进行删减，决定下一个着火点，和搜索下一个可能的着火点。最后如果火没有传播
	
	计算损失。当火灾模拟很多次的时候，统计damage ratio的频数 最后做出severe curve。

'''

class UnDirectGraph:

	def __init__(self,V,A,W = None):

		'''

		:param V: 整数,所有点的个数

		:param A: array-like。边集合，每个边是一个tuple (a,b) 点 到点b的边。A:[(a,b),(),...,]

		:param W: array-like. 下标相同A的边的权重

		'''

		self.nodes = V

		self.edges = A

		self.weights = W

		self.Adjacency_Matrix = np.zeros(shape=(self.nodes,self.nodes))

		if W != None:

			self.Weight_Matrix = np.zeros(shape=(self.nodes,self.nodes))

		for i in range(len(A)):

			edge = A[i]

			self.Adjacency_Matrix[edge[0],edge[1]] = 1

			self.Adjacency_Matrix[edge[1],edge[0]] = 1

			if W != None:

				weight = self.weights[i]

				self.Weight_Matrix[edge[0],edge[1]] = weight

				self.Weight_Matrix[edge[1],edge[0]] = weight


	def connect(self,nodeA,nodeB):

		'''
		使用深度搜索 判断两个点之间是否连通
		:param nodeA:
		:param nodeB:
		:return: True if connect else False
		'''
		SearchAdjacencyMatrix = self.Adjacency_Matrix.copy()

		def deepsearch(self,nodeA,nodeB):


			for nodeC in range(self.nodes):

				if nodeC == nodeA:

					continue

				if SearchAdjacencyMatrix[nodeA,nodeC] == 0:

					continue

				if nodeC == nodeB:


					return  True

				SearchAdjacencyMatrix[nodeA,nodeC] = 0

				SearchAdjacencyMatrix[nodeC,nodeA] = 0


				if deepsearch(self,nodeC,nodeB):

					return  True

			return False

		return deepsearch(self,nodeA,nodeB)

	def connected_componet(self,nodeA):

		'''
		输入一个点, 返回这个点 连通的所有点
		:param nodeA:
		:return:
		'''
		componets = [nodeA]

		for nodeB in range(self.nodes):

			if nodeB == nodeA:

				continue

			if self.connect(nodeA,nodeB):

				componets.append(nodeB)

		return componets

	def draw(self,pos = None):

		figure = plt.figure()

		G = nx.Graph()

		for i in range(self.nodes):

			G.add_node(i + 1)

		for edge in self.edges:

			G.add_edge(edge[0] + 1, edge[1] + 1)

		if pos == None:

			pos = nx.spring_layout(G, iterations=30)

			self.pos = pos


		nx.draw(G,pos ,with_labels = True)

		plt.show()

		pass

class FireSpreadModel:

	def __init__(self,graph : UnDirectGraph):
		'''
		模拟火灾传播, 输入一个图 , 这个图 必须是 UnDirectGraph这个类的实例
		:param graph: an instance of UnDirectGraph
		'''
		self.model_graph = graph

	def simulate_an_event(self,verbose = False):

		'''
		模拟一次火灾发送

		:return: graph_after_fire : UnDirectGraph  火灾传播过后的graph

		'''

		fire_start = np.random.choice(graph.nodes)

		if verbose:

			print("fire start at :",fire_start + 1)

		import queue

		graph_Adjacency_Matrix = graph.Adjacency_Matrix.copy( ) # 保存图的领接矩阵,在这个矩阵上进行修改

		output_graph_Adjacency_Matrix = graph.Adjacency_Matrix.copy( )

		fire_nodes  = queue.Queue( ) # 记录所有已着火的点

		fire_nodes.put(fire_start) #将起始点放入队列

		fire_nodes_record = set()

		fire_nodes_record.add(fire_start)

		while  fire_nodes.qsize() >= 1:


			this_fire_node = fire_nodes.get( ) #取出一个着火点


			for next_fire in range(graph.nodes): #循环所有点, 找到所有接下来着火的店

				if next_fire == this_fire_node:

					continue

				if graph_Adjacency_Matrix[this_fire_node,next_fire] == 1:

					#表明这两个点是连通的,现在要考虑火是否要从 node : previous_fire 烧到 node:next_fire

					spread_prob = graph.Weight_Matrix[this_fire_node,next_fire]

					u = np.random.rand()


					if u <= spread_prob:

						#这条路径着火了,表明火会烧到 node:next_fire; 已经着火的点队列里面加入这个点

						fire_nodes.put(next_fire)

						fire_nodes_record.add(next_fire)

						if verbose:

							print("fire spread {} ->: {}".format(this_fire_node + 1,next_fire + 1))

						graph_Adjacency_Matrix[this_fire_node, next_fire] = 0

						graph_Adjacency_Matrix[next_fire, this_fire_node] = 0

					else:

						#这条路径幸存了,需要删除掉
						output_graph_Adjacency_Matrix[next_fire,this_fire_node] = 0

						output_graph_Adjacency_Matrix[this_fire_node,next_fire] = 0

		#生成火灾之后的图
		after_fire_edges = []

		for i in range(graph.nodes):

			for j in range(i,graph.nodes):

				if output_graph_Adjacency_Matrix[i,j]:

					after_fire_edges.append((i,j))

		after_fire_graph = UnDirectGraph(graph.nodes,after_fire_edges,None)

		MPL = len(graph.connected_componet(fire_start))

		Loss = len(after_fire_graph.connected_componet(fire_start))

		if verbose:

			print("damage ratio",Loss / MPL)

		return after_fire_graph , MPL , Loss

edges = [
	(0,2),
	(0,6),
	(1,2),
	(1,6),
	(2,3),
	(4,5),
	(6,7)
]
Weight = [
    0.3,
	0.3,
	0.3,
	0.3,
	0.5,
	0.5,
	0.5

]
graph = UnDirectGraph(8,edges,Weight)

graph.draw()

model = FireSpreadModel(graph)

N = 10000

damage_ratios = [ ]

after_fire_graph, MPL, Loss = model.simulate_an_event(verbose=True)

after_fire_graph.draw(graph.pos)

for j in range(N):

	after_fire_graph, MPL, Loss = model.simulate_an_event(verbose=False)

	damage_ratios.append(Loss / MPL)

with open("damageratios.txt",'w') as f:

	for ratio in damage_ratios:

		f.write(str(ratio) + "\n")
damage_ratios = list(sorted(damage_ratios,reverse=False))

from collections import Counter

damage_ratio_frequecy_counter = Counter(damage_ratios)

damage_ratio_uniques = list(sorted(list(set(list(damage_ratio_frequecy_counter.keys())))))


figure = plt.figure()

plt.plot(damage_ratio_uniques,[damage_ratio_frequecy_counter[damage_ratio] for damage_ratio in damage_ratio_uniques])

plt.title("severe curve")

plt.xlabel("damage ratio")

plt.ylabel("frequecy")

plt.show()




