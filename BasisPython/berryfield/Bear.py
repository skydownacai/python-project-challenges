class Bear:

	def __init__(self,row , column , direction):

		self.row = row

		self.column = column

		self.direction = direction

		self.alseep = 0

		self.berrysEat = 0

	def __str__(self):


		if self.alseep == 3 or self.alseep == 0:

			return "Bear at ({},{}) moving {}".format(self.row,self.column,self.direction)

		else:

			return "Bear at ({},{}) moving {} - Asleep for {} more turns".format(self.row,self.column,self.direction,self.alseep)

	def move_one_space(self):

		if  "N" in self.direction:

			self.row -= 1

		if "S" in self.direction:

			self.row += 1

		if "E" in self.direction:

			self.column += 1

		if "W" in self.direction:

			self.column -= 1

	def OutOfBoundary(self,gridrow,gridcolumn):

		if self.row >= gridrow or self.row < 0 :

			return True

		if self.column >= gridcolumn or self.column < 0:

			return True

		return  False