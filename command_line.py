import argparse
from parameter_retrieval import retrieve_parameters
from outputter import output

def main():
	args = parse_arguments()
	
	inputfile = args["inputfile"]
	parameters = retrieve_parameters(inputfile)
	
	output_result = output(parameters, args["outputfile"], args["format"])
	
def parse_arguments():
	parser = argparse.ArgumentParser(description="Extract a DICOM file")
	parser.add_argument("-i", "--inputfile", required=True,
						help="The input DICOM file")
	parser.add_argument("-o", "--outputfile", 
						help="The filename of the output. Default is same as input file name")
	parser.add_argument("-f", "--format",  choices=["csv", "stdout"], default="stdout",
						help="The format of the output file. For now, only CSV or print to standard output are available.")
	args = parser.parse_args()
	return vars(args)
	
	
if __name__ == "__main__":
	main()