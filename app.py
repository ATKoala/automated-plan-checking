"""
The primary entry point for the program using command line interface.
The main function asks for user inputs using command line arguments, then pass it to the extractor. 
The extractor result is then passed to the outputter.
"""
import argparse
from parameter_retrieval import extract_parameters, evaluate_parameters
from outputter import output
from pathlib import Path
from sys import exit 

def main():
    # Retrieve user inputs from command line arguments
    user_input = parse_arguments()

    # Extract parameters from the specified DICOM file
    inputfile = user_input["inputfile"]
    case_number = user_input["case_number"]
    parameters, file_type = extract_parameters(inputfile)
    evaluations = evaluate_parameters(parameters, case_number, file_type)

    # Decide the name of the output file
    if user_input["outputfile"]:
        output_name = user_input["outputfile"]
    else:
        output_name = Path(user_input["inputfile"]).stem 


    output_file = output(evaluations, output_name, user_input["format"])
    if output_file:
        print("Extracted to file " + output_file)


def parse_arguments():
    parser = argparse.ArgumentParser(description="Extract a DICOM file")
    parser.add_argument("-i", "--inputfile", required=True,
                        help="The filepath to the input DICOM file.")
    parser.add_argument("-o", "--outputfile", 
                        help="The filepath to the output file. Default is same as input file.")
    parser.add_argument("-f", "--format", choices=["csv", "stdout"], default="stdout",
                        help="The format of the output file. For now, only CSV or print to standard output are available.")
    parser.add_argument("-c", "--case_number", required=True,
                        help="case number of input number")
    args = parser.parse_args()
    return vars(args)


if __name__ == "__main__":
    main()
