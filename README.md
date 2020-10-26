# automated-plan-checking

This repository contains code for extracting and evaluating parameters from radiology treatment plans (in the form of DICOM files).

## Table of Contents

1. Background
2. Table of Contents
3. System Requirements
4. Installation and Usage
5. Running tests
6. Features
7. Documetation Overview
8. Changelog

## System Requirements

- **Python 3** or above
- **pydicom** (can be installed with `pip install pydicom`)
- **pandas** ((can be installed with `pip install pandas`))

## Installation and Usage

To install with git: `git clone https://github.com/SuryadiTjandra/automated-plan-checking.git`
To download as zip: <https://github.com/SuryadiTjandra/automated-plan-checking/archive/master.zip>

Usage Examples:

- `python app.py --inputs Resources/Input --format csv` <- Process all dicoms in folder, with case number prompt for each dicom found
- `python app.py --inputs Resources/Input --format csv --case_number 6` <- Process all dicoms in folder, treating each as a case 6
- `python app.py --inputs Resources/Input OTHER_DICOM_FOLDER --format csv --case_number 6` <- Process all dicoms in both folders, treating all dicoms found as case 6
- `python app.py --inputs Resources/Input/YellowLvlIII_7a.dcm Resources/Input/YellowLvlIII_7b.dcm --format csv` <- Process any number of separate dicoms, with case number prompts for each
- `python app.py --inputs Resources/Input/YellowLvlIII_7a.dcm,1 Resources/Input/YellowLvlIII_7b.dcm,2 --format csv` <- Process any number of separate dicoms, giving case numbers for each (format: dicom,case, dicom2,case ... etc).
- `python app.py --inputs Resources/Input,1 OTHER_DICOM_FOLDER,2 --format csv` <- Process any number of folders, giving case numbers for each (format: folder,case, folder2,case ... etc).
- `python app.py --inputs Resources/Input --format csv --truth_table truth_table_example.csv` <- Use the file ``truth_table_example.csv`` as input for the truth table that will be used to evaluate extracted parameters

## Running Tests

Run the tests with `python -m unittest`

Run tests for a particular class with `python -m unittest test_parameter_retrieval.ClassName`

e.g `python -m unittest test_parameter_retrieval.TestIMRTExtractionValues`

Run a particular test (i.e prescription dose) with `python -m unittest test_parameter_retrieval.ClassName.FunctionName`

e.g. `python -m unittest test_parameter_retrieval.TestIMRTExtractionValues.test_total_prescription_dose`

## Features

Copy completed user stories here

## Documentation Overview

Full project documentation generated from a Confluence space can be found in docs/

It contains the project bacground in more depth as well as ...

## Changelog

...
