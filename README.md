# automated-plan-checking

`Unimelb COMP90082 :: 2020 Semester 2 :: Team AT-Koala`

Extract and evaluate data from DICOM RT-PLAN files.

**README best viewed with a [markdown reader](https://markdownlivepreview.com/) or on the [github page](https://github.com/SuryadiTjandra/automated-plan-checking)**

## Table of contents

[**Project background**](#project-background)

[**System requirements**](#system-requirements)

[**Installation and Usage**](#installation-and-usage)

- [**Truth table specification**](#truth-table-specification)
  
[**Documentation**](#documentation)

- [**Architecture**](#architecture)
- [**Test cases**](#test-cases)

[**Testing**](#testing)

[**Features**](#features)

- [**Sprint1**](#sprint1)
- [**Sprint2**](#sprint2)

[**Changelog**](#changelog)

## Project background

This project is with the Australian Radiation Protection and Nuclear Safety Agency.

The aim is to create a program that can perform an automated check of data and parameters with a Pass/Fail result.

Currently, the process to verify planning parameters is to manually check pdf print outs. The information required is contained in the DICOM RT-PLAN files created for each treatment plan. The goal is a program that can directly extract the information from the DICOM file and then compare this data to a standard data set to produce a pass/fail evaluation.

## System requirements

- **Python 3.6** or above
- **pydicom** (can be installed with `pip install pydicom`)
- **pandas** (can be installed with `pip install pandas`)

## Installation and Usage

To download as zip: <https://github.com/SuryadiTjandra/automated-plan-checking/archive/master.zip>

To install with git: `git clone https://github.com/SuryadiTjandra/automated-plan-checking.git`

Usage:

- Process single dicom
  - `python app.py --inputs data/Input/YellowLvlIII_7a.dcm`
- Process a folder of dicoms
  - `python app.py --inputs data/Input`
- Multiple dicoms or folders in any order
  - `python app.py --inputs FOLDER1 FOLDER2 FILE1 FILE2 FOLDER3 (etc...)`
  - Example: - `python app.py --inputs data/Input data/Input/more-input`
- Specify case number for each input item
  - `python app.py --inputs INPUT1,CASE1 INPUT2,CASE2`
  - Example: - `python app.py --inputs data/Input/YellowLvlIII_7a.dcm,7 data/Input/YellowLvlIII_7b.dcm,7`
- Specify case for all inputs
  - `python app.py --inputs INPUTS --case_number 7`
  - Example: - `python app.py --inputs data/Input  --case_number 7`
- Specify a custom truth table (default uses level 3 table)
  - `python app.py --inputs INPUTS --truth_table TRUTH_TABLE`
  - Example: - `python app.py --inputs data/Input --truth_table data/truth_table_lvl3_.csv`

More details can be found in the [User guide](https://github.com/SuryadiTjandra/automated-plan-checking/blob/master/docs/atkoala-UserGuide-271020-1338-2126.pdf).

### Writing truth tables

- Must be in csv format.
- Column headings must be standard parameters (case, mode, prescription dose ...).
- There are specified formats for Gantry angle, SSD, Prescripton Dose/# Fractions, Wedge Angle, Collimator, and Field Size.
- Mode and Energy are not evaluated with a pass/fail value.
- Other parameters (Prescription Point, Isocenter, Override, Couch, Meas.) have not beem implemented, therefore no formats have been specified yet.
- Unless otherwise specified, there should be no spaces in any truth table entries
- Gantry angle:
  - dash (-) indicating all values pass
  - numbers separated by commas to indicate the gantry of each beam
- SSD:
  - dash (-) indicating all values pass
  - numbers separated by commas to indicate the SSD of each beam. Any number can be replaced with a question mark (?) for a specific beam to indicate it accepts any value.
- Prescription Dose/#:
  - Prescription dose followed by a slash followed by the number of fractions followed by dosimeter unit (e.g. 2/1/-)
  - The dosimeter unit can be dash (-) if all units are accepted, otherwise it can specify MU
- Wedge Angle:
  - Comma separated string of numbers/no wedge
  - "no wedge" has a space inbetween
- Collimator:
  - number, dash or asterix number
  - asterix means the value must not be the following number
- Field Size
  - dash (-) indicating all values pass
  - A single field size can be specified with length by width (e.g. 10x10)
  - Multiple field sizes should be separated by commas, indicating the field size of each beam

Sample truth tables (for [level 2](data/truth_table_example.csv) and [level 3](data/truth_table_lvl2_example.csv))

## Documentation

### Architecture

[Architecture](https://github.com/SuryadiTjandra/automated-plan-checking/blob/master/docs/System-Design-and-Architecture.pdf) of the project, exported from Confluence. It includes components of the program and system design.

### Test cases

[Test cases](https://github.com/SuryadiTjandra/automated-plan-checking/blob/master/docs/Acceptance-Tests.pdf) of the project, exported from Confluence.

## Testing

Run the tests with `python -m unittest`

Run tests for a particular class with `python -m unittest test_parameter_retrieval.[ClassName]`.

- e.g `python -m unittest test_parameter_retrieval.TestIMRTExtractionValues`

Run a particular test (i.e prescription dose) with `python -m unittest test_parameter_retrieval.[ClassName].[FunctionName]`.

- e.g `python -m unittest test_parameter_retrieval.TestIMRTExtractionValues.test_total_prescription_dose`

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

## Changelog

### Sprint 2

- Update mode output ([#23](https://github.com/SuryadiTjandra/automated-plan-checking/pull/23))
- More error handling ([#21](https://github.com/SuryadiTjandra/automated-plan-checking/pull/21))
- Field size parameter implemented ([#20](https://github.com/SuryadiTjandra/automated-plan-checking/pull/20))
- Mode parameter ([#20](https://github.com/SuryadiTjandra/automated-plan-checking/pull/20))
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
