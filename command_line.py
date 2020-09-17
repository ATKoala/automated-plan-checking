"""
The primary entry point for the program using command line interface.
The main function asks for user inputs using command line arguments, then pass it to the extractor. 
The extractor result is then passed to the outputter.
"""
import argparse
from parameter_retrieval import extract_parameters
from outputter import output

def main():
    #Retrieve user inputs from command line arguments
    user_input = parse_arguments()
    
    #Extract parameters from the specified DICOM file
    inputfile = user_input["inputfile"]
    parameters = extract_parameters(inputfile)
    
    #output the extracted parameters into the format specified by user
    output_file = user_input["outputfile"] if user_input.get("outputfile", False) else \
                  user_input["inputfile"][0: len(user_input["inputfile"])-4] #remove the ".dcm" file extension
    output_file = output(parameters, output_file, user_input["format"])
    if output_file:
        print("Extracted to file " + output_file)
    
def parse_arguments():
    parser = argparse.ArgumentParser(description="Extract a DICOM file")
    parser.add_argument("-i", "--inputfile", required=True,
                        help="The filepath to the input DICOM file.")
    parser.add_argument("-o", "--outputfile", 
                        help="The filepath to the output file. Default is same as input file.")
    parser.add_argument("-f", "--format",  choices=["csv", "stdout"], default="stdout",
                        help="The format of the output file. For now, only CSV or print to standard output are available.")
    args = parser.parse_args()
    return vars(args)
    
    
if __name__ == "__main__":
    main()