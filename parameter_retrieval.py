"""
The function to extract parameters from the specified DICOM file.
"""

# We import the pydicom library to use it's DICOM reading methods
import pydicom as dicom
import strings 
from extractor_functions import extractor_functions
#from evaluator_functions import evaluator_functions

# We are mostly using parameters from the first item of Sequences; is this ok?  
first_sequence_item = 0

def extract_parameters(filepath):
    dataset = dicom.read_file(filepath, force=True)
    
    # created a variable file_type in circumstances where it is useful to identify whether the file is a VMAT for example
    # at the moment it does this by identifying wheter the control point index has different gantry angles for different control points of the same beam
    file_type = _extract_file_type(dataset)
    
    # define a list of parameters that need to be found
    parameters = [strings.mode_req, strings.prescription_dose_slash_fractions, strings.prescription_point, strings.isocenter_point, strings.override, strings.collimator,
                  strings.gantry, strings.SSD, strings.couch, strings.field_size, strings.wedge, strings.meas, strings.energy]
    
    
    #run the extraction functions for each parameter and store the values in parameter_values dictionary
    parameter_values = {}
    for parameter in parameters:
        parameter_values[parameter] = extractor_functions[parameter](dataset)

    return parameter_values, file_type


def evaluate_parameters(parameter_values, truth_table, case, file_type):
    case = int(case)
    # Initialise a dictionary where every key is a parameter and every associated value will either be strings.PASS,strings.FAIL or if that can't be determined the truth table value associated with that case will be added
    pass_fail_values = {}
    
    # Check if the case number is valid
    if case not in range(1, 18):
		raise Exception("Invalid case number! Must be between 1 and 18.")
        #print(case)
        
	context = {
		parameter_values: parameter_values,
		truth_table: truth_table,
		case: case,
		file_type: file_type
	}
	#iterate through each parameter you want to check
	for param in parameter_values:
		#print(param)
		# if the parameter_values[param] has not been extracted we cant determine PASS/FAIL
		# in these instances we simply return the message to indicate it has not been implemented
		if parameter_values[param] == NOT_IMPLEMENTED_STRING or parameter_values[param] is False:
			pass_fail_values[param] = NOT_IMPLEMENTED_STRING
		else:
			param_value = parameter_values[param]
			table_value = truth_table[param][case-1] # note case-1 is because the first case is 1 but the index position in the list is 0
			#call the appropriate evaluator function for each parameter
			pass_fail_values[param] = evaluator_functions[param](param_value, table_value, **context)
			 
    return pass_fail_values

def _extract_file_type(dataset):
    #Test whether the gantry angle changes within a single beam. If so, that indicates it is a VMAT file
    gantry_angle_changed = int(dataset.BeamSequence[0].ControlPointSequence[0].GantryAngle) != \
                            int(dataset.BeamSequence[0].ControlPointSequence[1].GantryAngle)
    return strings.VMAT if gantry_angle_changed else strings.not_VMAT
 

def _evaluate_gantry(param_value, table_value, **kwargs):
    # This line checks whether the parameter value found is the same as the truth table value (this is why the formating of the two dictionaries is important) and gives a "PASS" value
    # Also there are other instances where a PASS is given such as if the Truth Table is a dash for a given parameter in that case any value will satisfy
    # Or if the file is a VMAT and the parameter is either a gantry or an SSD
	file_type = kwargs["file_type"]
    if file_type == strings.VMAT:
        return strings.PASS
    else:
        return strings.PASS if (param_value == table_value or table_value == strings.ANY_VALUE) else strings.FAIL

