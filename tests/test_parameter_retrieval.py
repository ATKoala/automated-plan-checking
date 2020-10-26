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
import strings
from parameter_retrieval.parameter_retrieval import extract_parameters, evaluate_parameters

class TestIMRTExtractionValues(unittest.TestCase): 
    ''' Tests for verifying the correct values are extracted for IMRT file
    The 'correct' answers are derived from the vendor report in Documents/Input/7a.pdf
    '''
    @classmethod
    def setUpClass(self): 
        # We use the extraction function once here and inspect the results in the tests below
        self.extracted, _ = extract_parameters('./Resources/Input/YellowLvlIII_7a.dcm')

    def test_field_size(self):
        self.assertEqual(self.extracted['field size'], '10x10')

    def test_prescription_dose(self): 
        self.assertEqual(self.extracted[strings.prescription_dose_slash_fractions], '50/25/-')

    def test_collimator(self): 
        self.assertEqual(self.extracted[strings.collimator], '0')

    def test_gantry_angle(self): 
        self.assertEqual(self.extracted[strings.gantry], '150,60,0,300,210')

    def test_ssd(self): 
        # Notes on extraction output for this test
        # - The pdf has SSDs as 85.19, 89.42, 92.67 89.57, 85.19 for the beams
        # - But, currently testing using the string value for compatability with existing code
        self.assertEqual(self.extracted[strings.SSD], [85.19,89.42,92.67,89.57,85.19])

    def test_energy(self): 
        self.assertEqual(self.extracted[strings.energy], 6.0)

    def test_wedge_angles(self): 
        # Note :  extraction function returns 0,0,0,0,0 for the 5 beams respectively
        #       but can't find this parameter through the pdf, so it's improper to test it.
        pass

class TestVMATExtractionValues(unittest.TestCase): 
    ''' Tests for verifying the correct values are extracted
    The 'correct' answers are derived from the vendor report :  Documents/Input/7b.pdf
    '''
    @classmethod
    def setUpClass(self): 
        # We use the extraction function once here and inspect the results in the tests below
        self.extracted, _ = extract_parameters('./Resources/Input/YellowLvlIII_7b.dcm')

    def test_prescription_dose(self):
        # test return 50/25/MU
        self.assertEqual(self.extracted[strings.prescription_dose_slash_fractions], '50/25/-')

    def test_collimator(self): 
        self.assertEqual(self.extracted[strings.collimator], '355')

    # can't confirm this in report
    # def test_field_size(self):
    #     self.assertEqual(self.extracted['field size'], '10x10')

    def test_gantry_angle(self):
        # test return big array 180->360->180->0->180
        self.assertEqual(self.extracted[strings.gantry], '180/360') 

    def test_ssd(self): 
        self.assertEqual(self.extracted[strings.SSD], [87.17])

    def test_energy(self): 
        self.assertEqual(self.extracted[strings.energy], 6.0)

    def test_wedge_angles(self): 
        # Note :  extraction function returns 0,0,0,0,0 for the 5 beams respectively
        #       but can't find this parameter through the pdf, so it's improper to test it.
        pass

