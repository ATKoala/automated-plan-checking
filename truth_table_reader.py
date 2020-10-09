import pandas as pd
from pathlib import Path

def read_truth_table(truth_table_file):
    if Path(truth_table_file).suffix == '.csv':
        return read_truth_table_csv(truth_table_file)
    # placeholder for other possible truth table input types
    else:
        return False
    
def read_truth_table_csv(truth_table_file):
    tt = pd.read_csv(truth_table_file, dtype='str')
    return tt.to_dict('list')
                
#just for testing
if __name__ == "__main__":
    tt = read_truth_table("truth_table_example.csv")
    print(tt)