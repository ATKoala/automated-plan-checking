''' Test that the truth table reader function parses the csv input correctly'''

import unittest
from code.truth_table_reader import read_truth_table

class TestTruthTableReader(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        self.truth_table = {
            "case": ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17'],
            "mode req": ['False', 'False', 'False', 'False', 'False', 'True', 'True', 'True', 'False', 'True', 'True',
                        'True', 'True', 'True', 'True', 'True', 'True'],
            "prescription dose/#": ['2/-/-', '2/-/-', '2/-/-', '2/-/-', '50/25/-', '50/25/-', '50/25/-', '50/25/-', '900/3/MU', '45/3/-', '24/2/-',
                                    '48/4/-', '3/-/-', '3/-/-', '20/-/-', '20/-/-', '20/-/-'],
            "prescription point": ['1 or 3', '5', '3', '3', 'chair', 'CShape', 'CShape', 'C8Target', '-', 'SoftTissTarget',
                                'SpineTarget', 'LungTarget', '1', '1', 'PTV_c14_c15', '-', '-'],
            "isocentre point": ['surf', '3', '3', '3', '3', '3', '3', '3', 'SoftTiss', 'SoftTiss', 'Spine', 'Lung', '1',
                                '1', '1', '-', '-'],
            "override": ['bone', 'no override', 'no override', 'no override', 'no override', 'lungs', 'no override',
                        'no override', 'lungs', 'lungs', 'no override', 'no override', 'central cube', 'central cube',
                        'central cube', 'central cube', 'central cube'],
            "collimator": ['0', '-', '-', '-', '0', '*0', '*0', '*0', '-', '-', '-', '-', '-', '-', '-', '-', '-'],
            "gantry": ['0', '270,0,90', '90', '90', '0', '150,60,0,300,210', '150,60,0,300,210', '150,60,0,300,210', '-',
                    '-', '-', '-', '-', '-', '-', '-', '-'],
            "SSD": ['100', '86,93,86', '86', '86', '93', '?,89,93,89,?', '?,89,93,89,?', '?,89,93,89,?', '90', '-', '-',
                    '-', '-', '-', '-', '-', '-'],
            'couch': ['-', '-', '-', '-', '-', 'couch?', 'couch?', 'couch?', '-', 'couch?', 'couch?', 'couch?', '-', '-',
                    'couch?', 'couch?', 'couch?'],
            'field size': ['10x10', '10x6,10x12,10x6', '10x12', '10x12', '-', '-', '-', '-', '3x3,2x2,1x1', '-', '-', '-',
                        '3x3', '1.5x1.5', '-', '-', '-'],
            'wedge': ['no wedge', '30,no wedge,30', 'no wedge', '60', 'no wedge', 'no wedge', 'no wedge', 'no wedge', 'no wedge', 'no wedge', 'no wedge', 'no wedge', 'no wedge', 'no wedge', 'no wedge', 'no wedge', 'no wedge'],
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
                    "6,6FFF,10,10FFF,18"]
        }
                    
    def test_read_tt_csv(self):
        tt = read_truth_table('tests/resources/truth_table_test.csv')
        for parameter in self.truth_table:
            for i in range(0, len(self.truth_table['case'])):
                self.assertEqual(tt[parameter][i].upper(), self.truth_table[parameter][i].upper())
