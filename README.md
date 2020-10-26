# Table of contents
[**Project background**](#project-background)

[**User stories**](#user-stories)

[**Documentation**](#documentation)
  * [**User stories**](#user-stories)
  * [**Architecture**](#architecture)
  * [**Test cases**](#test-cases)
  
[**System requirements**](#system-requirements)

[**Installation and Usage**](#installation-and-usage)
  * [**Testing**](testing)
  
[**Changelog**](#changelog)



## Project background
This project is with the Australian Radiation Protection and Nuclear Safety Agency.

The aim is to create a program that can perform an automated check of data and parameters with a Pass/Fail result.

Currently, the only way to verify planning parameters is to manually check pdf print outs. The information required is contained in the planning DICOM files created for each treatment plan. Clients need a program that can extract the information from the DICOM file and then compare this data to a standard data set to verify it is within specifications.

The goal of this project and our clients want our team to achieve is to create a program that can replace the manual process outlined in the previous paragraph; which will read data points directly from the DICOM files generated and perform an automated check of the parameters extracted.
## User stories
01	As an Auditor,	I want parameter values to be output when running the program, as a csv

02	As an Auditor,	I also want each parameter value to be evaluated with a pass/fail result and recorded in the csv output

03	As an Auditor,	I want the value acceptance ranges to be output in the csv as well

04	As an Auditor,	It would be useful that  the range of acceptable values will automated modified depending on the file

05	As an Auditor,	I want to be able to specify the case of the files I'm processing (necessary if partial parameter extraction)

06	As an Auditor,	I want to be able to process batches of dicoms at a time

07	As an Auditor,	(Parameter) I want to know the angle of the machine gantry

08	As an Auditor,	(Parameter) I want to know the angle of the beam limiting device (aka collimator)

09	As an Auditor,	(Parameter) I want to know the SSD (source to skin distance)

10	As an Auditor,	(Parameter) I want to know the total amount of radiation dose planned(aka prescription dose/#)

11	As an Auditor,	(Parameter) I want to know the number of fractions the dose will be split up into(combined with prescription dose, 50/25 means 50 dose 25 fractions)

12	As an Auditor,	(Parameter) I want to know the wedge angle(s)

13	As an Auditor,	(Parameter) I want to know the machine energy(doesn't need to be evaluated)

14	As an Auditor,	(Parameter) I want to know the fluence mode of the radiation beams(attached to energy)

15	As an Auditor,	(Parameter) I want to know the field size of the radiation beam

16	As an Auditor,  (Parameter) I want to know the modality of treatment [imrt, vmat, 3dcrt, dcat, tomo, f-cone, hyp-arc, g-knife]
## Documentation
## Architecture

## Test cases
[Test cases](https://github.com/SuryadiTjandra/automated-plan-checking/blob/master/tests/atkoala-Test-271020-0054-2114.pdf) of the project ,exported from Confluence.

## System requirements

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
- `python app.py --inputs Resources/Input --format csv --truth_table truth_table_example.csv` <- Use the file ``truth_table_example.csv`` as input for the truth table that will be used to evaluate extracted parameters

## Testing

Test code is in `test_parameter_retrieval.py`.

### Running Tests

Run the tests with `python -m unittest`

Run tests for a particular class with `python -m unittest test_parameter_retrieval.ClassName`

e.g `python -m unittest test_parameter_retrieval.TestIMRTExtractionValues`

Run a particular test (i.e prescription dose) with `python -m unittest test_parameter_retrieval.ClassName.FunctionName`

e.g. `python -m unittest test_parameter_retrieval.TestIMRTExtractionValues.test_total_prescription_dose`


## Changelog
