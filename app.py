"""
The primary entry point for the program using command line interface.
The main function asks for user inputs using command line arguments, then pass it to the extractor. 
The extractor result is then passed to the outputter.
"""
import os
import argparse
from pathlib import Path
from parameter_retrieval.parameter_retrieval import extract_parameters, evaluate_parameters
from outputter import output
from pathlib import Path
from truth_table_reader import read_truth_table

def main():
    # Retrieve user inputs from command line arguments
    user_input = parse_arguments()
    
    #Retrieve default settings from properties file
    properties = read_properties_file("properties.txt")
    
    # Process the supplied arguments
    inputs = user_input["inputs"] if user_input["inputs"] else [properties["default_input_folder"]]
    case_number = user_input["case_number"]
    output_format = user_input["output_format"]
    truth_table_file = user_input["truth_table_file"] if user_input["truth_table_file"] else properties["truth_table_file"]
    truth_table = read_truth_table(truth_table_file) if truth_table_file else default_truth_table
    
    # Output location is Reports folder by default (if command is run without the output argument)
    output = user_input["output"] if user_input["output"] else properties["default_output_folder"]
    if not os.path.isdir(output):
        os.mkdir(output)

    # Look for the given file or files or directories (aka folders) and process them
    # TODO error handling for unexpected inputs for each case 
    #       - leave it until after we decide on which input methods to keep 
    for location in inputs:
        # Check if input is [file,case] [file,case] ... format
        comma_case = None
        input_item = location.split(",")
        if len(input_item) == 2:
            location = input_item[0]
            comma_case = int(input_item[1])
        final_case = case_number if comma_case is None else comma_case

        # Handle the case where file is specified
        if os.path.isfile(location):
            process_dicom(location, output, output_format, final_case, truth_table)

        # The case where folder is specified
        else:
            # Using 'with' keyword to release directory resources after processed
            with os.scandir(location) as folder:
                for item in folder:
                    if item.is_file() and item.name.endswith(".dcm"):
                        process_dicom(item.path, output, output_format, final_case, truth_table)

def process_dicom(location, destination, output_format, case_number, truth_table):
    # Prompt for case number if not specified (should be when each dicom is different case)
    while not isinstance(case_number, int):
        try:
            case_number = int(input(f"What is the case number for {location}? "))
        except ValueError:
            print("Case must be an integer!")

    # Extract and evaluate the dicom 
    parameters = extract_parameters(location, case_number)
    evaluations = evaluate_parameters(parameters, truth_table, case_number)

    # solutions == the truth table values for the given case
    solutions = dict([(key, truth_table[key][case_number-1]) for key in truth_table])
    # Output the extracted parameters into the format specified by user
    
    output_file = output(parameters, evaluations, solutions, os.path.join(destination,Path(location).stem), output_format)
    if output_file:
        print("Extracted to file " + output_file)

def parse_arguments():
    parser = argparse.ArgumentParser(description="Extract and evaluate selected parameters of DICOM files for the purpose of auditing planned radiotherapy treatment.")
    parser.add_argument("-i", "--inputs", nargs='+',
                        help="The locations of one or more DICOMS to be processed, OR the locations of one or more folders containing DICOMS to be processed.")
    parser.add_argument("-t", "--truth_table", dest="truth_table_file",
                        help="The file containing the truth table to be used for determining pass/fail results.")    
    parser.add_argument("-o", "--output", metavar="FOLDER",
                        help="The location where the reports for processed DICOMs should be saved (creates folder if doesn't yet exist). If unspecified, each report will be saved in a Reports folder in this directory.")
    parser.add_argument("-c", "--case_number", metavar="NUMBER", type=int,
                        help="The case number of input DICOMS. If specified, assumes all DICOMS in this batch will be this case.")
    parser.add_argument("-f", "--format", choices=["csv", "json"], default="csv", dest="output_format",
                        help="The format of the output file.")
                    
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

