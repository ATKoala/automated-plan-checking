'''This file applies the extraction and evaluation functions defined in extractor_functions.py and evaluator functions.py'''

# We import the pydicom library to use it's DICOM reading methods
import pydicom as dicom
from code import strings
from .extractor_functions import extractor_functions, _extract_mode
from .evaluator_functions import evaluator_functions

def extract_parameters(dataset, case):
    # define a list of parameters that need to be found
    parameters = [strings.mode, strings.prescription_dose, strings.prescription_point, strings.isocenter_point, strings.override, strings.collimator,
                  strings.gantry, strings.SSD, strings.couch, strings.field_size, strings.wedge, strings.meas, strings.energy]
    
    #run the extraction functions for each parameter and store the values in parameter_values dictionary
    parameter_values = {}
    for parameter in parameters:
        parameter_values[parameter] = extractor_functions[parameter](dataset, case)

    return parameter_values

def evaluate_parameters(parameter_values, truth_table, case):
    case = int(case)
    # Initialise a dictionary where every key is a parameter and every associated value will either be strings.PASS,strings.FAIL or if that can't be determined the truth table value associated with that case will be added
    pass_fail_values = {}
    
    # Check if the case number is valid
    cases = len(truth_table["case"])
    if case not in range(1, 18):
        raise Exception(f"Invalid case number! Must be between 1 and {cases}")

    # Grouped information that will be passed onto evaluation functions
    context = {
        "parameter_values": parameter_values,
        "truth_table": truth_table,
        "case": case,
        "file_type": parameter_values[strings.mode]
    }

    # Iterate through each parameter you want to check
    for param in parameter_values:
        # If the parameter_values[param] has not been extracted we cant determine PASS/FAIL
        # In these instances we simply return the message to indicate it has not been implemented
        if parameter_values[param] == strings.NOT_IMPLEMENTED or parameter_values[param] is False:
            pass_fail_values[param] = strings.NOT_IMPLEMENTED
        else:
            param_value = parameter_values[param]
            table_value = truth_table[param][case-1]
            # Call the appropriate evaluator function for each parameter
            pass_fail_values[param] = evaluator_functions[param](param_value, table_value, **context)
    return pass_fail_values
 
        
