"""
The primary entry point for the program using command line interface.
The main function asks for user inputs using command line arguments, then pass it to the extractor. 
The extractor result is then passed to the outputter.
"""
import os
import argparse
from pathlib import Path
from parameter_retrieval import extract_parameters, evaluate_parameters
from outputter import output


def main():
    # Retrieve user inputs from command line arguments
    user_input = parse_arguments()

    # Process the supplied arguments
    inputs = user_input["inputs"]
    case_number = user_input["case_number"]
    output_format = user_input["output_format"]
    # Output location is Reports folder by default (if command is run without the output argument)
    output = "./Reports" if user_input["output"] is None else user_input["output"]
    if not os.path.isdir(output):
        os.mkdir(output)

    # Look for the given file or files or directories (aka folders) and process them
    for location in inputs:
        if os.path.isfile(location):
            # Assumes the path leads to a valid DICOM. TODO add error handling?
            process_dicom(location, output, output_format, case_number)
        else:
            # Using 'with' to release directory resources after completion
            with os.scandir(location) as folder:
                for item in folder:
                    # Assumes all dcms will be the same format. TODO handle dose vs plan files, non radiotherapy dcms
                    if item.is_file() and item.name.endswith(".dcm"):
                        process_dicom(item, output, output_format, case_number)
    
def process_dicom(location, destination, output_format, case_number):
    # Prompt for case number if not specified (should be when each dicom is different case)
    while not isinstance(case_number, int):
        try:
            case_number = int(input(f"What is the case number for {location.name}? "))
        except ValueError:
            print("Case must be an integer!")

    # Extract and evaluate the dicom 
    parameters, file_type = extract_parameters(location)
    evaluations = evaluate_parameters(parameters, case_number, file_type)
    # Output the extracted parameters into the format specified by user
    output(evaluations, os.path.join(destination,Path(location.name).stem), output_format)

def parse_arguments():
    parser = argparse.ArgumentParser(description="Extract and evaluate selected parameters of DICOM files for the purpose of auditing planned radiotherapy treatment.")
    parser.add_argument("-i", "--inputs", nargs='+',
                        help="The locations of one or more DICOMS to be processed, OR the locations of one or more folders containing DICOMS to be processed.")
    parser.add_argument("-o", "--output", metavar="FOLDER",
                        help="The location where the reports for processed DICOMs should be saved (creates folder if doesn't yet exist). If unspecified, each report will be saved next to its DICOM buddy.")
    parser.add_argument("-c", "--case_number", metavar="NUMBER",
                        help="The case number of input DICOMS. If specified, assumes all DICOMS in this batch will be this case.")
    parser.add_argument("-f", choices=["csv", "json"], default="stdout", dest="output_format",
                        help="The format of the output file.")
    args = parser.parse_args()
    return vars(args)


if __name__ == "__main__":
    main()
