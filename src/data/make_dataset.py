"""This script reads in the raw data, converts it into a pandas DataFrame object and 
labels it. Data is cut into discrete time windows.

Command line arguments 
----------
dir: directory containing the raw data

fname: file name to save output dataframe under

window: size in ms of the discrete time windows

Output
-------
pandas DataFrame
Saves as an hdf (.h5) file in data/processed/

Author: Kartikey Vyas"""

## IMPORTS ----------------------------------------------------------------------------------------------
import argparse
import pandas as pd
import numpy as np
from src.data.load_data import generate_dataset

## PARSE COMMAND LINE ARGS ------------------------------------------------------------------------------
parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawTextHelpFormatter)
parser.add_argument('dir')
parser.add_argument('fname')
parser.add_argument('window', type=int)
args = parser.parse_args()


## LOAD AND PROCESS DATA --------------------------------------------------------------------------------
generate_dataset(args.fname, args.dir, args.window)
