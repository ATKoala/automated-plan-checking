# I think the main parameters left to extract are collimator and wedge angle (and maybe overide) before we get into the harder stuff
# We are going to get sent files on Monday 7/9 which should help
# and also we need to code in exceptions where particular values don't exist

#The pydicom library needs to be installed first

import pydicom

#define the filepath
filepath="../data/first samples/IMRT DICOM sample/YellowLvlIII_7a.dcm"

dataset=pydicom.read_file(filepath, force=True)

## Number of Beams
print("The number of beams is: " + str(len(dataset.BeamSequence))+"\n")
i=0
while i<len(dataset.BeamSequence):
    if dataset.BeamSequence[i].BeamDescription!="SETUP beam":
        print("beam #: "+ str(dataset.BeamSequence[i].BeamNumber))

        #target perscription dose is not complete and is probably wrong
        print("The target perscription dose is: "+ str(dataset.DoseReferenceSequence[0].TargetPrescriptionDose))

        # can't figure out how to find wedge angle
        # the tag is (300a,00D5) for wedge angle
        print("The number of Wedges is: "+ str(dataset.BeamSequence[i].NumberOfWedges))

        ## GantryAngle 
        print("The Gantry Angle is: " + str(dataset.BeamSequence[i].ControlPointSequence[0].GantryAngle))

        # SSD in millimetres
        print("Source to Surface Distance in centimetres: " + str(dataset.BeamSequence[i].ControlPointSequence[0].SourceToSurfaceDistance/10))

        # number of fractions
        print("The number of fractions planned is: " + str(dataset.FractionGroupSequence[0].NumberOfFractionsPlanned))

        #Nominal Beam Energy (only number)
        print("The Nominal Beam Energy is: "+ str(dataset.BeamSequence[i].ControlPointSequence[0].NominalBeamEnergy))

        print("The Monitor Units is: " + str(dataset.FractionGroupSequence[0].ReferencedBeamSequence[i].BeamMeterset))
        
        
        # I suspect override is at (3008, 0066)
        
        # Total Prescription Dose
        print("The Total Prescription Dose is: "+ str(dataset.DoseReferenceSequence[0].TargetPrescriptionDose))

        print("\n")
    i+=1
