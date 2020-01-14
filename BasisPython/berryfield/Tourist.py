class Tourist:

	def __init__(self,row,column):

		self.row = row

		self.column = column

		self.Turns_with_out_seeing_a_bear = 0 #记录看见熊的回合数

		self.bears_one_time_see = 0 # 记录一个回合看见的熊的个数

	def __str__(self):

		return "Tourist at ({},{}), {} turns without seeing a bear.".format(self.row,self.column,self.Turns_with_out_seeing_a_bear)

