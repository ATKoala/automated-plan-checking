"""
The function to extract parameters from the specified DICOM file.
"""

# We import the pydicom library to use it's DICOM reading methods
import pydicom as dicom

# We are mostly using parameters from the first item of Sequences; is this ok?  
first_sequence_item = 0
NOT_IMPLEMENTED_STRING = "NOT IMPLEMENTED"


def extract_parameters(filepath):
    dataset = dicom.read_file(filepath, force=True)

    # created a variable file_type in circumstances where it is useful to identify whether the file is a VMAT for example
    # at the moment it does this by identifying wheter the control point index has different gantry angles for different control points of the same beam
    file_type = _extract_mode(dataset)

    # define a list of parameters that need to be found
    parameters = ['mode req', 'prescription dose/#', 'prescription point', 'isocentre point', 'override', 'collimator',
                  'gantry', 'SSD', 'couch', 'field size', 'wedge', 'meas', 'energy']

    # run the extraction functions for each parameter and store the values in parameter_values dictionary
    parameter_values = {}
    for parameter in parameters:
        parameter_values[parameter] = extractor_functions[parameter](dataset)

    return parameter_values, file_type


def evaluate_parameters(parameter_values, truth_table, case, file_type):
    case = int(case)
    # Initialise a dictionary where every key is a parameter and every associated value will either be "PASS","FAIL" or if that can't be determined the truth table value associated with that case will be added
    pass_fail_values = {}

    # Check if the case number is valid
    if case in range(1, 18):
        # print(case)
        # iterate through each parameter you want to check
        for param in parameter_values:
            if param is 'mode req' and case in [6, 7, 8]:
                # "If you can determine IMRT or VMAT in cases 6-8 then that would be the most helpful"
                #   - Andrew , in Jiale's forwarded email 6/10/20
                pass_fail_values[param] = parameter_values[param]
            # print(param)
            # if the parameter_values[param] has not been extracted we cant determine PASS/FAIL
            # in these instances we simply return the message to indicate it has not been implemented
            if parameter_values[param] == NOT_IMPLEMENTED_STRING or parameter_values[param] is False:
                pass_fail_values[param] = NOT_IMPLEMENTED_STRING

            # This line checks whether the parameter value found is the same as the truth table value (this is why the formating of the two dictionaries is important) and gives a "PASS" value
            # Also there are other instances where a PASS is given such as if the Truth Table is a dash for a given parameter in that case any value will satisfy
            # Or if the file is a VMAT and the parameter is either a gantry or an SSD
            # note case-1 is because the first case is 1 but the index position in the list is 0
            if param == 'gantry':
                if file_type == 'VMAT':
                    pass_fail_values['gantry'] = "VMAT unknown"
                else:
                    if truth_table['gantry'][case - 1] == parameter_values['gantry'] or truth_table['gantry'][
                        case - 1] == '-':
                        pass_fail_values['gantry'] = "PASS"
                    else:
                        pass_fail_values['gantry'] = "FAIL"
            elif param == 'SSD':
                if file_type == 'VMAT':
                    pass_fail_values['SSD'] = "VMAT unknown"
                else:
                    if truth_table['SSD'][case - 1] == '-':
                        pass_fail_values['SSD'] = "PASS"
                    else:
                        truth_table_ssd_list = truth_table['SSD'][case - 1].split(',')
                        if len(truth_table_ssd_list) == len(parameter_values['SSD']):
                            pass_fail_values['SSD'] = "PASS"
                            i = 0
                            while i < len(truth_table_ssd_list):
                                if truth_table_ssd_list[i] != '?':
                                    if abs(int(truth_table_ssd_list[i]) - float(parameter_values['SSD'][i])) > 1:
                                        pass_fail_values['SSD'] = 'FAIL'
                                i += 1
                        else:
                            pass_fail_values['SSD'] = 'FAIL'
            elif truth_table[param][case - 1] == parameter_values[param] or truth_table[param][
                case - 1] == '-':
                pass_fail_values[param] = "PASS"

            # if the param has been extracted, it was tested and found to FAIL
            else:
                pass_fail_values[param] = "FAIL"

    return pass_fail_values


def _extract_mode(dataset):
    # Test whether the gantry angle changes within a single beam. If so, that indicates it is a VMAT file
    gantry_angle_changed = int(dataset.BeamSequence[0].ControlPointSequence[0].GantryAngle) != \
                           int(dataset.BeamSequence[0].ControlPointSequence[1].GantryAngle)
    return 'VMAT' if gantry_angle_changed else 'IMRT'


def _extract_prescription_dose(dataset):
    # Total Prescription Dose
    total_prescription_dose = str(int(dataset.DoseReferenceSequence[0].TargetPrescriptionDose))
    # number of fractions
    number_of_fractions = str(dataset.FractionGroupSequence[0].NumberOfFractionsPlanned)

    # this section deals with the 'prescription dos/#' parameter You need to make sure that the format of
    # parameter_values['perscription dose/#] is exactly the same as truth_table['perscription dose/#'] in cases where
    # the file passes To begin you assign the total_perscription dose to the parameter value
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


