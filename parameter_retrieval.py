"""
The function to extract parameters from the specified DICOM file.
"""

# We import the pydicom library to use it's DICOM reading methods
import pydicom as dicom
import strings 

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
			context =
			pass_fail_values[param] = evaluator_functions[param](param_value, table_value, **context)
			 
			 
			 
			 
		else:
			if truth_table[param][case - 1] == parameter_values[param] or truth_table[param][
				case - 1] == strings.ANY_VALUE:
				pass_fail_values[param] = strings.PASS
			# if the param has been extracted, it was tested and found to FAIL
			else:            
				pass_fail_values[param] = strings.FAIL

    return pass_fail_values

def _extract_file_type(dataset):
    #Test whether the gantry angle changes within a single beam. If so, that indicates it is a VMAT file
    gantry_angle_changed = int(dataset.BeamSequence[0].ControlPointSequence[0].GantryAngle) != \
                            int(dataset.BeamSequence[0].ControlPointSequence[1].GantryAngle)
    return strings.VMAT if gantry_angle_changed else strings.not_VMAT
 
def _extract_prescription_dose(dataset):
    # Total Prescription Dose
    total_prescription_dose = str(int(dataset.DoseReferenceSequence[0].TargetPrescriptionDose))
    # number of fractions
    number_of_fractions = str(dataset.FractionGroupSequence[0].NumberOfFractionsPlanned)
    
    #this section deals with the 'prescription dos/#' parameter
    # You need to make sure that the format of parameter_values['perscription dose/#] is exactly the same as truth_table['perscription dose/#'] in cases where the file passes
    # To begin you assign the total_perscription dose to the parameter value
    prescription_dose = total_prescription_dose
    
    # Then when perscription dose is 24,48,50, or 900 you also need to check the amount of fractions
    # and when its 900 the primary dosimeter unit needs to be 'MU' as well
    try:
        prim_dosimeter_unit = dataset.BeamSequence[0].PrimaryDosimeterUnit
    except:
        prim_dosimeter_unit = "No primary dosimeter unit"
    
    return prescription_dose + "/" + number_of_fractions + "/" + prim_dosimeter_unit
    
def _extract_collimator(dataset):
    #ignore setup beams
    beams = list(filter(lambda beam: beam.BeamDescription != strings.SETUP_beam, dataset.BeamSequence))
    # record collimator value in the parameter_values dictionary as a string to be consistant with truth_table format 
    # According to the truth table the collimator only needs to be recorded for cases 1&5 where only 1 beam occurs    
    collimator_value = beams[len(beams)-1].ControlPointSequence[0].BeamLimitingDeviceAngle
    return str(int(collimator_value))
    
def _extract_gantry(dataset):
    try:
        file_type = _extract_file_type(dataset)
        
        #If the dataset is a VMAT file it goes through each of the control point sequence and finds each associated gantry angle and returns the lowest value slash the highest value
        # Also I dont think there is meant to be more than one beam in these cases
        if file_type == strings.VMAT:
            i = 0
            vmat_gantry_angles = []
            while i < len(dataset.BeamSequence):
                if dataset.BeamSequence[i].BeamDescription != strings.SETUP_beam:
                    for control_point in dataset.BeamSequence[i].ControlPointSequence:
                        vmat_gantry_angles.append(float(control_point.GantryAngle))
                    return vmat_gantry_angles
                i+=1
            return "error retrieving gantry"
        # If not, then return the Gantry Angle of all beams, separated by commas
        else:
            #ignore setup beams
            beams = list(filter(lambda beam: beam.BeamDescription != strings.SETUP_beam, dataset.BeamSequence))
            #obtain the gantry angles of all beams
            gantry_instances = map(lambda beam: str(int(beam.ControlPointSequence[0].GantryAngle)), beams)
            
            return ','.join(gantry_instances)
    except:
        return strings.ANY_VALUE
        
