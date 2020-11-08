'''Collection of functions to output the extracted parameters into the format specified by the user'''

import pandas as pd
from code_files import strings

def output(parameters, evaluations, solutions, filepath):
    headers = ["Parameter Name", "Parameter Value", "Parameter Evaluation", "Parameter Solution"]
    allValues = []

    for item in strings.parameters:
        Value = [item] + [column[item] for column in (parameters, evaluations, solutions)]
        allValues.append(Value)

    test_pd = pd.DataFrame(columns=headers, data=allValues)

    filepath = filepath + ".csv" if not filepath.endswith(".csv") else filepath
    test_pd.to_csv(filepath, encoding='utf-8', index=False)
    return filepath