def _extract_field_size(dataset):
    # ignore setup beams
    beams = list(filter(lambda beam: beam.BeamDescription != "SETUP beam", dataset.BeamSequence))
    # record collimator value in the parameter_values dictionary as a string to be consistant with truth_table format
    # According to the truth table the collimator only needs to be recorded for cases 1&5 where only 1 beam occurs
    beam_type_number = len(beams[len(beams) - 1].ControlPointSequence[0].BeamLimitingDevicePositionSequence)
    print("\n" + str(beam_type_number) + " types of device in total:")

    length_x = -1
    length_y = -1

    for i in range(beam_type_number):
        device_type = beams[len(beams) - 1].ControlPointSequence[0].BeamLimitingDevicePositionSequence[
            i].RTBeamLimitingDeviceType
        jaw_position = beams[len(beams) - 1].ControlPointSequence[0].BeamLimitingDevicePositionSequence[
            i].LeafJawPositions
        # print(dataset)python app.py --inputs Resources/Input/YellowLvlIII_4a.dcm --format csv --case_number 6

        if device_type != "MLCX" and device_type != "MLCY":

            if device_type == "X":
                length_x = int((-jaw_position[0] + jaw_position[1]) / 10)
            elif device_type == "Y":
                length_y = int((-jaw_position[0] + jaw_position[1]) / 10)
            elif device_type == "ASYMX":
                if length_x != -1:
                    print("Two Beam Limiting Device on X axis!")
                    length_x = int((-jaw_position[0] + jaw_position[1]) / 10)
            elif device_type == "ASYMY":
                if length_y != -1:
                    print("Two Beam Limiting Device on Y axis!")
                length_y = int((-jaw_position[0] + jaw_position[1]) / 10)
        else:
            print("Sorry, cannot extract field size with MLCX/MLCY")
    if length_x == -1:
        print("No Beam Limiting Device on X axis!")
    elif length_y == -1:
        print("No Beam Limiting Device on Y axis!")
    else:
        #print(str(length_y) + "x" + str(length_x))
        return str(length_y) + "x" + str(length_x)

    # return str("("+length_x+","+length_y+")")


def _extract_collimator(dataset):
    # ignore setup beams
    beams = list(filter(lambda beam: beam.BeamDescription != "SETUP beam", dataset.BeamSequence))
    # record collimator value in the parameter_values dictionary as a string to be consistant with truth_table format 
    # According to the truth table the collimator only needs to be recorded for cases 1&5 where only 1 beam occurs    
    collimator_value = beams[len(beams) - 1].ControlPointSequence[0].BeamLimitingDeviceAngle
    return str(int(collimator_value))


def _extract_gantry(dataset):
    try:
        file_type = _extract_mode(dataset)

        # If the dataset is a VMAT file,the Gantry is then assumed to be irrelevant
        if file_type == 'VMAT':
            return 'VMAT File'
        # If not, then return the Gantry Angle of all beams, separated by commas
        else:
            # ignore setup beams
            beams = list(filter(lambda beam: beam.BeamDescription != "SETUP beam", dataset.BeamSequence))
            # obtain the gantry angles of all beams
            gantry_instances = map(lambda beam: str(int(beam.ControlPointSequence[0].GantryAngle)), beams)

            return ','.join(gantry_instances)
    except:
        return '-'


def _extract_ssd(dataset):
    # find SSD in centimeters
    ssd_list = []
    try:
        # ignore setup beams
        beams = list(filter(lambda beam: beam.BeamDescription != "SETUP beam", dataset.BeamSequence))
        # obtain the ssd of all beams
        # in the DICOM file the SSD is given in millimetres so its divided by 10 so its in centimetres
        ssd_list = list(map(lambda beam: beam.ControlPointSequence[0].SourceToSurfaceDistance / 10, beams))
    except:
        return '-'

    return ssd_list


def _extract_wedge(dataset):
    # It may need more work to deal with VMAT files for cases 6,7,8

    # ignore setup beams
    beams = list(filter(lambda beam: beam.BeamDescription != "SETUP beam", dataset.BeamSequence))
    # if there are wedges, get the wedge angle of the beam. Otherwise, get 0
    wedge_angles = list(
        map(lambda beam: str(int(beam.WedgeSequence[0].WedgeAngle)) if int(beam.NumberOfWedges) > 0 else 'no wedge',
            beams))
    return ','.join(wedge_angles)


def _extract_energy(dataset):
    # energies = []
    energy = ''
    for beam in dataset.BeamSequence:
        # ignore setup beams
        if beam.BeamDescription == "SETUP beam":
            continue

        # TODO extra LVL3 files given by client are still showing all STANDARD; need to confirm that one of them really
        #      is meant to be FFF so we can say this parameter is a bust or some other method is required.
        # Nominal Beam Energy (MV) + Fluence Mode(STANDARD/NONSTANDARD)
        energy = beam.ControlPointSequence[first_sequence_item].NominalBeamEnergy
        # Fluence Mode, which may indicate if dose is Flattening Filter Free (but might not! DICOM standard defines it as optional)
        #  -STANDARD     -> not FFF
        #  -NON_STANDARD -> check Fluence Mode ID for a short description of the fluence mode (could be FFF)
        if beam.PrimaryFluenceModeSequence[first_sequence_item].FluenceMode != 'STANDARD':
            energy += beam.PrimaryFluenceModeSequence[first_sequence_item].FluenceModeID

        # energies.append(energy)
    return energy


# just a placeholder function to indicate which parameter extractions have not been implemented
def to_be_implemented(dataset):
    return NOT_IMPLEMENTED_STRING


extractor_functions = {
    'mode req': _extract_mode,
    'prescription dose/#': _extract_prescription_dose,
    'prescription point': to_be_implemented,
    'isocentre point': to_be_implemented,
    'override': to_be_implemented,
    # I suspect override is at (3008, 0066) tag in the DICOM file but I'm not sure
    'collimator': _extract_collimator,
    'gantry': _extract_gantry,
    'SSD': _extract_ssd,
    'couch': to_be_implemented,
    'field size': _extract_field_size,
    'wedge': _extract_wedge,
    'meas': to_be_implemented,
    'energy': _extract_energy,
    #   'monitor unit'            : # dataset.FractionGroupSequence[0].ReferencedBeamSequence[i].BeamMeterset
}
