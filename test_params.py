''' Tests for parameters extracted

This module contains a number of tests using python's unittest library.
See https://docs.python.org/3/library/unittest.html for more information about unittest.

The tests are to run on 2 sample datasets; IMRT and VMAT; which are included in the Documents subdirectory.
The correct values for each test are derived from the corresponding pdf reports in each of IMRT and VMAT directories.

Basic method to run these tests: `python -m unittest`
Detailed instructions for running tests are in the README. 
'''
import unittest
import pydicom
from parameter_retrieval import extract_parameters, evaluate_parameters

class TestIMRTExtractionEvaluation(unittest.TestCase):
    ''' Tests for verifying that parameters are passed and failed correctly
    The 'correct' answers are derived from the Elekta Monaco pdf report in conjunction with the given truth table
    '''
    @classmethod
    def setUpClass(self):
        # We do some set up that is useful across tests in this class 
        # i.e. running the extraction function once and using the result for each test differently
        self.dummy_parameters = None

    def test_total_prescription_dose(self):
        pass
    
    def test_number_of_fractions(self):
        pass

    def test_collimator(self):
        pass

    def test_gantry_angle(self):
        pass

    def test_ssd(self):
        pass

    def test_number_of_wedges(self):
        pass


class TestIMRTExtractionValues(unittest.TestCase):
    ''' Tests for verifying the correct values are extracted
    The 'correct' answers are derived from the Elekta Monaco pdf report
    '''
    @classmethod
    def setUpClass(self):
        # We do some set up that is useful across tests in this class 
        # i.e. running the extraction function once and using the result for each test differently
        self.extracted = extract_parameters('./Documents/Input/YellowLvlIII_7a.dcm', 6)

    def test_total_prescription_dose(self):
        # self.assertEqual(50, self.extracted...)
        pass
    
    def test_number_of_fractions(self):
        # self.assertEqual(25, self.extracted...)
        pass

    def test_collimator(self):
        # self.assertEqual(0, self.extracted...)
        pass

    def test_gantry_angle(self):
        # TODO update the format of the tuple according to the output of our function
        # self.assertEqual((150,60,0,300,210), self.extracted...)
        pass

    def test_ssd(self):
        # intended for None == any value accepted here, and the numbered test have a slack of +-1
        # self.assertEqual((79.07,89.46,92.63,89.75,79.36), self.extracted...)
        pass

    def test_number_of_wedges(self):
        # do we mean wedge angle?
        pass


class TestVMRTExtractionEvaluation(unittest.TestCase):
    ''' Tests for verifying that parameters are passed and failed correctly
    The 'correct' answers are derived from the Elekta Monaco pdf report in conjunction with the given truth table
    '''
    @classmethod
    def setUpClass(self):
        # We do some set up that is useful across tests in this class 
        # i.e. running the extraction function once and using the result for each test differently

        #TODO put the VMRT file into documents 
        # self.extracted = extract_parameters('./Documents/Input/YellowLvlIII_7a.dcm', 6)
        # print(self.extracted)
        pass

    def test_total_prescription_dose(self):
        pass
    
    def test_number_of_fractions(self):
        pass

    def test_collimator(self):
        pass

    def test_gantry_angle(self):
        pass

    def test_ssd(self):
        pass

    def test_number_of_wedges(self):
        pass


class TestVMRTExtractionValues(unittest.TestCase):
    ''' Tests for verifying the correct values are extracted
    The 'correct' answers are derived from the Elekta Monaco pdf report
    '''
    @classmethod
    def setUpClass(self):
        # We do some set up that is useful across tests in this class 
        # i.e. running the extraction function once and using the result for each test differently
        
        #TODO put the VMRT file into documents 
        # self.extracted = extract_parameters('./Documents/Input/YellowLvlIII_7a.dcm', 6)
        # print(self.extracted)
        pass

    def test_total_prescription_dose(self):
        pass
    
    def test_number_of_fractions(self):
        pass

    def test_collimator(self):
        pass

    def test_gantry_angle(self):
        pass

    def test_ssd(self):
        pass

    def test_number_of_wedges(self):
        # do we mean wedge angle?
        pass

if __name__ == '__main__':
    unittest.main()


