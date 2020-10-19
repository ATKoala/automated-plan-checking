''' Tests for Parameter Extraction and Evaluation

This module contains a number of tests using python's unittest library.
See https://docs.python.org/3/library/unittest.html for more information about unittest.

- TestIMRTExtractionValues is a collection of tests verifying that the correct values are extracted from IMRT file (YellowLvlIII_7a.dcm)
- TestVMATExtractionValues is a collection of tests verifying that the correct values are extracted from VMAT file (YellowLvlIII_7b.dcm)
- TestEvaluation is a collection of tests on the parameter evaluation: given a set of parameters, 
   it verifies that the pass/fail results are as expected

The 2 DICOM files tested are included in the Resources subdirectory.
The correct values for each test are derived from the corresponding pdf reports in each of IMRT and VMAT directories (7a.pdf, 7b.pdf).

Basic method to run all tests: `python -m unittest`
Detailed instructions for running tests are in the README. 
'''
import unittest
import pydicom
from parameter_retrieval import extract_parameters, evaluate_parameters

class TestIMRTExtractionValues(unittest.TestCase):
    ''' Tests for verifying the correct values are extracted for IMRT file
    The 'correct' answers are derived from the vendor report in Documents/Input/7a.pdf
    '''
    @classmethod
    def setUpClass(self):
        # We use the extraction function once here and inspect the results in the tests below
        self.extracted, _ = extract_parameters('./Resources/Input/YellowLvlIII_7a.dcm')

    def test_prescription_dose(self):
        self.assertEqual(self.extracted['prescription dose/#'], '50/25')

    def test_collimator(self):
        self.assertEqual(self.extracted['collimator'], '0')

    def test_gantry_angle(self):
        self.assertEqual(self.extracted['gantry'], '150,60,0,300,210')

    def test_ssd(self):
        # Notes on extraction output for this test
        # - The pdf has SSDs as 85.19, 89.42, 92.67 89.57, 85.19 for the beams
        # - But, currently testing using the string value for compatability with existing code
        self.assertEqual(self.extracted['SSD'], [85.19,89.42,92.67,89.57,85.19])

    def test_energy(self):
        self.assertEqual(self.extracted['energy'], 6.0)

    def test_wedge_angles(self):
        # Note: extraction function returns 0,0,0,0,0 for the 5 beams respectively
        #       but can't find this parameter through the pdf, so it's improper to test it.
        pass

class TestVMATExtractionValues(unittest.TestCase):
    ''' Tests for verifying the correct values are extracted
    The 'correct' answers are derived from the vendor report: Documents/Input/7b.pdf
    '''
    @classmethod
    def setUpClass(self):
        # We use the extraction function once here and inspect the results in the tests below
        self.extracted, _ = extract_parameters('./Resources/Input/YellowLvlIII_7b.dcm')

    def test_prescription_dose(self):
        self.assertEqual(self.extracted['prescription dose/#'], '50/25')

    def test_collimator(self):
        self.assertEqual(self.extracted['collimator'], '355')

    def test_gantry_angle(self):
        #  Report shows '180/360' for a single beam for this plan
        # - Naturally this is because of VMAT style of rotating the beam around the patient
        # - In the dicom, the initial position is at 180, turns 360deg one way, then 360 again back the other way
        # Testing against the string 'VMAT File' for compatibility with existing code
        self.assertEqual(self.extracted['gantry'], 'VMAT File') 

    def test_ssd(self):
        self.assertEqual(self.extracted['SSD'], [87.17])

    def test_energy(self):
        self.assertEqual(self.extracted['energy'], 6.0)

    def test_wedge_angles(self):
        # Note: extraction function returns 0,0,0,0,0 for the 5 beams respectively
        #       but can't find this parameter through the pdf, so it's improper to test it.
        pass

