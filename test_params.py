''' Tests for parameters extraction and evaluation

This module contains a number of tests using python's unittest library.
See https://docs.python.org/3/library/unittest.html for more information about unittest.

- TestEvaluation is a collection of tests on the parameter evaluation: given a set of parameters, 
   it verifies that the pass/fail results are as expected
- TestIMRTExtractionValues is a collection of tests verifying that the correct values are extracted from IMRT file (YellowLvlIII_7a.dcm)
- TestVMATExtractionValues is a collection of tests verifying that the correct values are extracted from VMAT file (YellowLvlIII_7b.dcm)

The 2 dicom files are included in the Documents subdirectory.
The correct values for each test are derived from the corresponding pdf reports in each of IMRT and VMAT directories (7a.pdf, 7b.pdf).

Basic method to run all tests: `python -m unittest`
Detailed instructions for running tests are in the README. 
'''
import unittest
import pydicom
from parameter_retrieval import extract_parameters, evaluate_parameters

class TestIMRTExtractionValues(unittest.TestCase):
    ''' Tests for verifying the correct values are extracted for IMRT file
    The 'correct' answers are derived from the vendor report: Documents/Input/7a.pdf
    '''
    @classmethod
    def setUpClass(self):
        # We do some set up that is useful across tests in this class 
        # i.e. running the extraction function once and using the result for each test differently
        self.extracted, _ = extract_parameters('./Documents/Input/YellowLvlIII_7a.dcm', 6)

    def test_prescription_dose(self):
        self.assertEqual(self.extracted['prescription dose/#'], f'{50}/{25}')

    def test_collimator(self):
        self.assertEqual(self.extracted['collimator'], f'{0}')

    def test_gantry_angle(self):
        self.assertEqual(self.extracted['gantry'], f'{150},{60},{0},{300},{210}')

    def test_ssd(self):
        #don't agree with this an an extraction output; 
        # - the pdf has SSDs as 85.19, 89.42, 92.67 89.57, 85.19
        # - testing against this is no longer in the spirit of using the pdf as a reference
        self.assertEqual(self.extracted['SSD'], f'?,89,93,89,?')

    def test_energy(self):
        self.assertEqual(self.extracted['energy'], 6.0)

    def test_wedge_angles(self):
        # TODO Can't find this in pdf
        # self.assertEqual(f'{0},{0},{0},{0},{0}',self.extracted['wedge']) 
        pass

class TestVMATExtractionValues(unittest.TestCase):
    ''' Tests for verifying the correct values are extracted
    The 'correct' answers are derived from the vendor report: Documents/Input/7b.pdf
    '''
    @classmethod
    def setUpClass(self):
        # We do some set up that is useful across tests in this class 
        # i.e. running the extraction function once and using the result for each test differently
        temp_case = 6 #TODO is case for this really 6?
        self.extracted, _ = extract_parameters('./Documents/Input/YellowLvlIII_7b.dcm', temp_case)

    def test_prescription_dose(self):
        self.assertEqual(self.extracted['prescription dose/#'], f'{50}/{25}')

    def test_collimator(self):
        self.assertEqual(self.extracted['collimator'], f'{355}')

    def test_gantry_angle(self):
        #TODO PDF shows 180/360 for a single beam for this one, 
        # - Naturally this is because of VMAT style of rotating the beam around the patient
        # - In the dicom, the first ControlPointSequuence item is at 180, 
        #   does a 360 loop around back to 180, then 360 again back the other way to 180
        # The only thing is, how are we planning to display this? what value should we show? After we decide I'll update this test case
        # self.assertEqual(f'{180}', self.extracted['gantry']) 
        self.assertEqual(self.extracted['gantry'], 'VMAT File') 

    def test_ssd(self):
        self.assertEqual(self.extracted['SSD'], f'{87.17}')

    def test_energy(self):
        self.assertEqual(self.extracted['energy'], 6.0)

    def test_wedge_angles(self):
        # self.assertEqual(f'{0},{0},{0},{0},{0}',self.extracted['wedge'])
        pass