truth_table = {
    strings.case :  ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17'],
    strings.mode_req :  ['False', 'False', 'False', 'False', 'False', 'True', 'True', 'True', 'False', 'True', 'True',
                'True', 'True', 'True', 'True', 'True', 'True'],
    strings.prescription_dose_slash_fractions : ['2/-/-', '2/-/-', '2/-/-', '2/-/-', '50/25/-', '50/25/-', '50/25/-', '50/25/-', '900/3/MU', '45/3/-', '24/2/-',
                            '48/4/-', '3/-/-', '3/-/-', '20/-/-', '20/-/-', '20/-/-'],
    strings.prescription_point : ['1 or 3', '5', '3', '3', 'chair', 'CShape', 'CShape', 'C8Target', '-', 'SoftTissTarget',
                        'SpineTarget', 'LungTarget', '1', '1', 'PTV_c14_c15', '-', '-'],
    strings.isocenter_point : ['surf', '3', '3', '3', '3', '3', '3', '3', 'SoftTiss', 'SoftTiss', 'Spine', 'Lung', '1',
                        '1', '1', '-', '-'],
    strings.override : ['bone', 'no override', 'no override', 'no override', 'no override', 'lungs', 'no override',
                'no override', 'lungs', 'lungs', 'no override', 'no override', 'central cube', 'central cube',
                'central cube', 'central cube', 'central cube'],
    strings.collimator : ['0', '-', '-', '-', '0', '*0', '*0', '*0', '-', '-', '-', '-', '-', '-', '-', '-', '-'],
    strings.gantry: ['0', '270,0,90', '90', '90', '0', '150,60,0,300,210', '150,60,0,300,210', '150,60,0,300,210', '-',
            '-', '-', '-', '-', '-', '-', '-', '-'],
    strings.SSD : ['100', '86,93,86', '86', '86', '93', '?,89,93,89,?', '?,89,93,89,?', '?,89,93,89,?', '90', '-', '-',
            '-', '-', '-', '-', '-', '-'],
    strings.couch : ['-', '-', '-', '-', '-', 'couch?', 'couch?', 'couch?', '-', 'couch?', 'couch?', 'couch?', '-', '-',
            'couch?', 'couch?', 'couch?'],
    strings.field_size : ['10x10', '10x6,10x12,10x6', '10x12', '10x12', '-', '-', '-', '-', '3x3,2x2,1x1', '-', '-', '-',
                '3x3', '1.5x1.5', '-', '-', '-'],
    strings.wedge : ['no wedge', '30,no wedge,30', 'no wedge', '60', 'no wedge', 'no wedge', 'no wedge', 'no wedge', 'no wedge', 'no wedge', 'no wedge', 'no wedge', 'no wedge', 'no wedge', 'no wedge', 'no wedge', 'no wedge'],
    strings.meas : ["'1','3','10','-','-','-','-','-','-'",
            "'5_RLAT','8_RLAT','5_AP','8_AP','5_LLAT','8_LLAT','-','-','-'", "'3','5','-','-','-','-','-','-','-'",
            "'3','5','-','-','-','-','-','-','-'", "'11','12','13','14','15','18','19','20','21'",
            "'11','12','13','14','15','16','17','-','-'", "'11','12','13','14','15','16','17','-','-'",
            "'11','12','13','14','15','17','18','-','-'",
            "'SoftTiss_3','SoftTiss_2','SoftTiss_1','-','-','-','-','-','-'",
            "'SoftTiss','-','-','-','-','-','-','-','-'", "'Spine2Inf','Spine1Sup','Cord','-','-','-','-','-','-'",
            "'Lung','-','-','-','-','-','-','-','-'", "'1_3','4_3','-','-','-','-','-','-','-'",
            "'1_1.5','4_1.5','-','-','-','-','-','-','-'", "'1','3','-','-','-','-','-','-','-'",
            "'1','3','-','-','-','-','-','-','-'", "'1','2','3','-','-','-','-','-','-'"],
    strings.energy : ["6,6FFF,10,10FFF,18", "6,6FFF,10,10FFF,18", "6,6FFF,10,10FFF,18", "6,6FFF,10,10FFF,18",
            "6,6FFF,10,10FFF,18", "6,6FFF,10,10FFF,18", "6,6FFF,10,10FFF,18", "6,6FFF,10,10FFF,18",
            "6,6FFF,10,10FFF,18", "6,6FFF,10,10FFF,18", "6,6FFF,10,10FFF,18", "6,6FFF,10,10FFF,18",
            "6,6FFF,10,10FFF,18", "6,6FFF,10,10FFF,18", "6,6FFF,10,10FFF,18", "6,6FFF,10,10FFF,18",
            "6,6FFF,10,10FFF,18"]}

