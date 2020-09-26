"""
The function to extract parameters from the specified DICOM file.
"""

# We import the pydicom library to use it's DICOM reading methods
import pydicom as dicom

# TODO investigate whther it's ok to just look for the first item of the sequences
first_sequence_item = 0

def extract_parameters(filepath):
    dataset = dicom.read_file(filepath, force=True)
    # print(dataset)
    
    # truth_table_dict defines the truth table in the form a dictionary
    # Each key(i.e. case, mode req, etc) refers to a column of the truth table
    # Each key has an associated list which gives every row value corresponing to that column in order
    truth_table_dict = {
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
                 "'Lung','-','-','-','-','-','-','-','-'", "'1_3','1_4','-','-','-','-','-','-','-'",
                 "'1_1.5','4_1.5','-','-','-','-','-','-','-'", "'1','3','-','-','-','-','-','-','-'",
                 "'1','3','-','-','-','-','-','-','-'", "'1','2','3','-','-','-','-','-','-'"],
        'energy': ["6,6FFF,10,10FFF,18", "6,6FFF,10,10FFF,18", "6,6FFF,10,10FFF,18", "6,6FFF,10,10FFF,18",
                   "6,6FFF,10,10FFF,18", "6,6FFF,10,10FFF,18", "6,6FFF,10,10FFF,18", "6,6FFF,10,10FFF,18",
                   "6,6FFF,10,10FFF,18", "6,6FFF,10,10FFF,18", "6,6FFF,10,10FFF,18", "6,6FFF,10,10FFF,18",
                   "6,6FFF,10,10FFF,18", "6,6FFF,10,10FFF,18", "6,6FFF,10,10FFF,18", "6,6FFF,10,10FFF,18",
                   "6,6FFF,10,10FFF,18"]}
    
    # define a list of parameters that need to be found
    parameters = ['mode req', 'prescription dose/#', 'prescription point', 'isocentre point', 'override', 'collimator',
                  'gantry', 'SSD', 'couch', 'field size', 'wedge', 'meas', 'energy']
    
    # defines a dictionary of values found for each parameter
    # The idea is that when you retrieve a parameter its value in this parameter_values dictionary should be the same as the corresponding value in the truth_table_dictionary
    # This means when these values are changed when parameters are extracted attention needs to be paid to make sure that they are formatted in exact same way as the truth_table_dictionary 
    parameter_values = {'mode req': '', 'prescription dose/#': '', 'prescription point': '', 'isocentre point': '',
                        'override': '', 'collimator': '', 'gantry': '', 'SSD': '', 'couch': '', 'field size': '',
                        'wedge': '', 'meas': '', 'energy': ''}

    # created a variable file_type in circumstances where it is useful to identify whether the file is a VMAT for example
    # at the moment it does this by identifying wheter the control point index has different gantry angles for different control points of the same beam
    file_type = _extract_file_type(dataset)
    
    # ssd_list is defined to keep track of ssd values as an intermediate step
    # later the code uses this list to match the values against the truth table
    ssd_list = []

    # The idea of this while loop is that it iterates through every Beam in the Dicom file to find the relevant information
    i = 0
    while i < len(dataset.BeamSequence):
        # This if statement is used to ignore any setup beams
        if dataset.BeamSequence[i].BeamDescription != "SETUP beam":
            # Each parameter is divided into its own section

            # WRITE code for mode_req parameter here:

            # WRITE code for perscription_point parameter here:

            # WRITE code for isocentre_point parameter here:
            # Isocenter Position TODO:Figuring out what does "SoftTiss" etc means
            # parameter_values["Isocenter Position"] = dataset.BeamSequence[i].ControlPointSequence[0].IsocenterPosition

            # WRITE code for override parameter here:
            # I suspect override is at (3008, 0066) tag in the DICOM file but I'm not sure

            # WRITE code for collimator parameter here
            # record collimator value in the parameter_values dictionary as a string to be consistant with truth_table format 
            # According to the truth table the collimator only needs to be recorded for cases 1&5 where only 1 beam occurs
            parameter_values['collimator'] = str(
                int(dataset.BeamSequence[i].ControlPointSequence[0].BeamLimitingDeviceAngle))

            # WRITE code for couch parameter here:

            # WRITE code for field size parameter here:

            # Wedge Angles
            # It may need more work to deal with VMAT files for cases 6,7,8
            # First determine the amount of wedges
            num_wedges = int(dataset.BeamSequence[i].NumberOfWedges)
            # This first if else statement is simply so that there is a comma between wedge angles for cases where there are mulitiple wedge angles
            if parameter_values['wedge'] == '':
                #A zero is added if there is no wedge angle otherwise the wedge angle is added
                if num_wedges == 0:
                    parameter_values['wedge'] += '0'
                elif num_wedges == 1:
                    parameter_values['wedge'] += str(int(dataset.BeamSequence[0].WedgeSequence[0].WedgeAngle))
            else:
                #A zero is added if there is no wedge angle otherwise the wedge angle is added
                if num_wedges == 0:
                    parameter_values['wedge'] += ',0'
                elif num_wedges == 1:
                    parameter_values['wedge'] += ',' + str(int(dataset.BeamSequence[0].WedgeSequence[0].WedgeAngle))

            # WRITE code for meas parameter here:

            #TODO extra LVL3 files given by client are still showing all STANDARD; need to confirm that one of them really 
            #      is meant to be FFF so we can say this parameter is a bust or some other method is required.
            # Nominal Beam Energy (MV) + Fluence Mode(STANDARD/NONSTANDARD)
            parameter_values["energy"] = dataset.BeamSequence[i].ControlPointSequence[first_sequence_item].NominalBeamEnergy
            # Fluence Mode, which may indicate if dose is Flattening Filter Free (but might not! DICOM standard defines it as optional)
            #  -STANDARD     -> not FFF
            #  -NON_STANDARD -> check Fluence Mode ID for a short description of the fluence mode (could be FFF)
            if dataset.BeamSequence[i].PrimaryFluenceModeSequence[first_sequence_item].FluenceMode != 'STANDARD':
                parameter_values["energy"] += dataset.BeamSequence[i].PrimaryFluenceModeSequence[first_sequence_item].FluenceModeID

            # The monitor units is:
            # dataset.FractionGroupSequence[0].ReferencedBeamSequence[i].BeamMeterset

        i += 1

    parameter_values['gantry'] = extractor_functions['gantry'](dataset)
    # print(parameter_values)
    
    parameter_values['SSD'] = extractor_functions['SSD'](dataset)
    parameter_values['prescription dose/#'] = extractor_functions['prescription dose/#'](dataset)

    return parameter_values, file_type