def _extract_ssd(dataset):
#find SSD in centimeters    
    file_type = _extract_file_type(dataset)
    
    ssd_list = []
    try:
        if file_type == strings.VMAT:
            i = 0
            vmat_ssd_list = []
            while i < len(dataset.BeamSequence):
                if dataset.BeamSequence[i].BeamDescription != strings.SETUP_beam:
                    for control_point in dataset.BeamSequence[i].ControlPointSequence:
                        vmat_ssd_list.append(float(control_point.ReferencedDoseReferenceSequence[1].BeamDosePointSSD)/10)
                    return vmat_ssd_list
                i+=1
            return "error retrieving SSD"
        else:
            #ignore setup beams
            beams = list(filter(lambda beam: beam.BeamDescription != strings.SETUP_beam, dataset.BeamSequence))
            #obtain the ssd of all beams
            #in the DICOM file the SSD is given in millimetres so its divided by 10 so its in centimetres
            ssd_list = list(map(lambda beam: beam.ControlPointSequence[0].SourceToSurfaceDistance / 10, beams))
            return ssd_list
    except:
        return "error retrieving SSD"

def _extract_wedge(dataset):
    # It may need more work to deal with VMAT files for cases 6,7,8
    
    #ignore setup beams
    beams = list(filter(lambda beam: beam.BeamDescription != strings.SETUP_beam, dataset.BeamSequence))
    # if there are wedges, get the wedge angle of the beam. Otherwise, get 0
    wedge_angles = list(map(lambda beam: str(int(beam.WedgeSequence[0].WedgeAngle)) if int(beam.NumberOfWedges) > 0 else 'no wedge', beams))
    
    return ','.join(wedge_angles)
    
def _extract_energy(dataset):
    #energies = []
    energy = ''
    
    for beam in dataset.BeamSequence:
        #ignore setup beams
        if beam.BeamDescription == strings.SETUP_beam:
            continue
        
        #TODO extra LVL3 files given by client are still showing all STANDARD; need to confirm that one of them really 
        #      is meant to be FFF so we can say this parameter is a bust or some other method is required.
        # Nominal Beam Energy (MV) + Fluence Mode(STANDARD/NONSTANDARD)
        energy = beam.ControlPointSequence[first_sequence_item].NominalBeamEnergy
        # Fluence Mode, which may indicate if dose is Flattening Filter Free (but might not! DICOM standard defines it as optional)
        #  -STANDARD     -> not FFF
        #  -NON_STANDARD -> check Fluence Mode ID for a short description of the fluence mode (could be FFF)
        if beam.PrimaryFluenceModeSequence[first_sequence_item].FluenceMode != strings.STANDARD_FLUENCE:
            energy += str(beam.PrimaryFluenceModeSequence[first_sequence_item].FluenceModeID)
        
        #energies.append(energy)
    
    return energy
    

#just a placeholder function to indicate which parameter extractions have not been implemented
def to_be_implemented(dataset):
    return strings.NOT_IMPLEMENTED

extractor_functions = {
    strings.mode_req                : to_be_implemented, 
    strings.prescription_dose_slash_fractions     : _extract_prescription_dose, 
    strings.prescription_point     : to_be_implemented, 
    strings.isocenter_point        : to_be_implemented,
        # Isocenter Position TODO:Figuring out what does "SoftTiss" etc means
        # parameter_values["Isocenter Position"] = dataset.BeamSequence[i].ControlPointSequence[0].IsocenterPosition
    strings.override                : to_be_implemented, 
        #I suspect override is at (3008, 0066) tag in the DICOM file but I'm not sure
    strings.collimator             : _extract_collimator, 
    strings.gantry                  : _extract_gantry, 
    strings.SSD                    : _extract_ssd, 
    strings.couch                   : to_be_implemented, 
    strings.field_size              : to_be_implemented,
    strings.wedge                   : _extract_wedge, 
    strings.meas                    : to_be_implemented, 
    strings.energy                  : _extract_energy,
#   'monitor unit'            : # dataset.FractionGroupSequence[0].ReferencedBeamSequence[i].BeamMeterset
}

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
	return "PASS" if param_value == table_value or table_value == '-' else "FAIL"
    
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
        