def _evaluate_ssd(param_value, table_value, **kwargs):
	if table_value == strings.ANY_VALUE:
		return strings.PASS

    if kwargs["file_type"] == strings.VMAT:
		truth_table = kwargs["truth_table"]
		parameter_values = kwargs["parameter_values"]
		case = kwargs["case"]
		
		if truth_table[strings.gantry][case-1] == strings.ANY_VALUE or parameter_values[strings.gantry] == "error retrieving gantry":
			if truth_table[strings.gantry][case-1] != strings.ANY_VALUE:
				pass_fail_values[strings.SSD] = strings.PASS
			else:
				pass_fail_values[strings.SSD] = strings.FAIL
			
		if len(parameter_values[strings.gantry])!=len(parameter_values[strings.SSD]):
			return strings.FAIL
		
		truth_table_gantry_list = truth_table[strings.gantry][case-1].split(',')
		truth_table_ssd_list = truth_table[strings.SSD][case-1].split(',')
		if len(truth_table_gantry_list) != len(truth_table_ssd_list):
			return strings.FAIL
		
		i=0
		while i < len(truth_table_gantry_list):
			gantry_value = float(truth_table_gantry_list[i])
			ssd_value = truth_table_ssd_list[i]
			if ssd_value == '?':
				continue
				
			ssd_value=float(ssd_value)
			j = 0
			while j < len(parameter_values[strings.gantry]):
				if abs(parameter_values[strings.gantry][j] - gantry_value) < 0.3:
					if abs(parameter_values[strings.SSD][j] - ssd_value) > 1:
						return strings.FAIL
				j+=1
			i+=1
		return strings.PASS
	else:
		truth_table_ssd_list = table_value.split(',')
		if len(truth_table_ssd_list) != len(param_value):
			return strings.FAIL
		
		i=0
		while i < len(truth_table_ssd_list):
			if truth_table_ssd_list[i] != '?':
				if abs(int(truth_table_ssd_list[i])-float(parameter_values[strings.SSD][i])) > 1:
					return strings.FAIL
			i+=1
		return strings.PASS
	
def _evaluate_wedge(param_value, table_value, file_type, **kwargs):
	if table_value == 'no wedge':
		all_no_wedge = all(map(lambda w_angle: w_angle == 'no wedge', param_value.split(',')))
		return strings.PASS if all_no_wedge else strings.FAIL
	else:
		return strings.PASS if table_value == param_value else strings.FAIL

def _evaluate_prescription_dose(param_value, table_value, file_type):
	for i in range(0, 3):
		if table_value.split("/")[i] != strings.ANY_VALUE and table_value.split("/")[i] != param_value.split("/")[i]:
			return strings.FAIL
	return strings.PASS
	
def _evaluate_collimator(param_value, table_value, file_type):
	if table_value == strings.ANY_VALUE: 
		return strings.PASS
		
	result = table_value == param_value if table_value[0] != '*' else
			 table_value[1:] != param_value				
	return strings.PASS if result else strings.FAIL
	
def _evaluate_energy(param_value, table_value, file_type):
	return strings.NOT_IMPLEMENTED
	
def _evaluate_default(param_value, table_value, file_type):
	return strings.PASS if param_value == table_value or table_value == '-' else strings.FAIL
    
evaluator_functions = {
    strings.mode_req               : to_be_implemented, 
    strings.prescription_dose_slash_fractions    : _extract_prescription_dose, 
    strings.prescription_point     : to_be_implemented, 
    strings.isocenter_point        : to_be_implemented,
        # Isocenter Position TODO:Figuring out what does "SoftTiss" etc means
        # parameter_values["Isocenter Position"] = dataset.BeamSequence[i].ControlPointSequence[0].IsocenterPosition
    strings.override             : to_be_implemented, 
        #I suspect override is at (3008, 0066) tag in the DICOM file but I'm not sure
    strings.collimator              : _extract_collimator, 
    strings.gantry                   : _evaluate_gantry, 
    strings.SSD                        : _evaluate_ssd, 
    strings.couch                   : to_be_implemented, 
    strings.field_size              : to_be_implemented,
    strings.wedge                   : _evaluate_wedge, 
    strings.meas                    : to_be_implemented, 
    strings.energy                  : _extract_energy,
#   'monitor unit'            : # dataset.FractionGroupSequence[0].ReferencedBeamSequence[i].BeamMeterset
}
        
