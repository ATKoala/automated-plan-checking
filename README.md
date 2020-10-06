# automated-plan-checking

This repository contains code for extracting and evaluating parameters from radiology treatment plans (in the form of DICOM files).

## Getting started

### Dependencies

- **Python 3** or above
- **pydicom** (can be installed with `pip install pydicom`)
- **pandas** ((can be installed with `pip install pandas`))

### Installation and Usage

To install with git: `git clone https://github.com/SuryadiTjandra/automated-plan-checking.git`
To download as zip: <https://github.com/SuryadiTjandra/automated-plan-checking/archive/master.zip>

Usage Examples:

- `python app.py --inputs Resources/Input --format csv` <- Process all dicoms in folder, with case number prompt for each dicom found
- `python app.py --inputs Resources/Input --format csv --case_number 6` <- Process all dicoms in folder, treating each as a case 6
- `python app.py --inputs Resources/Input OTHER_DICOM_FOLDER --format csv --case_number 6` <- Process all dicoms in both folders, treating all dicoms found as case 6
- `python app.py --inputs Resources/Input/YellowLvlIII_7a.dcm Resources/Input/YellowLvlIII_7b.dcm --format csv` <- Process any number of separate dicoms, with case number prompts for each
- `python app.py --inputs Resources/Input/YellowLvlIII_7a.dcm,1 Resources/Input/YellowLvlIII_7b.dcm,2 --format csv` <- Process any number of separate dicoms, giving case numbers for each (format: dicom,case, dicom2,case ... etc).
- `python app.py --inputs Resources/Input,1 OTHER_DICOM_FOLDER,2 --format csv` <- Process any number of folders, giving case numbers for each (format: folder,case, folder2,case ... etc).

## Testing

Test code is in `test_parameter_retrieval.py`.

### Running Tests

Run the tests with `python -m unittest`

Run tests for a particular class with `python -m unittest test_parameter_retrieval.ClassName`

e.g `python -m unittest test_parameter_retrieval.TestIMRTExtractionValues`

Run a particular test (i.e prescription dose) with `python -m unittest test_parameter_retrieval.ClassName.FunctionName`

e.g. `python -m unittest test_parameter_retrieval.TestIMRTExtractionValues.test_total_prescription_dose`

### Structure

There are 3 classes (aka test suites aka groupings of tests) in the file;

- *TestEvaluation* is a collection of tests of the parameter evaluation: given a set of parameters, it verifies that the pass/fail results are as expected.
- *TestIMRTExtractionValues* is a collection of tests verifying that the correct values are extracted from IMRT file (YellowLvlIII_7a.dcm)
- *TestVMATExtractionValues* is a collection of tests verifying that the correct values are extracted from VMAT file (YellowLvlIII_7b.dcm)
