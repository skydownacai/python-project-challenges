# student number:

# IMPLEMENT YOUR FUNCTION HERE

def random_converter(x):

	converter = [
		int,float,bool,str,complex
	]
	import random
	converter_applied = converter[random.randint(0,len(converter) - 1)]
	print("转换器",converter_applied)

	if type(x) == str and converter_applied != str:


		digital = True

		for char in x:

			if char != "." and str.isdigit(char) == False:

				digital = False

				break
		#除小数点外都是数字

		if digital:

			if "." in x  and converter_applied  in [int,bool]:
				#说明是小输
				print("cannot be converted")

				return  None
		else:

				print("cannot be converted")

				return  None


	return converter_applied(x)

print(random_converter("12.1"))