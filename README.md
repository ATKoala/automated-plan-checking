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

To download as zip: <https://github.com/ATKoala/automated-plan-checking/archive/master.zip>

### Usage

1. Open the settings.txt file and edit the input, output and truth table files to the desired locations.
2. Navigate to app.py in Spyder and click Run.

More details can be found in the [User guide](docs/User-Guide.pdf).

## Documentation

### For Users

- [User Guide](docs/User-Guide.pdf)

### For Developers

- [Customising Truth Tables](docs/Writing-Truth-Tables.pdf)
- [Adding a new Parameter](docs/Adding-Parameters.pdf)
- [User Stories](docs/User-Stories.pdf) shows the features completed and not completed, as well as notes on completed features.
- [Architecture](docs/System-Design-and-Architecture.pdf) includes components of the program and how modules fit together.
- [Test cases](docs/Test-Cases.pdf) describes the results from manually testing various parts of the system.
- [Parameter Information](docs/Parameter-Information.pdf) contains some information about the parameters for future developers without domain knowledge.
