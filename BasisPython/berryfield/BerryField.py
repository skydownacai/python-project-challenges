

class BerryField:

	def __init__(self,BerryValues,ActiveBears,ActiveTourists):
		'''

		:param GridValues: 生成BerryField

		'''

		self.BerryValues =  BerryValues

		self.row ,self.column = len(self.BerryValues),len(self.BerryValues[0])

		self.ActiveBears = ActiveBears

		self.ActiveTourists = ActiveTourists

		for tourist in self.ActiveTourists:

			for bear in self.ActiveBears:

				if (bear.row,bear.column) == (tourist.row,tourist.column):

					bear.alseep = 3

	def grow_and_spread_berry(self):

		'''first grow berry . Then spread berry'''
		for i in range(self.row):

			for j in range(self.column):

				if self.BerryValues[i][j] > 0 and self.BerryValues[i][j] <= 9 :

					self.BerryValues[i][j] += 1


		for i in range(self.row):

			for j in range(self.column):

				if self.BerryValues[i][j] == 0:

					#spread berry

					spread = False

					# find the 8 adjacent spaces except itself

					for k in [-1,0,1]:

						for l in [-1,0,1]:

							if k == 0 and l == 0:

								continue

							if k + i >= 0 and k + i < self.row and l + j >= 0 and l + j < self.column:


								if  self.BerryValues[k + i][l + j] == 10:

									spread = True

									break

					if spread:

						self.BerryValues[i][j] = 1

	@property
	def OutPutGrid(self):

		import copy

		outputgrid = copy.deepcopy(self.BerryValues)

		for bear in self.ActiveBears:

			outputgrid[bear.row][bear.column] = "B"

		for tourist in self.ActiveTourists:

			if outputgrid[tourist.row][tourist.column] == "B":

				outputgrid[tourist.row][tourist.column] = "X"

			else:

				outputgrid[tourist.row][tourist.column] = "T"

		return outputgrid

	@property
	def total_berry(self):

		total_beerys = 0

		for i in range(self.row):

			for j in range(self.column):

				total_beerys += int(self.BerryValues[i][j])

		return total_beerys

	def __str__(self):

		import copy

		OutPutGrid = copy.deepcopy(self.BerryValues)

		for tourist in self.ActiveTourists:

			OutPutGrid[tourist.row][tourist.column] = "T"

		for bear in self.ActiveBears:

			if OutPutGrid[bear.row][bear.column] == "T": #already exist a tourist

				OutPutGrid[bear.row][bear.column] = "X"

			else:

				OutPutGrid[bear.row][bear.column] = "B"


		total_beerys = 0

		for i in range(self.row):

			for j in range(self.column):

				total_beerys += int(self.BerryValues[i][j])

		output = "Field has %s berries."%total_beerys + "\n"

		for i in range(self.row):

			for j in range(self.column):

				output+="{:>4}".format(OutPutGrid[i][j])

			output+= "\n"

		return output





