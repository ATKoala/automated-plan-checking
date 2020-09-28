# automated-plan-checking

This repository contains code for extracting and evaluating parameters from radiology treatment plans (in the form of DICOM files).

## Getting started

### Dependencies

- **Python 3** or above
- **pydicom** (can be installed with `pip install pydicom`)
- **pandas** ((can be installed with `pip install pandas`))

### Installation and Usage

To install: `git clone https://github.com/SuryadiTjandra/automated-plan-checking.git`

Usage Examples:
    `python app.py -i "YellowLvlIII_7a.dcm" -c 6 -o "D:\COMP90082\automated-plan-checking\Documents\Output\Result.csv" -f "csv"`(if in same folder, -c means case 6)
    `python app.py -i "C://Users/User/YellowLvlIII_7a.dcm"`(if in another folder)

## Testing

Test code is in `test_parameter_retrieval.py`.

### Running Tests

Run the tests with `python -m unittest`

Run tests for a particular class with `python -m unittest test_parameter_retrieval.ClassName` 

e.g `python -m unittest test_parameter_retrieval.TestIMRTExtractionValues` 

or `python -m unittest test_parameter_retrieval.TestEvaluation`

Run a particular test (i.e prescription dose) with `python -m unittest test_parameter_retrieval.ClassName.FunctionName` 

e.g. `python -m unittest test_parameter_retrieval.TestIMRTExtractionValues.test_total_prescription_dose`

### Structure

There are 3 classes (aka test suites aka groupings of tests) in the file;

- *TestEvaluation* is a collection of tests of the parameter evaluation: given a set of parameters, it verifies that the pass/fail results are as expected.
- *TestIMRTExtractionValues* is a collection of tests verifying that the correct values are extracted from IMRT file (YellowLvlIII_7a.dcm)
- *TestVMATExtractionValues* is a collection of tests verifying that the correct values are extracted from VMAT file (YellowLvlIII_7b.dcm)
