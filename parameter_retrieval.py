# I think the main parameters left to extract are collimator and wedge angle (and maybe overide) before we get into the harder stuff
# We are going to get sent files on Monday 7/9 which should help
# and also we need to code in exceptions where particular values don't exist

#The pydicom library needs to be installed first
import pydicom as dicom

def retrieve_parameters(filepath):
	dataset = dicom.read_file(filepath, force=True)
	parameters = {}

	## Number of Beams
	#print("The number of beams is: " + str(len(dataset.BeamSequence))+"\n")
	parameters["Number of Beams"] = len(dataset.BeamSequence)
	parameters["Beams"] = []
	i=0
	while i<len(dataset.BeamSequence):
		if dataset.BeamSequence[i].BeamDescription!="SETUP beam":
			beam = {}
			#print("beam #: "+ str(dataset.BeamSequence[i].BeamNumber))
			beam["Beam Number"] = dataset.BeamSequence[i].BeamNumber

			#target perscription dose is not complete and is probably wrong
			#print("The target perscription dose is: "+ str(dataset.DoseReferenceSequence[0].TargetPrescriptionDose))

			# can't figure out how to find wedge angle
			# the tag is (300a,00D5) for wedge angle
			#print("The number of Wedges is: "+ str(dataset.BeamSequence[i].NumberOfWedges))
			beam["Number of Wedges"] = dataset.BeamSequence[i].NumberOfWedges

			## GantryAngle 
			#print("The Gantry Angle is: " + str(dataset.BeamSequence[i].ControlPointSequence[0].GantryAngle))
			beam["Gantry Angle"] = dataset.BeamSequence[i].ControlPointSequence[0].GantryAngle

			# SSD in millimetres
			#print("Source to Surface Distance in centimetres: " + str(dataset.BeamSequence[i].ControlPointSequence[0].SourceToSurfaceDistance/10))
			beam["Source to Surface Distance in centimetres"] = dataset.BeamSequence[i].ControlPointSequence[0].SourceToSurfaceDistance/10

			# number of fractions
			#print("The number of fractions planned is: " + str(dataset.FractionGroupSequence[0].NumberOfFractionsPlanned))
			beam["Number of Fractions Planned"] = dataset.FractionGroupSequence[0].NumberOfFractionsPlanned

			#Nominal Beam Energy (only number)
			#print("The Nominal Beam Energy is: "+ str(dataset.BeamSequence[i].ControlPointSequence[0].NominalBeamEnergy))
			beam["Nominal Beam Energy"] = dataset.BeamSequence[i].ControlPointSequence[0].NominalBeamEnergy

			#print("The Monitor Units is: " + str(dataset.FractionGroupSequence[0].ReferencedBeamSequence[i].BeamMeterset))
			beam["Monitor Units"] = dataset.FractionGroupSequence[0].ReferencedBeamSequence[i].BeamMeterset
			
			parameters["Beams"].append(beam)
		i+=1

	return parameters