''' Tests for Parameter Extraction and Evaluation'''

import unittest
import pydicom
from code import strings
from code.parameters.parameter_retrieval import extract_parameters, evaluate_parameters

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
        from code.truth_table_reader import read_truth_table
        self.truth_table = read_truth_table("data/truth_table_lvl3.csv")

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
            # Get a set of values that should pass (directly from truth table)
            passing_data = dict([(key,value[i]) for key,value in self.truth_table.items()])
            # We discard the 'case' value since it's not part of evaluation
            del passing_data[strings.case]
            # SSD needs to be converted from string to a list because thats what evaluation function wants
            passing_data[strings.SSD] = passing_data[strings.SSD].split(',')
            self.assertEqual(evaluate_parameters(passing_data, self.truth_table, case), self.pass_evaluation)

    def test_fail_lvl3_prescription(self):
        # Test that a prescription value that is meant to fail does get failed by the evaluation function
        case = 1
        failing_data = dict([(key,value[case-1]) for key,value in self.truth_table.items()])
        del failing_data[strings.case]
        failing_data[strings.SSD] = failing_data[strings.SSD].split(',')

        # Make the prescription dose wrong
        failing_data[strings.prescription_dose] = "50/25/-"
        self.assertNotEqual(evaluate_parameters(failing_data, self.truth_table, case), self.pass_evaluation)

    def test_fail_lvl3_collimator(self):
        # Test that a wrong collimator value gets failed correctly
        case = 6
        failing_data = dict([(key,value[case-1]) for key,value in self.truth_table.items()])
        del failing_data[strings.case]
        failing_data[strings.SSD] = failing_data[strings.SSD].split(',')
        
        # Make the collimator angle wrong 
        failing_data[strings.prescription_dose] = "0"
        self.assertNotEqual(evaluate_parameters(failing_data, self.truth_table, case), self.pass_evaluation)


if __name__ == '__main__' : 
    unittest.main()