class TestEvaluation(unittest.TestCase):
    ''' Tests for verifying that parameters are passed and failed correctly
    The correct answers are derived from the truth table 

    Note that values of -1 are used for parameters where any value should be accepted (until a better representation is found)
    '''
    @classmethod
    def setUpClass(self):
        # If all parameters pass, evaluate_parameters should return this.
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
        self.maxDiff = None

    def test_case_1(self):
        # passing_parameters is one of a few possible passing sets of parameters
        # We don't cover every possible success/failure data point because the number of possiblities is too large;
        #  just a single point for each is used
        case = 1
        passing_parameters = {
            'mode req':'False',
            'prescription dose/#':'2',
            'prescription point':'1',
            'isocentre point':'surf',
            'override':'bone',
            'collimator':'0',
            'gantry':'0',
            'SSD':'100',
            'couch':'-1',
            'field size':'10x10',
            'wedge':'0',
            'meas':"'1','3','10','-','-','-','-','-','-'",#TODO disagree with this meas(ure) format
            'energy':"6,6FFF,10,10FFF,18"
        }
        treatment_type = 'IMRT'
        self.assertEqual(evaluate_parameters(passing_parameters, case, treatment_type), self.pass_evaluation)
        
        # failing_parameters is one of a few possible failing sets of parameters
        failing_parameters = {
            'mode req':'True',
            'prescription dose/#':'2',
            'prescription point':'1',
            'isocentre point':'surf',
            'override':'bone',
            'collimator':'0',
            'gantry':'0',
            'SSD':'100',
            'couch':'-1',
            'field size':'10x10',
            'wedge':'0',
            'meas':"'1','3','10'",
            'energy':"6,6FFF,10,10FFF,18"
        }
        self.assertNotEqual(evaluate_parameters(failing_parameters, case, treatment_type), self.pass_evaluation)

    def test_case_2(self):
        case = 2
        passing_parameters = {
            'mode req':'False',
            'prescription dose/#':'2',
            'prescription point':'5',
            'isocentre point':'3',
            'override':'no override',
            'collimator':'-1',
            'gantry':'270,0,90',
            'SSD':'86,93,86',
            'couch':'-1',
            'field size':'10x6,10x12,10x6',
            'wedge':'30,0,30',
            'meas':"'5_RLAT','8_RLAT','5_AP','8_AP','5_LLAT','8_LLAT','-','-','-'",
            'energy':"6,6FFF,10,10FFF,18"
        }
        treatment_type = 'IMRT'
        self.assertEqual(evaluate_parameters(passing_parameters, case, treatment_type), self.pass_evaluation)
        
        failing_parameters = {
            'mode req':'False',
            'prescription dose/#':'2',
            'prescription point':'1',
            'isocentre point':'surf',
            'override':'bone',
            'collimator':'0',
            'gantry':'0',
            'SSD':'100',
            'couch':'-1',
            'field size':'10x10',
            'wedge':'0',
            'meas':"'1','3','10'",
            'energy':"6,6FFF,10,10FFF,18"
        }
        self.assertNotEqual(evaluate_parameters(failing_parameters, case, treatment_type), self.pass_evaluation)

    def test_case_3(self):
        case = 3
        passing_parameters = {
            'mode req':'False',
            'prescription dose/#':'2',
            'prescription point':'3',
            'isocentre point':'3',
            'override':'no override',
            'collimator':'-1',
            'gantry':'90',
            'SSD':'86',
            'couch':'-1',
            'field size':'10x12',
            'wedge':'0',
            'meas':"'3','5','-','-','-','-','-','-','-'",
            'energy':"6,6FFF,10,10FFF,18"
        }
        treatment_type = 'IMRT'
        self.assertEqual(evaluate_parameters(passing_parameters, case, treatment_type), self.pass_evaluation)
        
        failing_parameters = {
            'mode req':'True',
            'prescription dose/#':'2',
            'prescription point':'1',
            'isocentre point':'surf',
            'override':'bone',
            'collimator':'0',
            'gantry':'0',
            'SSD':'100',
            'couch':'-1',
            'field size':'10x10',
            'wedge':'0',
            'meas':"'1','3','10'",
            'energy':"6,6FFF,10,10FFF,18"
        }
        self.assertNotEqual(evaluate_parameters(failing_parameters, case, treatment_type), self.pass_evaluation)

    #TODO add cases up till 18??? wew


if __name__ == '__main__':
    unittest.main()


