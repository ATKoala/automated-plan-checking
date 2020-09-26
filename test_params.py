''' Tests for parameters extracted

This module contains a number of tests using python's unittest library.
See https://docs.python.org/3/library/unittest.html for more information about unittest.

The tests are run on 2 sample datasets; IMRT and VMAT; which are included in the Documents subdirectory.
The correct values for each test are derived from the corresponding pdf reports in each of IMRT and VMAT directories.

Basic method to run these tests: `python -m unittest`
Detailed instructions for running tests are in the README. 
'''
import unittest
import pydicom
from parameter_retrieval import extract_parameters

class TestExtractionEvaluation(unittest.TestCase):
    ''' Tests for verifying that parameters are passed and failed correctly
    '''
    @classmethod
    def setUpClass(self):
        # We do some set up that is useful across tests in this class 
        # i.e. running the extraction function once and using the result for each test differently
        self.extracted = extract_parameters('./Documents/Input/YellowLvlIII_7a.dcm', 6)
        print(self.extracted)
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


class TestExtractionValues(unittest.TestCase):
    ''' Tests for verifying the correct values are extracted
    '''
    @classmethod
    def setUpClass(self):
        # We do some set up that is useful across tests in this class 
        # i.e. running the extraction function once and using the result for each test differently
        self.extracted = extract_parameters('./Documents/Input/YellowLvlIII_7a.dcm', 6)

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

if __name__ == '__main__':
    unittest.main()