# truth_table defines the truth table in the form a dictionary
# Each key(i.e. case, mode req, etc) refers to a column of the truth table
# Each key has an associated list which gives every row value corresponing to that column in order
default_truth_table = {
    "case": ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17'],
    "mode req": ['False', 'False', 'False', 'False', 'False', 'True', 'True', 'True', 'False', 'True', 'True',
                'True', 'True', 'True', 'True', 'True', 'True'],
    "prescription dose/#": ['2/-/-', '2/-/-', '2/-/-', '2/-/-', '50/25/-', '50/25/-', '50/25/-', '50/25/-', '900/3/MU', '45/3/-', '24/2/-',
                            '48/4/-', '3/-/-', '3/-/-', '20/-/-', '20/-/-', '20/-/-'],
    "prescription point": ['1 or 3', '5', '3', '3', 'chair', 'CShape', 'CShape', 'C8Target', '-', 'SoftTissTarget',
                        'SpineTarget', 'LungTarget', '1', '1', 'PTV_c14_c15', '-', '-'],
    "isocentre point": ['surf', '3', '3', '3', '3', '3', '3', '3', 'SoftTiss', 'SoftTiss', 'Spine', 'Lung', '1',
                        '1', '1', '-', '-'],
    "override": ['bone', 'no override', 'no override', 'no override', 'no override', 'lungs', 'no override',
                'no override', 'lungs', 'lungs', 'no override', 'no override', 'central cube', 'central cube',
                'central cube', 'central cube', 'central cube'],
    "collimator": ['0', '-', '-', '-', '0', '*0', '*0', '*0', '-', '-', '-', '-', '-', '-', '-', '-', '-'],
    "gantry": ['0', '270,0,90', '90', '90', '0', '150,60,0,300,210', '150,60,0,300,210', '150,60,0,300,210', '-',
            '-', '-', '-', '-', '-', '-', '-', '-'],
    "SSD": ['100', '86,93,86', '86', '86', '93', '?,89,93,89,?', '?,89,93,89,?', '?,89,93,89,?', '90', '-', '-',
            '-', '-', '-', '-', '-', '-'],
    'couch': ['-', '-', '-', '-', '-', 'couch?', 'couch?', 'couch?', '-', 'couch?', 'couch?', 'couch?', '-', '-',
            'couch?', 'couch?', 'couch?'],
    'field size': ['10x10', '10x6,10x12,10x6', '10x12', '10x12', '-', '-', '-', '-', '3x3,2x2,1x1', '-', '-', '-',
                '3x3', '1.5x1.5', '-', '-', '-'],
    'wedge': ['no wedge', '30,no wedge,30', 'no wedge', '60', 'no wedge', 'no wedge', 'no wedge', 'no wedge', 'no wedge', 'no wedge', 'no wedge', 'no wedge', 'no wedge', 'no wedge', 'no wedge', 'no wedge', 'no wedge'],
    'meas': ["'1','3','10','-','-','-','-','-','-'",
            "'5_RLAT','8_RLAT','5_AP','8_AP','5_LLAT','8_LLAT','-','-','-'", "'3','5','-','-','-','-','-','-','-'",
            "'3','5','-','-','-','-','-','-','-'", "'11','12','13','14','15','18','19','20','21'",
            "'11','12','13','14','15','16','17','-','-'", "'11','12','13','14','15','16','17','-','-'",
            "'11','12','13','14','15','17','18','-','-'",
            "'SoftTiss_3','SoftTiss_2','SoftTiss_1','-','-','-','-','-','-'",
            "'SoftTiss','-','-','-','-','-','-','-','-'", "'Spine2Inf','Spine1Sup','Cord','-','-','-','-','-','-'",
            "'Lung','-','-','-','-','-','-','-','-'", "'1_3','4_3','-','-','-','-','-','-','-'",
            "'1_1.5','4_1.5','-','-','-','-','-','-','-'", "'1','3','-','-','-','-','-','-','-'",
            "'1','3','-','-','-','-','-','-','-'", "'1','2','3','-','-','-','-','-','-'"],
    'energy': ["6,6FFF,10,10FFF,18", "6,6FFF,10,10FFF,18", "6,6FFF,10,10FFF,18", "6,6FFF,10,10FFF,18",
            "6,6FFF,10,10FFF,18", "6,6FFF,10,10FFF,18", "6,6FFF,10,10FFF,18", "6,6FFF,10,10FFF,18",
            "6,6FFF,10,10FFF,18", "6,6FFF,10,10FFF,18", "6,6FFF,10,10FFF,18", "6,6FFF,10,10FFF,18",
            "6,6FFF,10,10FFF,18", "6,6FFF,10,10FFF,18", "6,6FFF,10,10FFF,18", "6,6FFF,10,10FFF,18",
            "6,6FFF,10,10FFF,18"]
}
if __name__ == "__main__":
    main()
