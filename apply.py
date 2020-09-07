""" Apply functions in myfunctions to arg 'dataset'

Separates the parameter extraction from file reading, 
function application, output, etc. 

This organisation will hopefully make it easier on the parameter 
addition side which is where I anticipate future development work will be done.
"""

import inspect as ins
import myfunctions

# Assume access to 
dataset = None

# What it do: Get functions from a module and apply them to the dataset
# What it is: A list of the return values of each function when fed the dataset
[func(dataset) for name,func in ins.getmembers(myfunctions, ins.isfunction)]