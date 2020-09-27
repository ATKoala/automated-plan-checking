# automated-plan-checking

This repository contains code for extracting and evaluating parameters from radiology treatment plans (in the form of DICOM files).

## Getting started

### Dependencies

- **Python 3** or above
- **pydicom** (can be installed with `pip install pydicom`)

### Installation and Usage

`git clone [URL]`, then
`python PROGRAM_NAME.py -i DICOM_FILE`

Examples:
    python command_line.py -i "YellowLvlIII_7a.dcm" -c 6 -o "D:\COMP90082\automated-plan-checking\Documents\Output\Result.csv" -f "csv"(if in same folder, -c means case 6)
    python command_line.py -i "C://Users/User/YellowLvlIII_7a.dcm"(if in another folder)

## Testing

Test code is in `test_params.py`. There are currently 3 classes; *TestEvaluation* is a collection of
tests of the parameter evaluation: given a set of parameters, it verifies that the pass/fail results are as expected.
*TestIMRTExtractionValues* is a collection of tests verifying that the correct values are extracted from IMRT file (YellowLvlIII_7a.dcm)
*TestVMATExtractionValues* is a collection of tests verifying that the correct values are extracted from VMAT file (YellowLvlIII_7b.dcm)

- Run the tests with `python -m unittest`
- Run tests for a particular class with `python -m unittest test_params.ClassName` e.g `python -m unittest test_params.TestIMRTExtractionValues` or `python -m unittest test_params.TestEvaluation`
- Run a particular test (i.e prescription dose) with `python -m unittest test_params.ClassName.FunctionName` e.g. `python -m unittest test_params.TestIMRTExtractionValues.test_total_prescription_dose`
