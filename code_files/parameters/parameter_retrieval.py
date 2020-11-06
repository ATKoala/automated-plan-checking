'''This file applies the extraction and evaluation functions defined in extractor_functions.py and evaluator functions.py'''

# We import the pydicom library to use it's DICOM reading methods
import pydicom as dicom
from code_files import strings
from .extractor_functions import extractor_functions, _extract_mode
from .evaluator_functions import evaluator_functions

def extract_parameters(dataset, dose_struct_paths, case):
    ''' 
    dataset             - A pydicom Dataset object
    dose_struct_paths   - A dictionary {RTDOSE: [paths,...]), RTSTRUCT: [paths,...]}
                            with RTDOSE and RTSTRUCT files sharing a StudyInstanceUID with the plan dicom being processed
                          May be None if no associated dose/structs found
    case                - The case of the RTPLAN being processed
    '''
    # define a list of parameters that need to be found
    parameters = [strings.mode, strings.prescription_dose, strings.prescription_point, strings.isocenter_point, strings.override, strings.collimator,
                  strings.gantry, strings.SSD, strings.couch, strings.field_size, strings.wedge, strings.meas, strings.energy]
    
    # Perhaps there should only be one dose and struct associated with a plan?
    if dose_struct_paths and len(dose_struct_paths[strings.RTDOSE])!=1 or len(dose_struct_paths[strings.RTSTRUCT])!=1:
        exit("In parameter/parameter_retrieval.py, in function extract_parameters()\n \
              Unexpected number of dose/struct files found associated with one RTPLAN")
              
    dose = dicom.dcmread(dose_struct_paths[strings.RTDOSE][0], force=True)
    struct = dicom.dcmread(dose_struct_paths[strings.RTSTRUCT][0], force=True)

    #run the extraction functions for each parameter and store the values in parameter_values dictionary
    parameter_values = {}
    for parameter in parameters:
        parameter_values[parameter] = extractor_functions[parameter](dataset, dose, struct, case)

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
 
        
