import json

from BerryField import *

from Bear import  *

from Tourist import *

filepath = input("Enter the json file name for the simulation => ")

#filepath = "bears_and_berries_2.json"
print(filepath)

with open(filepath) as f:

	data = json.loads(f.read())

print("Starting Configuration")
#首先生成熊

ActiveBears = []

ReserveBears = []

ActiveTourists = []

ReserveTourists = [ ]

for item in data["active_bears"]:

	ActiveBears.append(Bear(**dict(list(zip(["row" ,"column", "direction"],item)))))


for item in data["reserve_bears"]:

	ReserveBears.append(Bear(**dict(list(zip(["row" ,"column", "direction"],item)))))

for item in data["active_tourists"]:

	ActiveTourists.append(Tourist(**dict(list(zip(["row" ,"column"],item)))))

for item in data["reserve_tourists"]:

	ReserveTourists.append(Tourist(**dict(list(zip(["row" ,"column"],item)))))


berryfield = BerryField(data["berry_field"],ActiveBears,ActiveTourists)

def PrintOutSimulation():

	print(berryfield)

	print("Active Bears:")

	for bear in berryfield.ActiveBears:

		print(bear)

	print("\nActive Tourists:")

	for tourist in berryfield.ActiveTourists:

		print(tourist)

PrintOutSimulation()

t = 0
while True :
	t  += 1
	print("\nTurn: {}".format(t))

	LeftField_message = []

	#grow berry
	berryfield.grow_and_spread_berry()


	#Moving the bears

	need_remove_bear = [ ]

	for bear in berryfield.ActiveBears:

		if bear.alseep == 0:

			'''eat berrys and move'''

			bear_berrysEat = 0

			while True:

				eat_capacity = 30 - bear_berrysEat #the maximium number of berry that this bear can eat

				berryeat = min(eat_capacity,berryfield.BerryValues[bear.row][bear.column]) # acual number of berry this bear eat

				bear_berrysEat	+= berryeat

				berryfield.BerryValues[bear.row][bear.column] -= berryeat



				if bear_berrysEat < 30 :

					bear.move_one_space()

				else:

					break

				#if bear move out of the boundary

				if bear.OutOfBoundary(len(berryfield.BerryValues),len(berryfield.BerryValues[0])):

					need_remove_bear.append(bear)

					break

				#if bear ran into a tourist

				ran_into_a_tourist = False

				for tourist in berryfield.ActiveTourists:


						if (bear.row, bear.column) == (tourist.row, tourist.column):

							ran_into_a_tourist = True

							bear.alseep = 3

							break

				if ran_into_a_tourist:

					break

	for bear in need_remove_bear:

		print(str(bear) + " - Left the Field")

		berryfield.ActiveBears.remove(bear)


	#check tourists

	need_remove_tourists = [ ]

	for tourist in berryfield.ActiveTourists:

		tourist.bears_one_time_see = 0


		meet_bear = False

		for bear in berryfield.ActiveBears:

			# Whether tourist meet a bear:

			if (bear.row,bear.column) == (tourist.row,tourist.column):


				print(str(tourist) + " - Left the Field")

				need_remove_tourists.append(tourist)

				meet_bear = True

				break

			# Whether tourist see a bear:

			import math

			distance = math.sqrt((bear.row - tourist.row)**2 + (bear.column - tourist.column)**2)

			if distance <= 4:

				tourist.bears_one_time_see += 1

		if not meet_bear:

			if tourist.bears_one_time_see == 0:

				tourist.Turns_with_out_seeing_a_bear += 1

			else:

				tourist.Turns_with_out_seeing_a_bear = 0

				if tourist.bears_one_time_see >= 3:

					#tourist get scared and left the field

					print(str(tourist) + " - Left the Field")

					need_remove_tourists.append(tourist)

			#tourists get board and left the field
			if tourist.Turns_with_out_seeing_a_bear >= 3:

				print(str(tourist) + " - Left the Field")

				need_remove_tourists.append(tourist)


	#remove tourist
	for tourist in need_remove_tourists:

		berryfield.ActiveTourists.remove(tourist)

	for bear in berryfield.ActiveBears:

		if bear.alseep > 0:

			bear.alseep -= 1
	#add reserve bears

	if berryfield.total_berry >= 500 and len(ReserveBears) >= 1:

		next_bear = ReserveBears.pop(0)

		berryfield.ActiveBears.append(next_bear)

		print(str(next_bear) + " - Entered the Field")

	#add reserve tourist
	if len( berryfield.ActiveBears) >= 1 and len(ReserveTourists) >= 1:

		next_tourist = ReserveTourists.pop( 0)

		berryfield.ActiveTourists.append(next_tourist)

		print(str(next_tourist) + " - Entered the Field")


	print()
	#Every five turns passed print out the simulation

	if t % 5 == 0:

		PrintOutSimulation()


	if len(berryfield.ActiveBears) == 0 and (len(ReserveBears) == 0 or  berryfield.total_berry == 0):

		break


PrintOutSimulation()


