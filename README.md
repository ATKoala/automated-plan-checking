# automated-plan-checking

This repository contains code for extracting and evaluating parameters from radiology treatment plans (in the form of DICOM files).

## Table of Contents

- [Background](#automated-plan-checking)
- [Table of Contents](#Table-of-Contents)
- [System Requirements](#System-Requirements)
- [Installation and Usage](#Installation-and-Usage)
- [Running tests](#Running-tests)
- [Features](#Features)
- [Documetation Overview](#Documetation-Overview)
- [Changelog](#Changelog)

## System Requirements

- **Python 3** or above
- **pydicom** (can be installed with `pip install pydicom`)
- **pandas** (can be installed with `pip install pandas`)

## Installation and Usage

To download as zip: <https://github.com/SuryadiTjandra/automated-plan-checking/archive/master.zip>

To install with git: `git clone https://github.com/SuryadiTjandra/automated-plan-checking.git`

Usage:

- Single dicom
    - `python app.py --inputs Resources/Input/YellowLvlIII_7a.dcm`
- Folder of dicoms
    - `python app.py --inputs Resources/Input`
- Process all dicoms across 2 folders
    - `python app.py --inputs Resources/Input OTHER_DICOM_FOLDER`
- Process all dicoms in folder assuming all are the same case
    - `python app.py --inputs Resources/Input  --case_number 6`
- Process any number of individual dicoms
    - `python app.py --inputs Resources/Input/YellowLvlIII_7a.dcm Resources/Input/YellowLvlIII_7b.dcm`
- Process any number of separate dicoms, giving case numbers for each (format: dicom,case, dicom2,case ... etc).
    - `python app.py --inputs Resources/Input/YellowLvlIII_7a.dcm,1 Resources/Input/YellowLvlIII_7b.dcm,2`
- Process any number of folders, giving case numbers for each (format: folder,case, folder2,case ... etc).
    - `python app.py --inputs Resources/Input,1 OTHER_DICOM_FOLDER,2`
- Use the file `truth_table_example.csv` as input for the truth table that will be used to evaluate extracted parameters
    - `python app.py --inputs Resources/Input --truth_table truth_table_example.csv`

## Running Tests

Run all tests with `python -m unittest`

Run tests for a particular class with `python -m unittest test_parameter_retrieval.<ClassName>`, where `<ClassName>` could be replaced by `TestIMRTExtractionValues`.

Run a particular test (i.e prescription dose) with `python -m unittest test_parameter_retrieval.<ClassName>.<FunctionName>` where `<ClassName>` and `<FunctionName>` could be `TestIMRTExtractionValues` and `test_total_prescription_dose`, respectively.

## Features

...

## Documentation Overview

Full project documentation generated from a Confluence space can be found in [docs](docs) folder

It contains the project background in more depth as well as architecture, full user guide, requirements list, ...

## Changelog

...
