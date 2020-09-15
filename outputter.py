"""Collection of functions to output the extracted parameters into the format specified by the user"""

import pandas as pd

def output_csv(Result, name):
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
    test_pd.to_csv('Documents/Output/Result.csv', encoding='utf-8', index=False)


def output_stdout(parameters, name):
    print("The number of beams: " + str(parameters["Number of Beams"]))
    for beam in parameters["Beams"]:
        for p in beam:
            print(p + " : " + str(beam[p]))
        print("\n")


formatter = {
    'csv': output_csv,
    'stdout': output_stdout
}


def output(parameters, name, format):
    formatter_function = formatter[format]
    formatter_function(parameters, name)
