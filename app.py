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

silent = None
skip_dose_structure = None

def main():
    ''' Handles input arguments and processes the dicoms'''

    global silent, skip_dose_structure

    # Retrieve user inputs and settings from command line arguments
    user_input = parse_arguments()
    properties = read_properties_file("settings.txt")
    
    # Process the supplied arguments
    settings_input = [location.strip() for location in properties["default_input"].split('*')]
    inputs = user_input["inputs"] if user_input["inputs"] else settings_input
    output = user_input["output"] if user_input["output"] else properties["default_output_folder"]
    silent = True if properties["silent_run"].lower() == "true" else False
    skip_dose_structure = True if properties["skip_dose_structure"].lower() == "true" else False
    case_number = user_input["case_number"]
    truth_table_file = user_input["truth_table_file"] if user_input["truth_table_file"] else properties["truth_table_file"]
    truth_table = read_truth_table(truth_table_file) 

    # Print truth table being applied: this can be confusing for the user due to the settings file defaulting to lvl3
    info_print(f"\nUsing truth table: {truth_table_file}\n")
    
    # Create the output folder if it doesn't exist
    if not os.path.isdir(output):
        try:
            os.mkdir(output)
        except FileNotFoundError:
            exit(f"Tried creating the output directory <{output}>, but the location <{Path(output).resolve().parent}> doesn't exist!")

    # Look for the given file or files or directories (aka folders) and process them
    for location in inputs:
        process_location(location, output, case_number, truth_table)
    print()

def process_location(location, output, case_number, truth_table):
    # Check if input item has case number attached
    input_item = location.split(",")
    if len(input_item) == 2:
        location = Path(input_item[0])
        case_number = int(input_item[1])
    else:
        location = Path(location)

    # Handle the location where a file is specified
    if os.path.isfile(location):
        folder_path = Path(os.path.dirname(location))
        dose_struct_index = dose_struct_references(folder_path)
        process_dicom(location, output, case_number, truth_table, dose_struct_index)

    # Handle the location where a folder is specified
    else:
        # First we scan through the entire folder once to find out what dose and structure files we have
        dose_struct_index = dose_struct_references(location)
        # Then, scan through the folder and process each RTPLAN DICOM
        with os.scandir(location) as folder:
            for item in folder:
                if item.is_file() and item.name.endswith(".dcm"):
                    result = process_dicom(item.path, output, case_number, truth_table, dose_struct_index)
                    info_print(result)
        
def dose_struct_references(folder_path):
    ''' Function to scan a directory and build an index of RTDOSE and RTSTRUCT files by StudyInstanceUID
        Returns a dictionary: {StudyInstanceUID: {RTDOSE: [paths,...]), RTSTRUCT: [paths,...]}, ...}
    '''
    if skip_dose_structure:
        return None
    dose_struct_index = {}
    with os.scandir(folder_path) as folder:
        for entry in folder:
            # uid, modality and file_path are all None if the entry is not a dose or structure file
            uid, modality, file_path = dose_struct_reference(entry.path)
            # create a new dictionary entry if we haven't seen this uid before
            if uid not in dose_struct_index:
                dose_struct_index[uid] = {strings.RTDOSE:[], strings.RTSTRUCT:[], None:[]}
            dose_struct_index[uid][modality].append(file_path)
    return dose_struct_index

def dose_struct_reference(dir_entry):
    if dir_entry.is_file() and dir_entry.name.endwith(".dcm"):
        dataset = pydicom.dcmread(dir_entry.path, force=True, specific_tags=["StudyInstanceUID", "Modality"])
        if str(dataset.Modality) in [strings.RTDOSE, strings.RTSTRUCT]:
            return dataset.StudyInstanceUID, dataset.Modality, dir_entry.path
    return None,None,None

def process_dicom(location, destination, case_number, truth_table, dose_struct_index):
    ''' Function to process a single DICOM RTPLAN

    location            - the filepath of the DICOM
    destination         - the filepath of the folder in which the result will be saved to
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
    output_file = output(parameters, evaluations, solutions, output_location)
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
