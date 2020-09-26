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
Run the tests with `test command`

