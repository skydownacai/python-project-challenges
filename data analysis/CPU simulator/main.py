import threading
import pandas as pd
from scipy import stats
import numpy as np
import sqlite3
from pandas.io import sql

class processor:

	def __init__(self,code):

		self.code = code

		self.task_end_time = 0

		self.task_start_time = 0

		self.avaliable = True

	def assign_task(self,task,start_time):

		self.task_on_hand = task

		self.task_end_time = start_time + task["Duration"]

		print("** {} : Task {} assigned to processor {}.".format(start_time,task["ID"],self.code))

		self.avaliable = False

	def complete_task(self):

		print("** {} : Task {} completed.".format(self.task_end_time,self.task_on_hand["ID"]))

		self.avaliable = True

class Simulated_System:

	def __init__(self,n_processor):

		self.processors = [
			processor(i + 1) for i in range(n_processor)
		]

		self.processor_state = [
			0 for i in range(n_processor)
		]
		self.clock = 0

		print("** SYSTEM INITIALISED **")

	@staticmethod
	def check_id_validity(id):

		rule1 = False

		rule2 = False

		rule3 = False

		isspecial = lambda x: np.any([True if specialchar in x else False for specialchar in "@_#*-&" ])

		rule4 = isspecial(id)

		for char in id:
			rule1 = char.islower() or rule1
			rule2 = char.isupper() or rule2
			rule3 = char.isdigit() or rule3
			if rule1 + rule2 + rule3 + rule4 >= 3 :
				return True

		return False

	def run(self,task_list):

		task_list = task_list.sort_values(by = "Arrival")

		task_pointer = 0

		task_assign_lists = [ ]


		while True:

			complete_time = [ ]

			avaliable_processor = [ ]

			for j in range(len(self.processors)):

				processor = self.processors[j]

				if not processor.avaliable :

					complete_time.append([processor.task_end_time,j])

				else:
					avaliable_processor.append([processor,j])


			if len(task_assign_lists) > 0 :

				if len(avaliable_processor) >= 1:

					asign_processor,processor_index = avaliable_processor.pop(0)

					assign_task = task_assign_lists.pop(0)

					asign_processor.assign_task(assign_task, self.clock)

					complete_time.append([asign_processor.task_end_time,processor_index])


			complete_time = np.array(complete_time)


			if task_pointer <= len(task_list) - 1:

				next_task = task_list.iloc[task_pointer]

				task_arrival = next_task["Arrival"]

			else:

				task_arrival = 10000000000000000


			if len(complete_time) > 0:

				min_complete_time = np.min(complete_time[:,0])

				min_index = np.argmin(complete_time[:,0])

				need_complete_processor = self.processors[int(complete_time[min_index][1])]

				if min_complete_time < task_arrival:

					self.clock = need_complete_processor.task_end_time

					need_complete_processor.complete_task()

					continue

			if task_arrival == 10000000000000000:

				break

			self.clock = next_task["Arrival"]

			print("** {} : Task {} with duration {} enters the system".format(self.clock, next_task['ID'],
																			  next_task['Duration']))
			if Simulated_System.check_id_validity(next_task["ID"]):

				print("** Task {} accepted.".format(next_task['ID']))

				task_assign_lists.append(next_task)

				if len(avaliable_processor) == 0:

					print("** Task {} on hold.".format(next_task["ID"]))
			else:

				print("** Task {} unfeasible and discarded".format(next_task["ID"]))


			task_pointer += 1


class Random_task_list:
	@staticmethod
	def random_id():
		valid_char = "qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM0123456789@_#*-&"
		return "".join([valid_char[np.random.randint(0,len(valid_char) - 1)] for i in range(6)])

	@staticmethod
	def random_arrival():
		return np.random.rand() * 100

	@staticmethod
	def Sample_to_DataBase(task_num):
		'''
		use the method of  Metropolis-Hasting to sample from exponential distribution
		the tasklist data will be inserted into sqlite3 database
		:param task_num:
		'''

		x0 = 0.5
		g = lambda x: np.exp(- 1  * x) if x >= 0 else 0
		def Q(x, xi):
			return 1 / np.sqrt(2 * np.pi) * np.exp(-1 * (x - xi) * (x - xi) / 2)
		samples = [x0]
		for i in range(task_num):
			u = np.random.rand(1)[0]
			x_last = samples[-1]
			x = stats.norm.rvs(loc=x_last, scale=1, size=1)[0]
			accept = min(1, (Q(x_last, x) * g(x)) / (g(x_last) * Q(x, x_last)))
			if u <= accept:
				samples.append(x)
			else:
				samples.append(x_last)

		import math
		Duration = list(map(math.ceil,samples[1:]))

		Arrival  = [Random_task_list.random_arrival() for i in range(task_num)]

		ID = [Random_task_list.random_id() for i in range(task_num)]

		df = pd.DataFrame(
			{
				"ID":ID,
				"Arrival":Arrival,
				"Duration":Duration
			}
		)

		#insert the data into database
		conn = sqlite3.connect('tasklist.db')
		df.to_sql("tasklist",conn,if_exists="replace")

	@staticmethod
	def Read_From_DataBase():

		conn = sqlite3.connect('tasklist.db')

		task_df = pd.read_sql("select * from tasklist",conn).drop("index",axis=1)

		return task_df

Random_task_list.Sample_to_DataBase(100)

task_list = Random_task_list.Read_From_DataBase()

sytem = Simulated_System(3)

sytem.run(task_list = task_list)#
