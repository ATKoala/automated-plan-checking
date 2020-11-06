# automated-plan-checking

`Extract and evaluate data from DICOM RT-PLAN files.`

*README best viewed on the [github page](https://github.com/ATKoala/automated-plan-checking)*

## Table of contents

[**Project background**](#project-background)

[**System Setup**](#system-setup)

- [**Anaconda and Spyder**](#anaconda-setup)
- [**Pip and command line**](#pip-setup)

[**Installation and Usage**](#installation-and-usage)
  
- [**Usage**](#usage)

[**Documentation**](#documentation)

- [**For Users**](#for-users)
- [**For Developers**](#for-developers)

## Project background

This project is with the Australian Radiation Protection and Nuclear Safety Agency.

The aim is to create a program that can perform an automated check of data and parameters with a Pass/Fail result.

Currently, the process to verify planning parameters is to manually check pdf print outs. The information required is contained in the DICOM RT-PLAN files created for each treatment plan. The goal is a program that can directly extract the information from the DICOM file and then compare this data to a standard data set to produce a pass/fail evaluation.

## System Setup

### Anaconda Setup

1. Open Spyder
2. Check the python version in the bottom bar, if it's below 3.6, update by running `conda update python` in the Spyder console.
3. Anaconda comes with pandas preinstalled, but check it with `conda list pandas` in the console.
4. Install pydicom by running `conda install -c conda-forge pydicom` in the console.

### Pip Setup

The necessary packages can also be installed using python's package manager pip and a command prompt/shell.

1. Ensure that the python version is **Python 3.6** or above. (Run `python --version` on the command line)
2. Install pydicom (can be installed with `pip install pydicom`)
3. Install pandas (can be installed with `pip install pandas`)

## Installation and Usage

To download as zip: <https://github.com/ATKoala/automated-plan-checking/archive/master.zip>

To install with git: `git clone https://github.com/ATKoala/automated-plan-checking.git`

### Usage

1. Open the settings.txt file and edit the input, output and truth table files to the desired locations
2. Navigate to app.py in Spyder and click Run.

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

More details can be found in the [User guide](docs/User-Guide.pdf).

## Documentation

### For Users

- [User Guide](docs/User-Guide.pdf)

### For Developers

- [Customising Truth Tables](docs/Writing-Truth-Tables.pdf)
- [Adding a new Parameter](docs/Adding-Parameters.pdf)
- [User Stories](docs/User-Stories.pdf) shows the stories completed and not completed, as well as notes on completed features.
- [Architecture](docs/System-Design-and-Architecture.pdf) includes components of the program and how modules fit together.
- [Test cases](docs/Test-Cases.pdf) describes the results from manually testing various parts of the system.
- [Parameter Information](docs/Parameter-Information.pdf) contains some information about the parameters for future developers without domain knowledge.