truth_table = {
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

class TestEvaluation(unittest.TestCase):
    ''' Tests for verifying that parameter sets are passed correctly
    Each case (from 1-17) of the truth table has its own test against a set of parameters that *should* pass.
    It's currently infeasible to test every possible combination of pass/failure values, this is just a basic check. 
    Also, the correct answers are derived from the truth table. 

    Note that values of None are used for parameters where any value should be accepted.
    Note that modalities are IMRT for all cases; TODO check if that's ok.
    '''
    @classmethod
    def setUpClass(self):
        # If all parameters pass, evaluate_parameters() should return this.
        # We'll use this to compare with the actual results in our tests below
        self.pass_evaluation = {
            'mode req':'PASS',
            'prescription dose/#':'PASS',
            'prescription point':'PASS',
            'isocentre point':'PASS',
            'override':'PASS',
            'collimator':'PASS',
            'gantry':'PASS',
            'SSD':'PASS',
            'couch':'PASS',
            'field size':'PASS',
            'wedge':'PASS',
            'meas':'PASS',
            'energy':'PASS'
        }

    def test_case_1(self):
        case = 1
        passing_parameters = {
            'mode req':'False',
            'prescription dose/#':'2',
            'prescription point':'1 or 3',
                #TODO Think this should work for either 1 or 3, not the string "1 or 3"? 
            'isocentre point':'surf',
            'override':'bone',
            'collimator':'0',
            'gantry':'0',
            'SSD':[100],
            'couch':None,
            'field size':'10x10',
            'wedge':'0',
            'meas':"'1','3','10','-','-','-','-','-','-'",
            'energy':"6,6FFF,10,10FFF,18"
        }
        treatment_type = 'IMRT'
        self.assertEqual(evaluate_parameters(passing_parameters, truth_table, case, treatment_type), self.pass_evaluation)

    def test_case_2(self):
        case = 2
        passing_parameters = {
            'mode req':'False',
            'prescription dose/#':'2',
            'prescription point':'5',
            'isocentre point':'3',
            'override':'no override',
            'collimator':None,
            'gantry':'270,0,90',
            'SSD':[86,93,86],
            'couch':None,
            'field size':'10x6,10x12,10x6',
            'wedge':'30,0,30',
            'meas':"'5_RLAT','8_RLAT','5_AP','8_AP','5_LLAT','8_LLAT','-','-','-'",
            'energy':"6,6FFF,10,10FFF,18"
        }
        treatment_type = 'IMRT'
        self.assertEqual(evaluate_parameters(passing_parameters, truth_table, case, treatment_type), self.pass_evaluation)

    def test_case_3(self):
        case = 3
        passing_parameters = {
            'mode req':'False',
            'prescription dose/#':'2',
            'prescription point':'3',
            'isocentre point':'3',
            'override':'no override',
            'collimator':None,
            'gantry':'90',
            'SSD':[86],
            'couch':None,
            'field size':'10x12',
            'wedge':'0',
            'meas':"'3','5','-','-','-','-','-','-','-'",
            'energy':"6,6FFF,10,10FFF,18"
        }
        treatment_type = 'IMRT'
        self.assertEqual(evaluate_parameters(passing_parameters, truth_table, case, treatment_type), self.pass_evaluation)

    def test_case_4(self):
        case = 4
        passing_parameters = {
            'mode req':'False',
            'prescription dose/#':'2',
            'prescription point':'3',
            'isocentre point':'3',
            'override':'no override',
            'collimator':None,
            'gantry':'90',
            'SSD':[86],
            'couch':None,
            'field size':'10x12',
            'wedge':'60',
            'meas':"'3','5','-','-','-','-','-','-','-'",
            'energy':"6,6FFF,10,10FFF,18"
        }
        treatment_type = 'IMRT'
        self.assertEqual(evaluate_parameters(passing_parameters, truth_table, case, treatment_type), self.pass_evaluation)
        
    def test_case_5(self):
        case = 5
        passing_parameters = {
            'mode req':'False',
            'prescription dose/#':'50/25',
            'prescription point':'chair',
            'isocentre point':'3',
            'override':'no override',
            'collimator':'0',
            'gantry':'0',
            'SSD':[93],
            'couch':None,
            'field size':None,
            'wedge':None,
            'meas':"'11','12','13','14','15','18','19','20','21'",
            'energy':"6,6FFF,10,10FFF,18"
        }
        treatment_type = 'IMRT'
        self.assertEqual(evaluate_parameters(passing_parameters, truth_table, case, treatment_type), self.pass_evaluation)

    def test_case_6(self):
        case = 6
        passing_parameters = {
            'mode req':'True',
            'prescription dose/#':'50/25',
            'prescription point':'CShape',
            'isocentre point':'3',
            'override':'lungs',
            'collimator':None,
            'gantry':'150,60,0,300,210',
            'SSD':[None,89,93,89,None],
            'couch':'couch?',
            'field size':None,
            'wedge':None,
            'meas':"'11','12','13','14','15','16','17','-','-'",
            'energy':"6,6FFF,10,10FFF,18"
        }
        treatment_type = 'IMRT'
        self.assertEqual(evaluate_parameters(passing_parameters, truth_table, case, treatment_type), self.pass_evaluation)

    def test_case_7(self):
        case = 7
        passing_parameters = {
            'mode req':'True',
            'prescription dose/#':'50/25',
            'prescription point':'CShape',
            'isocentre point':'3',
            'override':'no override',
            'collimator':None,
            'gantry':'150,60,0,300,210',
            'SSD':[None,89,93,89,None],
            'couch':'couch?',
            'field size':None,
            'wedge':None,
            'meas':"'11','12','13','14','15','16','17','-','-'",
            'energy':"6,6FFF,10,10FFF,18"
        }
        treatment_type = 'IMRT'
        self.assertEqual(evaluate_parameters(passing_parameters, truth_table, case, treatment_type), self.pass_evaluation)

    def test_case_8(self):
        case = 8
        passing_parameters = {
            'mode req':'True',
            'prescription dose/#':'50/25',
            'prescription point':'C8Target',
            'isocentre point':'3',
            'override':'no override',
            'collimator':None,
            'gantry':'150,60,0,300,210',
            'SSD':[None,89,93,89,None],
            'couch':'couch?',
            'field size':None,
            'wedge':None,
            'meas':"'11','12','13','14','15','17','18','-','-'",
            'energy':"6,6FFF,10,10FFF,18"
        }
        treatment_type = 'IMRT'
        self.assertEqual(evaluate_parameters(passing_parameters, truth_table, case, treatment_type), self.pass_evaluation)

    def test_case_9(self):
        case = 9
        passing_parameters = {
            'mode req':'False',
            'prescription dose/#':'900/3 MU',
            'prescription point':'C8Target',
            'isocentre point':'SoftTiss',
            'override':'lungs',
            'collimator':None,
            'gantry':None,
            'SSD':[90],
            'couch':None,
            'field size':'3x3,2x2,1x1',
            'wedge':None,
            'meas':"'SoftTiss_3','SoftTiss_2','SoftTiss_1','-','-','-','-','-','-'",
            'energy':"6,6FFF,10,10FFF,18"
        }
        treatment_type = 'IMRT'
        self.assertEqual(evaluate_parameters(passing_parameters, truth_table, case, treatment_type), self.pass_evaluation)

    def test_case_10(self):
        case = 10
        passing_parameters = {
            'mode req':'True',
            'prescription dose/#':'45/3',
            'prescription point':'SoftTissTarget',
            'isocentre point':'SoftTiss',
            'override':'lungs',
            'collimator':None,
            'gantry':None,
            'SSD':None,
            'couch':'couch?',
            'field size':None,
            'wedge':None,
            'meas':"'SoftTiss','-','-','-','-','-','-','-','-'",
            'energy':"6,6FFF,10,10FFF,18"
        }
        treatment_type = 'IMRT'
        self.assertEqual(evaluate_parameters(passing_parameters, truth_table, case, treatment_type), self.pass_evaluation)


    def test_case_11(self):
        case = 11
        passing_parameters = {
            'mode req':'True',
            'prescription dose/#':'24/2',
            'prescription point':'SpineTarget',
            'isocentre point':'Spine',
            'override':'no override',
            'collimator':None,
            'gantry':None,
            'SSD':None,
            'couch':'couch?',
            'field size':None,
            'wedge':None,
            'meas':"'Spine2Inf','Spine1Sup','Cord','-','-','-','-','-','-'",
            'energy':"6,6FFF,10,10FFF,18"
        }
        treatment_type = 'IMRT'
        self.assertEqual(evaluate_parameters(passing_parameters, truth_table, case, treatment_type), self.pass_evaluation)

    def test_case_12(self):
        case = 12
        passing_parameters = {
            'mode req':'True',
            'prescription dose/#':'48/4',
            'prescription point':'LungTarget',
            'isocentre point':'Lung',
            'override':'no override',
            'collimator':None,
            'gantry':None,
            'SSD':None,
            'couch':'couch?',
            'field size':None,
            'wedge':None,
            'meas':"'Lung','-','-','-','-','-','-','-','-'",
            'energy':"6,6FFF,10,10FFF,18"
        }
        treatment_type = 'IMRT'
        self.assertEqual(evaluate_parameters(passing_parameters, truth_table, case, treatment_type), self.pass_evaluation)

    def test_case_13(self):
        case = 13
        passing_parameters = {
            'mode req':'True',
            'prescription dose/#':'3',
            'prescription point':'1',
            'isocentre point':'1',
            'override':'central cube',
            'collimator':None,
            'gantry':None,
            'SSD':None,
            'couch':None,
            'field size':'3x3',
            'wedge':None,
            'meas':"'1_3','4_3','-','-','-','-','-','-','-'",
            'energy':"6,6FFF,10,10FFF,18"
        }
        treatment_type = 'IMRT'
        self.assertEqual(evaluate_parameters(passing_parameters, truth_table, case, treatment_type), self.pass_evaluation)


    def test_case_14(self):
        case = 14
        passing_parameters = {
            'mode req':'True',
            'prescription dose/#':'3',
            'prescription point':'1',
            'isocentre point':'1',
            'override':'central cube',
            'collimator':None,
            'gantry':None,
            'SSD':None,
            'couch':None,
            'field size':'1.5x1.5',
            'wedge':None,
            'meas':"'1_1.5','4_1.5','-','-','-','-','-','-','-'",
            'energy':"6,6FFF,10,10FFF,18"
        }
        treatment_type = 'IMRT'
        self.assertEqual(evaluate_parameters(passing_parameters, truth_table, case, treatment_type), self.pass_evaluation)


    def test_case_15(self):
        case = 15
        passing_parameters = {
            'mode req':'True',
            'prescription dose/#':'20',
            'prescription point':'PTV_c14_c15',
            'isocentre point':'1',
            'override':'central cube',
            'collimator':None,
            'gantry':None,
            'SSD':None,
            'couch':'couch?',
            'field size':None,
            'wedge':None,
            'meas':"'1','3','-','-','-','-','-','-','-'",
            'energy':"6,6FFF,10,10FFF,18"
        }
        treatment_type = 'IMRT'
        self.assertEqual(evaluate_parameters(passing_parameters, truth_table, case, treatment_type), self.pass_evaluation)

    def test_case_16(self):
        case = 16
        passing_parameters = {
            'mode req':'True',
            'prescription dose/#':'20',
            'prescription point':None,
            'isocentre point':None,
            'override':'central cube',
            'collimator':None,
            'gantry':None,
            'SSD':None,
            'couch':'couch?',
            'field size':None,
            'wedge':None,
            'meas':"'1','3','-','-','-','-','-','-','-'",
            'energy':"6,6FFF,10,10FFF,18"
        }
        treatment_type = 'IMRT'
        self.assertEqual(evaluate_parameters(passing_parameters, truth_table, case, treatment_type), self.pass_evaluation)

    def test_case_17(self):
        case = 17
        passing_parameters = {
            'mode req':'True',
            'prescription dose/#':'20',
            'prescription point':None,
            'isocentre point':None,
            'override':'central cube',
            'collimator':None,
            'gantry':None,
            'SSD':None,
            'couch':'couch?',
            'field size':None,
            'wedge':None,
            'meas':"'1','2','3','-','-','-','-','-','-'",
            'energy':"6,6FFF,10,10FFF,18"
        }
        treatment_type = 'IMRT'
        self.assertEqual(evaluate_parameters(passing_parameters, truth_table, case, treatment_type), self.pass_evaluation)

if __name__ == '__main__':
    unittest.main()


