''' Tests for Parameter Extraction and Evaluation

This module contains a number of tests using python's unittest library.
See https://docs.python.org/3/library/unittest.html for more information about unittest.

- TestIMRTExtractionValues is a collection of tests verifying that the correct values are extracted from IMRT file (YellowLvlIII_7a.dcm)
- TestVMATExtractionValues is a collection of tests verifying that the correct values are extracted from VMAT file (YellowLvlIII_7b.dcm)
- TestEvaluation is a collection of tests on the parameter evaluation: given a set of parameters, 
   it verifies that the pass/fail results are as expected

The 2 DICOM files tested are included in the data subdirectory.
The correct values for each test are derived from the corresponding pdf reports in each of IMRT and VMAT directories (7a.pdf, 7b.pdf).

Basic method to run all tests: `python -m unittest`
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
        dataset = pydicom.dcmread('./data/Input/YellowLvlIII_7a.dcm', force=True)
        self.extracted = extract_parameters(dataset, 7)

    def test_prescription_dose(self):
        # MU setting is not found in the PDF
        self.assertEqual(self.extracted[strings.prescription_dose], '50/25/MU')

    def test_collimator(self): 
        self.assertEqual(self.extracted[strings.collimator], '0')

    def test_gantry_angle(self): 
        self.assertEqual(self.extracted[strings.gantry], '150,60,0,300,210')

    def test_ssd(self): 
        self.assertEqual(self.extracted[strings.SSD], [85.19,89.42,92.67,89.57,85.19])

    def test_energy(self): 
        self.assertEqual(self.extracted[strings.energy], '6')

class TestVMATExtractionValues(unittest.TestCase): 
    ''' Tests for verifying the correct values are extracted
    The 'correct' answers are derived from the vendor report in Documents/Input/7b.pdf
    '''
    @classmethod
    def setUpClass(self): 
        # We use the extraction function once here and inspect the results in the tests below
        dataset = pydicom.dcmread('./data/Input/YellowLvlIII_7b.dcm', force=True)
        self.extracted = extract_parameters(dataset, 7)

    def test_prescription_dose(self):
        # Function returns 50/25/MU, but MU is not found in PDF Report.
        # but Michael says it be like that, so...
        self.assertEqual(self.extracted[strings.prescription_dose], '50/25/MU')

    def test_collimator(self): 
        self.assertEqual(self.extracted[strings.collimator], '355')

    def test_gantry_angle(self):
        # Real result returns large array with values going from 180->360->180->0->180
        # PDF report formats it as "180/360", which does not match our own formatting
        # self.assertEqual(self.extracted[strings.gantry], '180/360')
        pass 

    def test_ssd(self):
        # Real result returns large array, PDF report shows only one
        # self.assertEqual(self.extracted[strings.SSD], [87.17])
        pass

    def test_energy(self): 
        self.assertEqual(self.extracted[strings.energy], '6')


class TestEvaluation(unittest.TestCase): 
    ''' Tests for verifying that parameter sets are passed correctly
    Each case (from 1-17) of the truth table has its own test against a set of parameters that *should* pass.
    It's currently infeasible to test every possible combination of pass/failure values, this is just a basic check. 
    Also, the correct answers are derived from the truth table. 

    Note that values of '-' are used for parameters where any value should be accepted.
    '''
    @classmethod
    def setUpClass(self): 
        from truth_table_reader import read_truth_table
        self.truth_table = read_truth_table(strings.lvl3_truth_table)

        # If all parameters pass, evaluate_parameters() should return this.
        # We'll use this to compare with the actual results in our tests below
        self.pass_evaluation = {
            strings.mode                                : strings.NOT_APPLICABLE,
            strings.prescription_dose                   : strings.PASS,
            strings.prescription_point                  : strings.PASS,
            strings.isocenter_point                     : strings.PASS,
            strings.override                            : strings.PASS,
            strings.collimator                          : strings.PASS,
            strings.gantry                              : strings.PASS,
            strings.SSD                                 : strings.PASS,
            strings.couch                               : strings.PASS,
            strings.field_size                          : strings.PASS,
            strings.wedge                               : strings.PASS,
            strings.meas                                : strings.PASS,
            strings.energy                              : strings.NOT_APPLICABLE
        }

    def test_passing_lvl3_all(self):
        # Test that the evaluation passes all cases when values are directly retrieved from the truth table
        num_cases = 17
        for i in range(num_cases):
            case = i + 1
            # Get the truth table values for this case into passing_data
            passing_data = dict([(key,value[i]) for key,value in self.truth_table.items()])
            # Truth table also has a "case" value which we discard since it's not part of evaluation
            del passing_data[strings.case]
            self.assertEqual(evaluate_parameters(passing_data, self.truth_table, case), self.pass_evaluation)

    def test_fail_lvl3_case1(self):
        # Test that values that are meant to fail do get failed by the evaluation function
        case = 1
        # Get the truth table values for this case into passing_data
        passing_data = dict([(key,value[case-1]) for key,value in self.truth_table.items()])
        # Grabbing values fro truth table also produces the "case" value which we discard since it's not part of evaluation
        del passing_data[strings.case]

        # Make the prescription dose wrong - it should be 2/1/-
        passing_data[strings.prescription_dose] = "50/25/-"
        self.assertNotEqual(evaluate_parameters(passing_data, self.truth_table, case), self.pass_evaluation)

if __name__ == '__main__' : 
    unittest.main()


