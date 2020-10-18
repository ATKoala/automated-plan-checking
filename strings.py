""" strings Module - A collection of commonly used strings throughout the project

Purpose:
- Standard string format: e.g. <"10x12" vs "10 x 12"> 
    Although they both look reasonable, format must be consistent throughout the project for equality comparisons.
- Easier changes: If a string were to be changed, it can be done with one change in this file.

What kind of strings go in here:
- Strings that are used in equality comparisons
- Strings that are used more than 

Including:
    - Strings from truth table values
    - Error message strings
    - Other strings
"""

NOT_IMPLEMENTED= "NOT IMPLEMENTED"
mode_req = "mode req"
prescription_dose_slash_fractions = "prescription dose/#"
prescription_point = "prescription point"
isocenter_point = "isocentre point"
override = "override"
collimator = "collimator"
gantry = "gantry"
SSD = "SSD"
couch = "couch"
field_size = "field_size"
wedge = "wedge"
meas = "meas"
energy = "energy"
VMAT = "VMAT"
IMRT = "IMRT"
VMAT_unknown = "VMAT unknown"
hyphen = "-"
FAIL = "FAIL"
PASS = "PASS"
SETUP_beam = "SETUP beam"
no_wedge = "no wedge"
STANDARD = "STANDARD"
FFF = "FFF"