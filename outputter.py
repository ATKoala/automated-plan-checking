def output_csv(parameters, name):
	print("Not yet Implemented")
	
def output_stdout(parameters, name):
	print("The number of beams: " + str(parameters["Number of Beams"]))
	for beam in parameters["Beams"]:
		for p in beam:
			print(p + " : " + str(beam[p]))
		print("\n")
			
formatter = {
	'csv': output_csv,
	'stdout': output_stdout
}

def output(parameters, name, format):
	formatter_function = formatter[format]
	formatter_function(parameters, name)
	