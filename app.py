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

    # In the future, we might read the truth table in from here 
    # truth_table defines the truth table in the form a dictionary
    # Each key(i.e. case, mode req, etc) refers to a column of the truth table
    # Each key has an associated list which gives every row value corresponing to that column in order
    truth_table = {
        "case": ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17'],
        "mode req": ['False', 'False', 'False', 'False', 'False', 'True', 'True', 'True', 'False', 'True', 'True',
                    'True', 'True', 'True', 'True', 'True', 'True'],
        "prescription dose/#": ['2', '2', '2', '2', '50/25', '50/25', '50/25', '50/25', '900/3 MU', '45/3', '24/2',
                                '48/4', '3', '3', '20', '20', '20'],
        "prescription point": ['1 or 3', '5', '3', '3', 'chair', 'CShape', 'CShape', 'C8Target', '-', 'SoftTissTarget',
                            'SpineTarget', 'LungTarget', '1', '1', 'PTV_c14_c15', '-', '-'],
        "isocentre point": ['surf', '3', '3', '3', '3', '3', '3', '3', 'SoftTiss', 'SoftTiss', 'Spine', 'Lung', '1',
                            '1', '1', '-', '-'],
        "override": ['bone', 'no override', 'no override', 'no override', 'no override', 'lungs', 'no override',
                    'no override', 'lungs', 'lungs', 'no override', 'no override', 'central cube', 'central cube',
                    'central cube', 'central cube', 'central cube'],
        "collimator": ['0', '-', '-', '-', '0', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-'],
        "gantry": ['0', '270,0,90', '90', '90', '0', '150,60,0,300,210', '150,60,0,300,210', '150,60,0,300,210', '-',
                '-', '-', '-', '-', '-', '-', '-', '-'],
        "SSD": ['100', '86,93,86', '86', '86', '93', '?,89,93,89,?', '?,89,93,89,?', '?,89,93,89,?', '90', '-', '-',
                '-', '-', '-', '-', '-', '-'],
        'couch': ['-', '-', '-', '-', '-', 'couch?', 'couch?', 'couch?', '-', 'couch?', 'couch?', 'couch?', '-', '-',
                'couch?', 'couch?', 'couch?'],
        'field size': ['10x10', '10x6,10x12,10x6', '10x12', '10x12', '-', '-', '-', '-', '3x3,2x2,1x1', '-', '-', '-',
                    '3x3', '1.5x1.5', '-', '-', '-'],
        'wedge': ['0', '30,0,30', '0', '60', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-'],
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
                "6,6FFF,10,10FFF,18"]}

    # Extract parameters and evaluate them
    inputfile = user_input["inputfile"]
    case_number = user_input["case_number"]
    parameters, file_type = extract_parameters(inputfile)
    evaluations = evaluate_parameters(parameters, truth_table, case_number, file_type)

    # Decide the name of the output file
    if user_input["outputfile"] is not None:
        output_name = user_input["outputfile"]
    else:
        output_name = Path(user_input["inputfile"]).stem 

    output_file = output(parameters, evaluations, truth_table, output_name, user_input["format"])
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
