import json

from BerryField import *

from Bear import  *

from Tourist import *

filepath = input("Enter the json file name for the simulation => ")

#filepath = "bears_and_berries_1.json"
print(filepath)

with open(filepath) as f:

	data = json.loads(f.read())


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

print(berryfield)

print("Active Bears:")

for bear in ActiveBears:

	print(bear)

print("\nActive Tourists:")

for tourist in ActiveTourists:

	print(tourist)
