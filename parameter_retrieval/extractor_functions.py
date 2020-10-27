import strings
first_sequence_item = 0

def _extract_mode(dataset, case):
    # For now, we are only producing IMRT vs VMAT modes for cases 6, 7, and 8
    if case not in [6, 7, 8]:
        return strings.NOT_IMPLEMENTED

    moving_gantry = int(dataset.BeamSequence[0].ControlPointSequence[0].GantryAngle) != \
                            int(dataset.BeamSequence[0].ControlPointSequence[1].GantryAngle)

    # One beam will be the setup beam, which is not counted
    number_of_beams = len(dataset.BeamSequence) - 1

    # If IMRT there should be 5 static gantry positions (5 beams) for each case, and the intensity of the 
    # beam is modulated by moving the multi leaf collimator (MLC) to different control points within each 
    # gantry angle. If VMAT the gantry and the MLCs all move at the same time so each control point has 
    # both gantry moves and MLC moves.
    if moving_gantry:
        mode = strings.VMAT
    elif not moving_gantry and number_of_beams is 5:
        mode = strings.IMRT
    else:
        mode = "UNKNOWN"
    return mode

def _extract_prescription_dose(dataset, case):
    total_prescription_dose = str(int(dataset.DoseReferenceSequence[0].TargetPrescriptionDose))
    number_of_fractions = str(dataset.FractionGroupSequence[0].NumberOfFractionsPlanned)

    # This section deals with the 'prescription dose/#' parameter
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

def _extract_collimator(dataset, case):
    #ignore setup beams
    beams = list(filter(lambda beam: beam.BeamDescription != strings.SETUP_beam, dataset.BeamSequence))
    # record collimator value in the parameter_values dictionary as a string to be consistant with truth_table format 
    # According to the truth table the collimator only needs to be recorded for cases 1&5 where only 1 beam occurs    
    collimator_value = beams[len(beams)-1].ControlPointSequence[0].BeamLimitingDeviceAngle
    return str(int(collimator_value))

def _extract_gantry(dataset, case):
    try:
        file_type = _extract_mode(dataset, case)

        #If the dataset is a VMAT file it goes through each of the control point sequence and finds each associated gantry angle and returns the lowest value slash the highest value
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

def _extract_ssd(dataset, case):
    #find SSD in centimeters
    file_type = _extract_mode(dataset, case)

    ssd_list = []
    try:
        if file_type == strings.VMAT:
            i = 0
            vmat_ssd_list = []
            while i < len(dataset.BeamSequence):
                if dataset.BeamSequence[i].BeamDescription != strings.SETUP_beam:
                    for control_point in dataset.BeamSequence[i].ControlPointSequence:
                        vmat_ssd_list.append(round(float(control_point.ReferencedDoseReferenceSequence[1].BeamDosePointSSD)/10,2))
                    return vmat_ssd_list
                i+=1
            return "error retrieving SSD"
        else:
            #ignore setup beams
            beams = list(filter(lambda beam: beam.BeamDescription != strings.SETUP_beam, dataset.BeamSequence))
            #obtain the ssd of all beams
            #in the DICOM file the SSD is given in millimetres so its divided by 10 so its in centimetres
            ssd_list = list(map(lambda beam: round(beam.ControlPointSequence[0].SourceToSurfaceDistance / 10, 2), beams))
            return ssd_list
    except:
        return "error retrieving SSD"

def _extract_wedge(dataset, case):
    # It may need more work to deal with VMAT files for cases 6,7,8

    #ignore setup beams
    beams = list(filter(lambda beam: beam.BeamDescription != strings.SETUP_beam, dataset.BeamSequence))
    # if there are wedges, get the wedge angle of the beam. Otherwise, get 0
    wedge_angles = list(map(lambda beam: str(int(beam.WedgeSequence[0].WedgeAngle)) if int(beam.NumberOfWedges) > 0 else 'no wedge', beams))

    return ','.join(wedge_angles)

def _extract_energy(dataset, case):
    energy = ''

    for beam in dataset.BeamSequence:
        #ignore setup beams
        if beam.BeamDescription == strings.SETUP_beam:
            continue

        energy = str(int(beam.ControlPointSequence[first_sequence_item].NominalBeamEnergy))
        if beam.PrimaryFluenceModeSequence[first_sequence_item].FluenceMode != strings.STANDARD_FLUENCE:
            energy += str(beam.PrimaryFluenceModeSequence[first_sequence_item].FluenceModeID)
    return energy

def _extract_field_size(dataset, case):
    # ignore setup beams
    beams = list(filter(lambda beam: beam.BeamDescription != "SETUP beam", dataset.BeamSequence))
    # record collimator value in the parameter_values dictionary as a string to be consistant with truth_table format
    # According to the truth table the collimator only needs to be recorded for cases 1&5 where only 1 beam occurs

    field_size_list=[]

    for beam in beams:
        beam_type_number = len(beam.ControlPointSequence[0].BeamLimitingDevicePositionSequence)

        length_x = 0
        length_y = 0

        for i in range(beam_type_number):
            device_type = beam.ControlPointSequence[0].BeamLimitingDevicePositionSequence[
                i].RTBeamLimitingDeviceType
            jaw_position = beam.ControlPointSequence[0].BeamLimitingDevicePositionSequence[
                i].LeafJawPositions

            if device_type != "MLCX" and device_type != "MLCY":

                if device_type == "X":
                    length_x = int((-jaw_position[0] + jaw_position[1]) / 10)
                elif device_type == "Y":
                    length_y = int((-jaw_position[0] + jaw_position[1]) / 10)
                elif device_type == "ASYMX":
                    length_x = int((-jaw_position[0] + jaw_position[1]) / 10)
                elif device_type == "ASYMY":
                    length_y = int((-jaw_position[0] + jaw_position[1]) / 10)
                if length_x != 0 and length_y != 0:

                    field_size_list.append(str(length_y) + "x" + str(length_x))
            else:
                if length_x==0 or length_y==0:
                    field_size_list.append("Not Extracted")

    return ','.join(field_size_list)

#just a placeholder function to indicate which parameter extractions have not been implemented
def to_be_implemented(dataset, case):
    return strings.NOT_IMPLEMENTED

extractor_functions = {
    strings.mode                    : _extract_mode,
    strings.prescription_dose_slash_fractions     : _extract_prescription_dose,
    strings.prescription_point      : to_be_implemented,
    strings.isocenter_point         : to_be_implemented,
    strings.override                : to_be_implemented,
    strings.collimator              : _extract_collimator,
    strings.gantry                  : _extract_gantry,
    strings.SSD                     : _extract_ssd,
    strings.couch                   : to_be_implemented,
    strings.field_size              : _extract_field_size,
    strings.wedge                   : _extract_wedge,
    strings.meas                    : to_be_implemented,
    strings.energy                  : _extract_energy,
}
