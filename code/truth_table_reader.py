''' Parse the truth table from a csv input into a python dictionary'''

import pandas as pd
from pathlib import Path
import csv

def read_truth_table(truth_table_file):
    tt = pd.read_csv(truth_table_file, dtype='str')
    return tt.to_dict('list')
    
if __name__ == "__main__":
    tt = read_truth_table("data/truth_table_lvl3.csv")
    print(tt)




