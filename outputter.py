"""Collection of functions to output the extracted parameters into the format specified by the user"""
import pandas as pd

def output_csv(Result, filepath):
    title = ["Beam Id"]
    allValues = []
    for colomn_name in Result["Beams"][0]:
        title.append(colomn_name)

    i = 0
    while i + 1 < Result["Number of Beams"]:
        value = [i + 1]
        tempdic = Result["Beams"][i]
        for item in tempdic:
            value.append(tempdic[item])

        allValues.append(value)
        i += 1

    test_pd = pd.DataFrame(columns=title, data=allValues)

    filepath = filepath + ".csv" if not filepath.endswith(".csv") else filepath
    test_pd.to_csv(filepath, encoding='utf-8', index=False)
    return filepath


def output_stdout(parameters, filepath):
    for item in parameters:
        print(item + ": " + parameters[item])
    '''print("The number of beams: " + str(parameters["Number of Beams"]))
    for beam in parameters["Beams"]:
        for p in beam:
            print(p + " : " + str(beam[p]))
        print("\n")
    '''


def update_output_csv(data, filepath):
    title = ["Parameter Name", "Parameter Value", "Parameter Evaluation", "Parameter Solution"]
    allValues = []

    for item in data[0]:
        Value = [item] + [col[item] for col in data]
        allValues.append(Value)

    test_pd = pd.DataFrame(columns=title, data=allValues)

    filepath = filepath + ".csv" if not filepath.endswith(".csv") else filepath
    test_pd.to_csv(filepath, encoding='utf-8', index=False)
    return filepath


def update_output_stdout(data, filepath):
    for key in data[0]:
        print(key + ": " + " || ".join([str(column[key]) for column in data]))


formatter = {
    'csv': update_output_csv,
    'stdout': update_output_stdout
    # 'csv': output_csv,
    # 'stdout': output_stdout
}


def output(parameters, evaluations, solutions, filepath, format):
    # for item in parameters:
    # print(item+": "+parameters[item])
    formatter_function = formatter[format]
    return formatter_function((parameters, evaluations, solutions), filepath)