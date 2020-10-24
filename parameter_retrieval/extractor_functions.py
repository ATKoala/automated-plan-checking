# We are mostly using parameters from the first item of Sequences; is this ok?  
first_sequence_item = 0

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
    strings.prescription_point      : to_be_implemented, 
    strings.isocenter_point         : to_be_implemented,
        # Isocenter Position TODO:Figuring out what does "SoftTiss" etc means
        # parameter_values["Isocenter Position"] = dataset.BeamSequence[i].ControlPointSequence[0].IsocenterPosition
    strings.override                : to_be_implemented, 
        #I suspect override is at (3008, 0066) tag in the DICOM file but I'm not sure
    strings.collimator              : _extract_collimator, 
    strings.gantry                  : _extract_gantry, 
    strings.SSD                     : _extract_ssd, 
    strings.couch                   : to_be_implemented, 
    strings.field_size              : to_be_implemented,
    strings.wedge                   : _extract_wedge, 
    strings.meas                    : to_be_implemented, 
    strings.energy                  : _extract_energy,
#   'monitor unit'            : # dataset.FractionGroupSequence[0].ReferencedBeamSequence[i].BeamMeterset
}