class TestEvaluation(unittest.TestCase): 
    ''' Tests for verifying that parameter sets are passed correctly
    Each case (from 1-17) of the truth table has its own test against a set of parameters that *should* pass.
    It's currently infeasible to test every possible combination of pass/failure values, this is just a basic check. 
    Also, the correct answers are derived from the truth table. 

    Note that values of '-' are used for parameters where any value should be accepted.
    Note that modalities are IMRT for all cases; TODO check if that's ok.
    '''
    @classmethod
    def setUpClass(self): 
        # If all parameters pass, evaluate_parameters() should return this.
        # We'll use this to compare with the actual results in our tests below
        self.pass_evaluation = {
            strings.mode_req : strings.PASS,
            strings.prescription_dose_slash_fractions : strings.PASS,
            strings.prescription_point : strings.PASS,
            strings.isocenter_point : strings.PASS,
            strings.override : strings.PASS,
            strings.collimator : strings.PASS,
            strings.gantry : strings.PASS,
            strings.SSD : strings.PASS,
            strings.couch : strings.PASS,
            strings.field_size : strings.PASS,
            strings.wedge : strings.PASS,
            strings.meas : strings.PASS,
            strings.energy : strings.PASS
        }

    def test_case_1(self): 
        case = 1
        passing_parameters = {
            strings.mode_req : 'False',
            strings.prescription_dose_slash_fractions : '2/-/-',
            strings.prescription_point : '1 or 3',
                #TODO Think this should work for either 1 or 3, not the string "1 or 3"? 
            strings.isocenter_point : 'surf',
            strings.override : 'bone',
            strings.collimator : '0',
            strings.gantry : '0',
            strings.SSD : [100],
            strings.couch : '-',
            strings.field_size : '10x10',
            strings.wedge : 'no wedge',
            strings.meas : "'1','3','10','-','-','-','-','-','-'",
            strings.energy : "6"
        }
        treatment_type = 'not VMAT'

        self.assertEqual(evaluate_parameters(passing_parameters, truth_table, case, treatment_type), self.pass_evaluation)

    def test_case_2(self): 
        case = 2
        passing_parameters = {
            strings.mode_req : 'False',
            strings.prescription_dose_slash_fractions : '2/-/-',
            strings.prescription_point : '5',
            strings.isocenter_point : '3',
            strings.override : 'no override',
            strings.collimator : '-',
            strings.gantry : '270,0,90',
            strings.SSD : [86,93,86],
            strings.couch : '-',
            strings.field_size : '10x6,10x12,10x6',
            strings.wedge : '30,no wedge,30',
            strings.meas : "'5_RLAT','8_RLAT','5_AP','8_AP','5_LLAT','8_LLAT','-','-','-'",
            strings.energy : "6"
        }
        treatment_type = 'not VMAT'
        self.assertEqual(evaluate_parameters(passing_parameters, truth_table, case, treatment_type), self.pass_evaluation)

    def test_case_3(self): 
        case = 3
        passing_parameters = {
            strings.mode_req : 'False',
            strings.prescription_dose_slash_fractions : '2/-/-',
            strings.prescription_point : '3',
            strings.isocenter_point : '3',
            strings.override : 'no override',
            strings.collimator : '-',
            strings.gantry : '90',
            strings.SSD : [86],
            strings.couch : '-',
            strings.field_size : '10x12',
            strings.wedge : 'no wedge',
            strings.meas : "'3','5','-','-','-','-','-','-','-'",
            strings.energy : "6"
        }
        treatment_type = 'not VMAT'
        self.assertEqual(evaluate_parameters(passing_parameters, truth_table, case, treatment_type), self.pass_evaluation)

    def test_case_4(self): 
        case = 4
        passing_parameters = {
            strings.mode_req : 'False',
            strings.prescription_dose_slash_fractions : '2/-/-',
            strings.prescription_point : '3',
            strings.isocenter_point : '3',
            strings.override : 'no override',
            strings.collimator : '-',
            strings.gantry : '90',
            strings.SSD : [86],
            strings.couch : '-',
            strings.field_size : '10x12',
            strings.wedge : '60',
            strings.meas : "'3','5','-','-','-','-','-','-','-'",
            strings.energy : "6"
        }
        treatment_type = 'not VMAT'
        self.assertEqual(evaluate_parameters(passing_parameters, truth_table, case, treatment_type), self.pass_evaluation)
        
    def test_case_5(self): 
        case = 5
        passing_parameters = {
            strings.mode_req : 'False',
            strings.prescription_dose_slash_fractions : '50/25/-',
            strings.prescription_point : 'chair',
            strings.isocenter_point : '3',
            strings.override : 'no override',
            strings.collimator : '0',
            strings.gantry : '0',
            strings.SSD : [93],
            strings.couch : '-',
            strings.field_size : '-',
            strings.wedge : '-',
            strings.meas : "'11','12','13','14','15','18','19','20','21'",
            strings.energy : "6"
        }
        treatment_type = 'not VMAT'
        self.assertEqual(evaluate_parameters(passing_parameters, truth_table, case, treatment_type), self.pass_evaluation)

    def test_case_6(self): 
        case = 6
        passing_parameters = {
            strings.mode_req : 'True',
            strings.prescription_dose_slash_fractions : '50/25/-',
            strings.prescription_point : 'CShape',
            strings.isocenter_point : '3',
            strings.override : 'lungs',
            strings.collimator : '1',
            strings.gantry : '150,60,0,300,210',
            strings.SSD : ['-',89,93,89,'-'],
            strings.couch : 'couch?',
            strings.field_size : '-',
            strings.wedge : '-',
            strings.meas : "'11','12','13','14','15','16','17','-','-'",
            strings.energy : "6"
        }
        treatment_type = 'not VMAT'
        self.assertEqual(evaluate_parameters(passing_parameters, truth_table, case, treatment_type), self.pass_evaluation)

    def test_case_7(self): 
        case = 7
        passing_parameters = {
            strings.mode_req : 'True',
            strings.prescription_dose_slash_fractions : '50/25/-',
            strings.prescription_point : 'CShape',
            strings.isocenter_point : '3',
            strings.override : 'no override',
            strings.collimator : '1',
            strings.gantry : '150,60,0,300,210',
            strings.SSD : ['-',89,93,89,'-'],
            strings.couch : 'couch?',
            strings.field_size : '-',
            strings.wedge : '-',
            strings.meas : "'11','12','13','14','15','16','17','-','-'",
            strings.energy : "6"
        }
        treatment_type = 'not VMAT'
        self.assertEqual(evaluate_parameters(passing_parameters, truth_table, case, treatment_type), self.pass_evaluation)

    def test_case_8(self): 
        case = 8
        passing_parameters = {
            strings.mode_req : 'True',
            strings.prescription_dose_slash_fractions : '50/25/-',
            strings.prescription_point : 'C8Target',
            strings.isocenter_point : '3',
            strings.override : 'no override',
            strings.collimator : '1',
            strings.gantry : '150,60,0,300,210',
            strings.SSD : ['-',89,93,89,'-'],
            strings.couch : 'couch?',
            strings.field_size : '-',
            strings.wedge : '-',
            strings.meas : "'11','12','13','14','15','17','18','-','-'",
            strings.energy : "6"
        }
        treatment_type = 'not VMAT'
        self.assertEqual(evaluate_parameters(passing_parameters, truth_table, case, treatment_type), self.pass_evaluation)

    def test_case_9(self): 
        case = 9
        passing_parameters = {
            strings.mode_req : 'False',
            strings.prescription_dose_slash_fractions : '900/3/MU',
            strings.prescription_point : 'C8Target',
            strings.isocenter_point : 'SoftTiss',
            strings.override : 'lungs',
            strings.collimator : '-',
            strings.gantry : '-',
            strings.SSD : [90],
            strings.couch : '-',
            strings.field_size : '3x3,2x2,1x1',
            strings.wedge : '-',
            strings.meas : "'SoftTiss_3','SoftTiss_2','SoftTiss_1','-','-','-','-','-','-'",
            strings.energy : "6"
        }
        treatment_type = 'not VMAT'
        self.assertEqual(evaluate_parameters(passing_parameters, truth_table, case, treatment_type), self.pass_evaluation)

    def test_case_10(self): 
        case = 10
        passing_parameters = {
            strings.mode_req : 'True',
            strings.prescription_dose_slash_fractions : '45/3/-',
            strings.prescription_point : 'SoftTissTarget',
            strings.isocenter_point : 'SoftTiss',
            strings.override : 'lungs',
            strings.collimator : '-',
            strings.gantry : '-',
            strings.SSD : '-',
            strings.couch : 'couch?',
            strings.field_size : '-',
            strings.wedge : '-',
            strings.meas : "'SoftTiss','-','-','-','-','-','-','-','-'",
            strings.energy : "6"
        }
        treatment_type = 'not VMAT'
        self.assertEqual(evaluate_parameters(passing_parameters, truth_table, case, treatment_type), self.pass_evaluation)


    def test_case_11(self): 
        case = 11
        passing_parameters = {
            strings.mode_req : 'True',
            strings.prescription_dose_slash_fractions : '24/2/-',
            strings.prescription_point : 'SpineTarget',
            strings.isocenter_point : 'Spine',
            strings.override : 'no override',
            strings.collimator : '-',
            strings.gantry : '-',
            strings.SSD : '-',
            strings.couch : 'couch?',
            strings.field_size : '-',
            strings.wedge : '-',
            strings.meas : "'Spine2Inf','Spine1Sup','Cord','-','-','-','-','-','-'",
            strings.energy : "6"
        }
        treatment_type = 'not VMAT'
        self.assertEqual(evaluate_parameters(passing_parameters, truth_table, case, treatment_type), self.pass_evaluation)

    def test_case_12(self): 
        case = 12
        passing_parameters = {
            strings.mode_req : 'True',
            strings.prescription_dose_slash_fractions : '48/4/-',
            strings.prescription_point : 'LungTarget',
            strings.isocenter_point : 'Lung',
            strings.override : 'no override',
            strings.collimator : '-',
            strings.gantry : '-',
            strings.SSD : '-',
            strings.couch : 'couch?',
            strings.field_size : '-',
            strings.wedge : '-',
            strings.meas : "'Lung','-','-','-','-','-','-','-','-'",
            strings.energy : "6"
        }
        treatment_type = 'not VMAT'
        self.assertEqual(evaluate_parameters(passing_parameters, truth_table, case, treatment_type), self.pass_evaluation)

    def test_case_13(self): 
        case = 13
        passing_parameters = {
            strings.mode_req : 'True',
            strings.prescription_dose_slash_fractions : '3/-/-',
            strings.prescription_point : '1',
            strings.isocenter_point : '1',
            strings.override : 'central cube',
            strings.collimator : '-',
            strings.gantry : '-',
            strings.SSD : '-',
            strings.couch : '-',
            strings.field_size : '3x3',
            strings.wedge : '-',
            strings.meas : "'1_3','4_3','-','-','-','-','-','-','-'",
            strings.energy : "6"
        }
        treatment_type = 'not VMAT'
        self.assertEqual(evaluate_parameters(passing_parameters, truth_table, case, treatment_type), self.pass_evaluation)


    def test_case_14(self): 
        case = 14
        passing_parameters = {
            strings.mode_req : 'True',
            strings.prescription_dose_slash_fractions : '3/-/-',
            strings.prescription_point : '1',
            strings.isocenter_point : '1',
            strings.override : 'central cube',
            strings.collimator : '-',
            strings.gantry : '-',
            strings.SSD : '-',
            strings.couch : '-',
            strings.field_size : '1.5x1.5',
            strings.wedge : '-',
            strings.meas : "'1_1.5','4_1.5','-','-','-','-','-','-','-'",
            strings.energy : "6"
        }
        treatment_type = 'not VMAT'
        self.assertEqual(evaluate_parameters(passing_parameters, truth_table, case, treatment_type), self.pass_evaluation)


    def test_case_15(self): 
        case = 15
        passing_parameters = {
            strings.mode_req : 'True',
            strings.prescription_dose_slash_fractions : '20/-/-',
            strings.prescription_point : 'PTV_c14_c15',
            strings.isocenter_point : '1',
            strings.override : 'central cube',
            strings.collimator : '-',
            strings.gantry : '-',
            strings.SSD : '-',
            strings.couch : 'couch?',
            strings.field_size : '-',
            strings.wedge : '-',
            strings.meas : "'1','3','-','-','-','-','-','-','-'",
            strings.energy : "6"
        }
        treatment_type = 'not VMAT'
        self.assertEqual(evaluate_parameters(passing_parameters, truth_table, case, treatment_type), self.pass_evaluation)

    def test_case_16(self): 
        case = 16
        passing_parameters = {
            strings.mode_req : 'True',
            strings.prescription_dose_slash_fractions : '20/-/-',
            strings.prescription_point : '-',
            strings.isocenter_point : '-',
            strings.override : 'central cube',
            strings.collimator : '-',
            strings.gantry : '-',
            strings.SSD : '-',
            strings.couch : 'couch?',
            strings.field_size : '-',
            strings.wedge : '-',
            strings.meas : "'1','3','-','-','-','-','-','-','-'",
            strings.energy : "6"
        }
        treatment_type = 'not VMAT'
        self.assertEqual(evaluate_parameters(passing_parameters, truth_table, case, treatment_type), self.pass_evaluation)

    def test_case_17(self): 
        case = 17
        passing_parameters = {
            strings.mode_req : 'True',
            strings.prescription_dose_slash_fractions : '20/-/-',
            strings.prescription_point : '-',
            strings.isocenter_point : '-',
            strings.override : 'central cube',
            strings.collimator : '-',
            strings.gantry : '-',
            strings.SSD : '-',
            strings.couch : 'couch?',
            strings.field_size : '-',
            strings.wedge : '-',
            strings.meas : "'1','2','3','-','-','-','-','-','-'",
            strings.energy : "6"
        }
        treatment_type = 'not VMAT'
        self.assertEqual(evaluate_parameters(passing_parameters, truth_table, case, treatment_type), self.pass_evaluation)

if __name__ == '__main__' : 
    unittest.main()


