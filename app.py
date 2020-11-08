''' automated-plan-checker

Extracts and evaluates data points from DICOM RTPLAN files.
This file covers the high level process of handling input and processing dicoms 
'''

import pydicom 
import os
import argparse
from pathlib import Path
from code_files import strings
from code_files.outputter import output
from code_files.truth_table_reader import read_truth_table
from code_files.parameters.parameter_retrieval import extract_parameters, evaluate_parameters

def main():
    '''
    Main function; everything starts here.
    Handles input arguments and processes the dicoms
    '''
    # Retrieve user inputs and settings from command line arguments
    user_input = parse_arguments()
    properties = read_properties_file("settings.txt")
    
    # Process the supplied arguments
    settings_input = [location.strip() for location in properties["default_input"].split('*')]
    inputs = user_input["inputs"] if user_input["inputs"] else settings_input
    output = user_input["output"] if user_input["output"] else properties["default_output_folder"]
    silent = True if properties["silent_run"].lower() == "true" else False
    skip_dose_structure = True if properties["skip_dose_structure"].lower() == "true" else False
    output_format = user_input["output_format"]
    case_number = user_input["case_number"]
    truth_table_file = user_input["truth_table_file"] if user_input["truth_table_file"] else properties["truth_table_file"]
    truth_table = read_truth_table(truth_table_file) 

    # Print truth table being applied: this can be confusing for the user due to the settings file defaulting to lvl3
    info_print(f"\nUsing truth table: {truth_table_file}\n", silent)
    
    # Create the output folder if it doesn't exist
    if not os.path.isdir(output):
        try:
            os.mkdir(output)
        except FileNotFoundError:
            output = Path(output)
            print(f"Tried creating the output directory <{output.name}>, but the location <{output.resolve().parent}> doesn't exist")
            exit()

    # Look for the given file or files or directories (aka folders) and process them
    for location in inputs:
        # Check if input item is [file,case] formatted
        comma_case = None
        input_item = location.split(",")
        if len(input_item) == 2:
            location = Path(input_item[0])
            comma_case = int(input_item[1])
        else:
            location = Path(location)
        final_case = case_number if comma_case is None else comma_case

        # Handle the input where a file is specified
        if os.path.isfile(location):
            folder_path = Path(os.path.dirname(location))
            dose_struct_index = dose_struct_references(folder_path, skip_dose_structure)
            process_dicom(location, output, output_format, final_case, truth_table, dose_struct_index)

        # Handle the input where a folder is specified
        else:
            # First we scan through the entire folder once to find out what dose and structure files we have
            dose_struct_index = dose_struct_references(location, skip_dose_structure)
            # Then, scan through the folder and process each RTPLAN DICOM
            with os.scandir(location) as folder:
                for item in folder:
                    if item.is_file() and item.name.endswith(".dcm"):
                        result = process_dicom(item.path, output, output_format, final_case, truth_table, dose_struct_index)
                        info_print(result, silent)
        
def dose_struct_references(folder_path, skip):
    ''' Function to scan a directory and build an index of RTDOSE and RTSTRUCT files by StudyInstanceUID
        Returns a dictionary: {StudyInstanceUID: {RTDOSE: [paths,...]), RTSTRUCT: [paths,...]}, ...}
    '''
    if skip:
        return None
    dose_struct_index = {}
    with os.scandir(folder_path) as folder:
        for item in folder:
            if item.is_file() and item.name.endswith(".dcm"):
                uid, modality, file_path = dose_struct_reference(item.path)
                if uid not in dose_struct_index:
                    dose_struct_index[uid] = {strings.RTDOSE:[], strings.RTSTRUCT:[], None:[]}
                dose_struct_index[uid][modality].append(file_path)
    return dose_struct_index

def dose_struct_reference(file_path):
    dataset = pydicom.dcmread(file_path, force=True, specific_tags=["StudyInstanceUID", "Modality"])
    if str(dataset.Modality) in [strings.RTDOSE, strings.RTSTRUCT]:
        return dataset.StudyInstanceUID, dataset.Modality, file_path
    else:
        return None,None,None

def process_dicom(location, destination, output_format, case_number, truth_table, dose_struct_index):
    ''' Function to process a single DICOM RTPLAN

    location            - the filepath of the DICOM
    destination         - the filepath of the folder in which the result will be saved to
    output_format       - perhaps there will be support for json output in the future? currently always csv
    case_number         - the case number of the truth table that parameters should be evaluated against (see data/truth_table_lvl3.csv)
    truth_table         - a dictionary of correct values for each case
    dose_struct_index   - a dictionary {StudyInstanceUID: {RTDOSE: [paths,...]), RTSTRUCT: [paths,...]}, ...}
    '''
    dataset = pydicom.read_file(location, force=True)

    # If the dicom is not an RTPLAN, we don't want to process it. 
    if str(dataset.Modality) != "RTPLAN":
        return "{:10} {}: not a plan file".format("SKIPPED", location)

    # Prompt for case number if not specified
    cases = len(truth_table["case"])
    while not isinstance(case_number, int):
        try:
            case_number = int(input(f"What is the case number for {location}? "))
        except ValueError:
            print(f"Case must be an integer between 1 and {cases}!")

    # Look for any related dose files or structure sets
    dose_struct_paths = None
    if dose_struct_index and dataset.StudyInstanceUID in dose_struct_index:
        dose_struct_paths = dose_struct_index[dataset.StudyInstanceUID]

    # Extract and evaluate the DICOM 
    parameters = extract_parameters(dataset, dose_struct_paths, case_number)
    evaluations = evaluate_parameters(parameters, truth_table, case_number)
    solutions = dict([(key, truth_table[key][case_number-1]) for key in truth_table])

    # Output the extracted parameters into the format specified by user
    output_location = os.path.join(destination,Path(location).stem)
    output_file = output(parameters, evaluations, solutions, output_location, output_format)
    return "{:10} {} -> {}".format("EXTRACTED", location, output_file)

def info_print(text,silent=False):
    if not silent:
        print(text)
        
def parse_arguments():
    parser = argparse.ArgumentParser(description="Extract and evaluate information from DICOM files for the purpose of auditing planned radiotherapy treatment.")
    parser.add_argument("-i", "--inputs", nargs='+',
                        help="The locations of one or more DICOMS to be processed, OR the locations of one or more folders containing DICOMS to be processed.")
    parser.add_argument("-t", "--truth_table", dest="truth_table_file",
                        help="The path of the file containing the truth table to be used for determining pass/fail results.")    
    parser.add_argument("-o", "--output", metavar="FOLDER",
                        help="The location where the reports for processed DICOMs should be saved (creates folder if doesn't yet exist). If unspecified, each report will be saved in a Reports folder in this directory.")
    parser.add_argument("-c", "--case_number", metavar="NUMBER", type=int,
                        help="The case number of input DICOMS. If specified, assumes all DICOMS in this batch will be this case.")
    parser.add_argument("-f", "--format", metavar="csv", default="csv", dest="output_format",
                        help="The format of the output file. Csv by default if not set. Also, currently only csv available.")
    args = parser.parse_args()
    return vars(args)
    
def read_properties_file(properties_file):
    properties = {}
    with open(properties_file, 'r') as prop_file:
        for line in prop_file:
            line = line.strip()
            
            #skip  if line is a comment or wrong syntax
            if line.startswith("#"): continue
            if '=' not in line: continue
            
            [key, value] = line.split('=', 1)
            properties[key.strip()] = value.strip()
            
    return properties

if __name__ == "__main__":
    main()
