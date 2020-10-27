# Table of contents

[**Project background**](#project-background)

[**Features**](#features)

- [**Sprint1**](#sprint1)
- [**Sprint2**](#sprint2)
  
[**Documentation**](#documentation)

- [**Architecture**](#architecture)
- [**Test cases**](#test-cases)
  
[**System requirements**](#system-requirements)

[**Installation and Usage**](#installation-and-usage)

- [**Testing**](#testing)
  
[**Changelog**](#changelog)

## Project background

This project is with the Australian Radiation Protection and Nuclear Safety Agency.

The aim is to create a program that can perform an automated check of data and parameters with a Pass/Fail result.

Currently, the only way to verify planning parameters is to manually check pdf print outs. The information required is contained in the planning DICOM files created for each treatment plan. Clients need a program that can extract the information from the DICOM file and then compare this data to a standard data set to verify it is within specifications.

The goal of this project and our clients want our team to achieve is to create a program that can replace the manual process outlined in the previous paragraph; which will read data points directly from the DICOM files generated and perform an automated check of the parameters extracted.

## Features

### Sprint1

01 As an Auditor, I want parameter values to be output when running the program, as a csv

02 As an Auditor, I also want each parameter value to be evaluated with a pass/fail result and recorded in the csv output

05 As an Auditor, I want to be able to specify the case of the files I'm processing (necessary if partial parameter extraction)

07 As an Auditor, (Parameter) I want to know the angle of the machine gantry

08 As an Auditor, (Parameter) I want to know the angle of the beam limiting device (aka collimator)

09 As an Auditor, (Parameter) I want to know the SSD (source to skin distance)

10 As an Auditor, (Parameter) I want to know the total amount of radiation dose planned(aka prescription dose/#)

11 As an Auditor, (Parameter) I want to know the number of fractions the dose will be split up into(combined with prescription dose, 50/25 means 50 dose 25 fractions)

12 As an Auditor, (Parameter) I want to know the wedge angle(s)

13 As an Auditor, (Parameter) I want to know the machine energy(doesn't need to be evaluated)

14 As an Auditor, (Parameter) I want to know the fluence mode of the radiation beams(attached to energy)

### Sprint2

03 As an Auditor, I want the value acceptance ranges to be output in the csv as well

04 As an Auditor, It would be useful that  the range of acceptable values will automated modified depending on the file

06 As an Auditor, I want to be able to process batches of dicoms at a time

15 As an Auditor, (Parameter) I want to know the field size of the radiation beam

16 As an Auditor, (Parameter) I want to know the modality of treatment [imrt, vmat, 3dcrt, dcat, tomo, f-cone, hyp-arc, g-knife]

## Documentation

### Architecture

[Architecture](https://github.com/SuryadiTjandra/automated-plan-checking/blob/master/docs/System-Design-and-Architecture.pdf) of the project, exported from Confluence. It includes components of the program and system design.

### Test cases

[Test cases](https://github.com/SuryadiTjandra/automated-plan-checking/blob/master/tests/atkoala-Test-271020-0054-2114.pdf) of the project ,exported from Confluence.

## System requirements

- **Python 3.6** or above
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
  - Example: - `python app.py --inputs Resources/Input OTHER_DICOM_FOLDER --format csv --case_number 6`
- Specify case number for each input item
  - `python app.py --inputs INPUT1,CASE1 INPUT2,CASE2`
  - Example: - `python app.py --inputs Resources/Input/YellowLvlIII_7a.dcm,1 Resources/Input/YellowLvlIII_7b.dcm,2 --format csv`
- Specify case for all inputs
  - `python app.py --inputs INPUTS --case_number 6`
  - Example: - `python app.py --inputs Resources/Input --format csv --case_number 6`
- Specify a custom truth table (default uses level 3 table)
  - `python app.py --inputs INPUTS --truth_table truth_table_example.csv`
  - Example: - `python app.py --inputs Resources/Input --format csv --truth_table truth_table_example.csv`

"--format csv" can be added in any command as the argument, generating csv output file. More details can be found in the [User guide](https://github.com/SuryadiTjandra/automated-plan-checking/blob/master/docs/atkoala-UserGuide-271020-1338-2126.pdf).

## Testing

Run the tests with `python -m unittest`

Run tests for a particular class with `python -m unittest test_parameter_retrieval.ClassName`, where `<ClassName>` could be replaced by `TestIMRTExtractionValues`.

- e.g `python -m unittest test_parameter_retrieval.TestIMRTExtractionValues`

Run a particular test (i.e prescription dose) with `python -m unittest test_parameter_retrieval.ClassName.FunctionName`, where `<ClassName>` and `<FunctionName>` could be `TestIMRTExtractionValues` and `test_total_prescription_dose`, respectively.

- e.g `python -m unittest test_parameter_retrieval.TestIMRTExtractionValues.test_total_prescription_dose`

## Changelog

### Sprint 2

- Update mode output ([#23)](https://github.com/SuryadiTjandra/automated-plan-checking/pull/23))
- More error handling ([#21)](https://github.com/SuryadiTjandra/automated-plan-checking/pull/21))
- Field size parameter implemented ([#20)](https://github.com/SuryadiTjandra/automated-plan-checking/pull/20))
- Mode parameter ([#20)](https://github.com/SuryadiTjandra/automated-plan-checking/pull/20))
- Refactor ([#19](https://github.com/SuryadiTjandra/automated-plan-checking/pull/19))
- Strings Module ([#18](https://github.com/SuryadiTjandra/automated-plan-checking/pull/18))
- Properties File ([#17](https://github.com/SuryadiTjandra/automated-plan-checking/pull/17))
- Truth table standardization ([#14](https://github.com/SuryadiTjandra/automated-plan-checking/pull/14))
- Input truth table ([#13](https://github.com/SuryadiTjandra/automated-plan-checking/pull/13))
- Add batch processing ([#11](https://github.com/SuryadiTjandra/automated-plan-checking/pull/11))
- More informative output ([#10](https://github.com/SuryadiTjandra/automated-plan-checking/pull/10))

### Sprint 1

- Modularize parameter extraction ([#9](https://github.com/SuryadiTjandra/automated-plan-checking/pull/9))
- Unit Tests ([#8](https://github.com/SuryadiTjandra/automated-plan-checking/pull/8))
- Nominal Beam Energy ([#4](https://github.com/SuryadiTjandra/automated-plan-checking/pull/4))
- Command line args ([#3](https://github.com/SuryadiTjandra/automated-plan-checking/pull/3))
- Total Prescription Dose ([#2](https://github.com/SuryadiTjandra/automated-plan-checking/pull/2))
- SSD (initial commit)
- Number of fractions (initial commit)
- Gantry Angle (initial commit)
- Collimator angle (initial commit)
