'''Collection of functions to output the extracted parameters into the format specified by the user'''

import pandas as pd

def output_csv(data, filepath):
    headers = ["Parameter Name", "Parameter Value", "Parameter Evaluation", "Parameter Solution"]
    allValues = []

    for item in data[0]:
        Value = [item] + [column[item] for column in data]
        allValues.append(Value)

    test_pd = pd.DataFrame(columns=headers, data=allValues)

    filepath = filepath + ".csv" if not filepath.endswith(".csv") else filepath
    test_pd.to_csv(filepath, encoding='utf-8', index=False)
    return filepath

def output_stdout(data, filepath):
    for key in data[0]:
        print(key + ": " + " || ".join([str(column[key]) for column in data]))

formatter = {
    'csv': output_csv,
    'stdout': output_stdout
}

def output(parameters, evaluations, solutions, filepath, format):
    formatter_function = formatter[format]
    return formatter_function((parameters, evaluations, solutions), filepath)