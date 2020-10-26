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

- Process single dicom
  - `python app.py --inputs Resources/Input/YellowLvlIII_7a.dcm`
- Process a folder of dicoms
  - `python app.py --inputs Resources/Input`
- Multiple dicoms or folders in any order
  - `python app.py --inputs FOLDER1 FOLDER2 FILE1 FILE2 FOLDER3 (etc...)`
- Specify case number for each input item
  - `python app.py --inputs INPUT1,CASE1 INPUT2,CASE2`
- Specify case for all inputs
  - `python app.py --inputs INPUTS --case_number 6`
- Specify a custom truth table (default uses level 3 table)
  - `python app.py --inputs INPUTS --truth_table truth_table_example.csv`

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
