import sys
import math
import random
class GMM:

	def __init__(self,k):

		self.prior_cluster_prob = [1/k for i in range(k)]


		self.cluster_num = k

	@staticmethod
	def add(vectorA,vectorB):

		result = []

		for i in range(len(vectorA)):

			result.append(vectorA[i] + vectorB[i])

		return result

	@staticmethod
	def tran(MatrixA):

		row = len(MatrixA)

		column = len(MatrixA[0])

		result = []

		for i in range(column):

			result.append([MatrixA[j][i] for j in range(row)])

		return result

	@staticmethod
	def sub(vectorA,vectorB):

		result = []

		for i in range(len(vectorA)):

			result.append(vectorA[i] - vectorB[i])

		return result
	@staticmethod
	def Matrix_add(MatrixA,MatrixB):

		result = []

		for i in range(len(MatrixA)):

			vectorA = MatrixA[i]

			vectorB = MatrixB[i]

			result.append(GMM.add(vectorA,vectorB))


		return result

	@staticmethod
	def identity(dim):

		result = []

		for i in range(dim):

			result.append([0 for j in range(dim)])

		for i in range(dim):

			result[i][i] = 1


		return result

	@staticmethod
	def zeros(shape :tuple):

		result = []

		for i in range(shape[0]):

			result.append([0 for j in range(shape[1])])

		return result


	@staticmethod
	def TwoDimension_MatrixInv(matrix):

		det = GMM.TwoDimensionDet(matrix)

		inv = [

			[matrix[1][1]/det,matrix[1][0]/det],
			[matrix[0][1]/det,matrix[0][0]/det]
		]

		return inv

	@staticmethod
	def MatrixMultiplication(A,B):

		result = [ ]
		#print("A",len(A),len(A[0]))

		#print("B",len(B),len(B[0]))


		for i in range(len(A)):

			row = [ ]

			for j in range(len(B[0])):


				this_sum = 0

				for p in range(len(A[0])):

					this_sum += A[i][p] * B[p][j]


				row.append(this_sum)

			result.append(row)

		return result

	@staticmethod
	def inner_product(x,y):


		result = 0

		for i in range(len(x)):

			result += x[i]*y[i]

		return result


	@staticmethod
	def TwoDimensionDet(A):


		return A[0][0]*A[1][1] - A[0][1]*A[1][0]


	@staticmethod
	def N(x, mean_value,covariance_matrix):
		'''
		正态分布的概率密度函数
		:param self: 
		:return: 
		'''


		dimx = len(x)

		operator1 =  math.sqrt((2 * math.pi) ** dimx * GMM.TwoDimensionDet(covariance_matrix))

		operator2 = [GMM.sub(x, mean_value)]

		operator3 =  GMM.MatrixMultiplication(operator2, GMM.TwoDimension_MatrixInv(covariance_matrix))

		operator4 = GMM.MatrixMultiplication(operator3,GMM.tran([GMM.sub(x, mean_value)]))

		operator5 = math.exp( -1/2 * operator4[0][0])

		return operator5/operator1

	def likelyhood(self,x):

		result = 0

		cluser_prob = [GMM.N(x, self.means[l], self.covariance_matrix[l]) for l in range(self.cluster_num)]

		return GMM.inner_product(self.prior_cluster_prob,cluser_prob)

	def log_likelyhood(self,X):



		return math.log(sum([ self.likelyhood(X[i]) for i in range(len(X))]))

	def predict(self,X):
		'''
		预测cluster
		:return:
		'''
		ypred = [ ]

		for j in range(len(X)):

			cluser_prob = [GMM.N(X[j], self.means[i], self.covariance_matrix[i]) for i in range(self.cluster_num)]

			cluser_probs = [ ]

			for i in range(len(cluser_prob)):

				cluser_probs.append(

					self.prior_cluster_prob[i] * cluser_prob[i]
				)

			max_prob = max(cluser_probs)

			cluster = cluser_probs.index(max_prob)


			ypred.append( cluster)

		return ypred

	def fit(self,X  , verbose = True ,tol = 1e-6):


		N = len(X)

		DimX = len(X[0])

		self.covariance_matrix  =  [ GMM.identity(DimX) for i in range(self.cluster_num)] # 初始化每个cluster的 协方差矩阵


		iteration = 0

		log_likelyhood_history = []

		while True:


			#E-step

			responsibility = GMM.zeros(shape=(N,self.cluster_num))

			for i in range(N):

				point_likelyhood = self.likelyhood(X[i])

				for l in range(self.cluster_num):

					responsibility[i][l] =  self.prior_cluster_prob[l] * GMM.N(X[i],self.means[l],self.covariance_matrix[l]) / point_likelyhood


			#M-step

			new_means = [ ]

			new_covarances = []

			for l in range(self.cluster_num):

				cluster_responsibility = []

				for P in range(len(responsibility)):

					cluster_responsibility.append(responsibility[P][l])

				self.prior_cluster_prob[l] = sum(cluster_responsibility) / N

				this_mean  = [0 for P in range(DimX)]

				vectors  = [ ]

				for i in range(len(X)):

					this_vector = []

					for P in range(DimX):

						this_vector.append(responsibility[i][l] * X[i][P])

					vectors.append(this_vector)

				for vector in vectors:

					this_mean =  GMM.add(this_mean,vector)

				this_new_mean = []

				for i in range(len(this_mean)):

					this_new_mean.append(this_mean[i] / sum(cluster_responsibility))


				new_means.append(this_new_mean)


				this_covarance = GMM.zeros(shape = (len(self.covariance_matrix[0]),len(self.covariance_matrix[0][0])))


				matrixs = []

				for i in range(len(X)):

					operator1 = [GMM.sub(X[i],self.means[l])]

					operator2 = GMM.tran(operator1)

					new_matrix = GMM.MatrixMultiplication(operator2,operator1)


					for P in range(len(new_matrix)):

						for Q in range(len(new_matrix[0])):

							new_matrix[P][Q] = new_matrix[P][Q] * responsibility[i][l]

					matrixs.append(new_matrix)



				for matrix in matrixs:


					this_covarance = GMM.Matrix_add(matrix,this_covarance)



				for P in range(len(this_covarance)):

					for Q in range(len(this_covarance[0])):

						this_covarance[P][Q] = this_covarance[P][Q] /sum(cluster_responsibility)

				new_covarances.append(this_covarance)

			self.means = new_means


			self.covariance_matrix = new_covarances


			this_log_likelyhood = self.log_likelyhood(X)

			if verbose:

				print("iteration: ",iteration," log_likelyhood",this_log_likelyhood)

			iteration += 1

			log_likelyhood_history.append(this_log_likelyhood)

			if iteration >= 2 and log_likelyhood_history[-1] - log_likelyhood_history[-2] <= tol:

				break


inputdata = []

for line in sys.stdin:

	if line == '\n':

		break

	inputdata.append(line)

N, k  = list(map(int,inputdata[0].replace("\n","").split(" ")))


for i in range(len(inputdata)):

	inputdata[i] = 	list(map(float,inputdata[i].replace("\n","").split(" ")))

X = inputdata[1: N + 1]

model = GMM(k)

model.means = inputdata[-1 * k : ]


model.fit(X,tol=0,verbose=False)

pred = model.predict(X)

print(pred)