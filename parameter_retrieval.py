"""
The function to extract parameters from the specified DICOM file.
"""

# We import the pydicom library to use it's DICOM reading methods
import pydicom as dicom

# TODO investigate whther it's ok to just look for the first item of the sequences
first_sequence_item = 0

def extract_parameters(filepath):
    dataset = dicom.read_file(filepath, force=True)
    parameters = {}

    # Number of Beams
    parameters["Number of Beams"] = len(dataset.BeamSequence)
    parameters["Beams"] = []
    i = 0
    while i < len(dataset.BeamSequence):
        if dataset.BeamSequence[i].BeamDescription != "SETUP beam":
            beam = {}
            beam["Beam Number"] = dataset.BeamSequence[i].BeamNumber

            # can't figure out how to find wedge angle
            # the tag is (300a,00D5) for wedge angle
            # print("The number of Wedges is: "+ str(dataset.BeamSequence[i].NumberOfWedges))
            beam["Number of Wedges"] = dataset.BeamSequence[i].NumberOfWedges

            # Gantry Angle
            beam["Gantry Angle"] = dataset.BeamSequence[i].ControlPointSequence[first_sequence_item].GantryAngle

            # SSD in cm. Originally in millimeters, we convert to cm  
            beam["Source to Surface Distance in centimetres"] = \
                dataset.BeamSequence[i].ControlPointSequence[first_sequence_item].SourceToSurfaceDistance / 10

            # Nominal Beam Energy (MV) + Fluence Mode(FFF)
            beam["Nominal Beam Energy"] = dataset.BeamSequence[i].ControlPointSequence[first_sequence_item].NominalBeamEnergy
            # Fluence Mode, which may indicate if dose is Flattening Filter Free (but might not! DICOM standard defines it as optional)
            #  -STANDARD     -> not FFF
            #  -NON_STANDARD -> check Fluence Mode ID for a short description of the fluence mode
            beam["Fluence Mode"] = dataset.BeamSequence[i].PrimaryFluenceModeSequence[first_sequence_item].FluenceMode

            # Total Prescription Dose + Number of fractions
            beam["Total Prescription Dose"] = dataset.DoseReferenceSequence[first_sequence_item].TargetPrescriptionDose
            # Number of fractions - how many fractions the total dose is split up into for treatment
            beam["Number of Fractions Planned"] = dataset.FractionGroupSequence[first_sequence_item].NumberOfFractionsPlanned

            # Monitor Units aka MU aka meterset
            beam["Monitor Units"] = dataset.FractionGroupSequence[0].ReferencedBeamSequence[i].BeamMeterset

            parameters["Beams"].append(beam)
        i += 1

    return parameters