def evaluate_parameters(parameter_values, case, file_type):

    truth_table_dict = {
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

    case = int(case)
    # Initialise a dictionary where every key is a parameter and every associated value will either be "PASS","FAIL" or if that can't be determined the truth table value associated with that case will be added
    pass_fail_values = {}
    
    # Check if the case number is valid
    if case in range(1, 18):
        #print(case)
        #iterate through each parameter you want to check
        for param in parameter_values:
            #print(param)
            # This line checks whether the parameter value found is the same as the truth table value (this is why the formating of the two dictionaries is important) and gives a "PASS" value
            # Also there are other instances where a PASS is given such as if the Truth Table is a dash for a given parameter in that case any value will satisfy
            # Or if the file is a VMAT and the parameter is either a gantry or an SSD
            # note case-1 is because the first case is 1 but the index position in the list is 0
            if truth_table_dict[param][case - 1] == parameter_values[param] or truth_table_dict[param][
                case - 1] == '-' or (file_type == 'VMAT' and (param == 'gantry' or param == 'SSD')):
                pass_fail_values[param] = "PASS"
            else:
                # this else statement covers situations where we can't determine a PASS Value
                # if the parameter_values[param]!='' this means that the param has been extracted since this value has been changed which means it was tested and found to FAIL
                if parameter_values[param] != '':
                    pass_fail_values[param] = "FAIL"
                # if the parameter_values[param] hasn't been changed it means the param wasn't extracted and we cant determine PASS/FAIL
                # in these instances we return what the truth table value would need to be for a PASS and return that instead
                else:
                    pass_fail_values[param] = truth_table_dict[param][case - 1]
    return pass_fail_values

def _extract_file_type(dataset):
    #Test whether the gantry angle changes within a single beam. If so, that indicates it is a VMAT file
    gantry_angle_changed = int(dataset.BeamSequence[0].ControlPointSequence[0].GantryAngle) != \
                            int(dataset.BeamSequence[0].ControlPointSequence[1].GantryAngle)
    return 'VMAT' if gantry_angle_changed else 'IMRT'
 
def _extract_prescription_dose(dataset):
    # Total Prescription Dose
    total_prescription_dose = str(int(dataset.DoseReferenceSequence[0].TargetPrescriptionDose))
    # number of fractions
    number_of_fractions = str(dataset.FractionGroupSequence[0].NumberOfFractionsPlanned)
    
    #this section deals with the 'prescription dos/#' parameter
    # You need to make sure that the format of parameter_values['perscription dose/#] is exactly the same as truth_table_dict['perscription dose/#'] in cases where the file passes
    # To begin you assign the total_perscription dose to the parameter value
    prescription_dose = total_prescription_dose
    
    # Then when perscription dose is 24,48,50, or 900 you also need to check the amount of fractions
    # and when its 900 the primary dosimeter unit needs to be 'MU' as well
    if total_prescription_dose == '24':
        prescription_dose = '24/' + number_of_fractions
    elif total_prescription_dose == '48':
        prescription_dose = '48/' + number_of_fractions
    elif total_prescription_dose == '50':
        prescription_dose = '50/' + number_of_fractions
    elif total_prescription_dose == '900' and dataset.BeamSequence[0].PrimaryDosimeterUnit == 'MU':
        prescription_dose = '900/' + number_of_fractions + ' MU'
    
    return prescription_dose
    
def _extract_gantry(dataset):
    try:
        file_type = _extract_file_type(dataset)
        
        #If the dataset is a VMAT file,the Gantry is then assumed to be irrelevant
        if file_type == 'VMAT':
            return 'VMAT File'
        # If not, then return the Gantry Angle of all beams, separated by commas
        else:
            #ignore setup beams
            beams = list(filter(lambda beam: beam.BeamDescription != "SETUP beam", dataset.BeamSequence))
            #obtain the gantry angles of all beams
            gantry_instances = map(lambda beam: str(int(beam.ControlPointSequence[0].GantryAngle)), beams)
            
            return ','.join(gantry_instances)
    except:
        return '-'
        
def _extract_ssd(dataset):
#find SSD in centimeters    
    ssd_list = []
    try:
        #ignore setup beams
        beams = list(filter(lambda beam: beam.BeamDescription != "SETUP beam", dataset.BeamSequence))
        #obtain the ssd of all beams
        #in the DICOM file the SSD is given in millimetres so its divided by 10 so its in centimetres
        ssd_list = list(map(lambda beam: int(beam.ControlPointSequence[0].SourceToSurfaceDistance / 10), beams))
    except:
        return '-'
    
    if len(ssd_list) == 0:
        return '-'
        
    # The ssd_list contains SSD values for each beam
    # This code converts those values into a format that is the same as the truth table
    # A key assumption is that the SSD value needs to be within one centimetre of the truth_table value for it to pass
    # checks instances where there is only one ssd value
    if len(ssd_list) == 1:
        # 100, 86, 93, or 90 are the only single value SSDs in the truth table
        if abs(ssd_list[0] - 100) <= 1:
            return '100'
        elif abs(ssd_list[0] - 86) <= 1:
            return '86'
        elif abs(ssd_list[0] - 93) <= 1:
            return '93'
        elif abs(ssd_list[0] - 90) <= 1:
            return '90'
        # if the SSD isn't any of the above values we just assign it value it was closest to
        # Then it will only pass the truth table when the corresponing thruth table value is a '-'
        else:
            return str(ssd_list[0])
    
    elif len(ssd_list) == 3:
        # '86,93,86' is the only truth table value of length 3 that needs to be checked
        if abs(ssd_list[0] - 86) <= 1 and abs(ssd_list[1] - 93) <= 1 and abs(ssd_list[2] - 86) <= 1:
            return '86,93,86'
        else:
            return "non valid ssd"
    
    elif len(ssd_list) == 5:
        # '?,86,93,86,?' is the only truth table value of length 5 that needs to be checked
        if abs(ssd_list[1] - 89) <= 1 and abs(ssd_list[2] - 93) <= 1 and abs(ssd_list[3] - 89) <= 1:
            return '?,89,93,89,?'
        else:
            return "non valid ssd"


#just a placeholder function to indicate which parameters have not been implemented
def to_be_implemented(dataset):
    return ''

extractor_functions = {
    'mode req': to_be_implemented, 
    'prescription dose/#': _extract_prescription_dose, 
    'prescription point': to_be_implemented, 
    'isocentre point': to_be_implemented,
        # Isocenter Position TODO:Figuring out what does "SoftTiss" etc means
        # parameter_values["Isocenter Position"] = dataset.BeamSequence[i].ControlPointSequence[0].IsocenterPosition
    'override': to_be_implemented, 
        #I suspect override is at (3008, 0066) tag in the DICOM file but I'm not sure
    'collimator': '', 
    'gantry': _extract_gantry, 
    'SSD': _extract_ssd, 
    'couch': '', 
    'field size': '',
    'wedge': '', 
    'meas': '', 
    'energy': ''
}
