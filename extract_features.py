"""This script runs parallelized, automated feature extraction on processed MEA data
tsfresh is used to extract the set of "Efficient" features that can be computed from the input data
It is designed to be used in conjunction with the `extract_features.sl` slurm
script, which creates a feature extration job for each signal in the MEA data.
The optional flag '-diffs' computes signals that are the difference between signals from neighbouring
electrodes and feeds them into the feature extraction.

Command line arguments 
----------
filename: Name of .h5 file that is placed in the data/processed/ folder.
            This should contain the full dataset containing ts signals
        
electrode: Number that represents the electrode number of the signal to use.
            Should be set to environment variable $SLURM_ARRAY_TASK_ID

Output
-------
Generates a design matrix with the extracted features for the specified signal.
Saves as an hdf (.h5) file in data/features/

Author: Kartikey Vyas"""

## IMPORTS ----------------------------------------------------------------------------------------------
import os.path
import argparse
import logging
import time
from datetime import datetime
import pandas as pd
import numpy as np
from tsfresh import extract_features
from tsfresh.feature_extraction import EfficientFCParameters
from tsfresh.utilities.dataframe_functions import impute

## PARSE COMMAND LINE ARGS ---------------------------------------------------------------------------------
parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawTextHelpFormatter)
parser.add_argument('filename')
parser.add_argument('electrode', type=int)
parser.add_argument('-diffs', action='store_true', help='computes differences between neighbouring signals\
and runs feature extraction on difference signals')
args = parser.parse_args()

## INITIALISE LOGGING --------------------------------------------------------------------------------------
# use current time as a unique identifier
now = datetime.now()
job_id = now.strftime("%d%m%y_%H%M%S")
electrode = str(args.electrode)
if args.diffs:
    electrode += '_diffs'

# create log file
logging.basicConfig(filename='logs/feature_extraction/feature_extraction_'+electrode+'_'+job_id+'.txt', level=logging.DEBUG)

if os.path.isfile('data/processed/'+args.filename) == False:
    logging.error("Specified file not found - terminating script")
    exit()

if args.electrode not in range(0,60):
    logging.error("Invalid electrode selected - terminating script")
    exit()

## for now, load the full data frame, retrieve the relevant columns and then delete the full df from memory
## it would probably be faster to generate 60 dataframes and access the desired one...

## LOAD DATA -------------------------------------------------------------------------------------------------
start = time.process_time()

fpath = "data/processed/"+args.filename
df = pd.read_hdf(fpath)

logging.info("loaded dataframe")
col = args.electrode

if args.diffs:
    # find the neighbouring electrode numbers
    config = np.load('config.npy')
    pos = np.where(config == col)
    neighbours = []

    # corners are invalid
    if pos[0][0] != 7: # NOT bottom edge
        neighbours.append(config[pos[0][0]+1, pos[1][0]])
        if pos[1][0] != 7: # NOT right edge
            neighbours.append(config[pos[0][0], pos[1][0]+1])
            neighbours.append(config[pos[0][0]+1, pos[1][0]+1])
        if pos[1][0] != 0: # NOT left edge
            neighbours.append(config[pos[0][0]+1, pos[1][0]-1]) 
            neighbours.append(config[pos[0][0], pos[1][0]-1])
    else: # bottom edge
        neighbours.append(config[pos[0][0], pos[1][0]+1])
        neighbours.append(config[pos[0][0], pos[1][0]-1])
    if pos[0][0] != 0: # NOT top edge
        neighbours.append(config[pos[0][0]-1, pos[1][0]])
        if pos[1][0] != 7: # NOT right edge
            neighbours.append(config[pos[0][0]-1, pos[1][0]+1])
        if pos[1][0] != 0: # NOT left edge
            neighbours.append(config[pos[0][0]-1, pos[1][0]-1])
            
    # remove any occurences of the corner eletrodes (they are labelled 255)        
    neighbours = [i for i in neighbours if i != 255]
    logging.info("neighbours found")
    
    # create new signal using differences
    df_diffs = (df[neighbours]
           .sub(df[col], axis=0)
           .add_suffix('_'+str(col)+'_diff'))
    df = pd.concat([df[['id']], df_diffs], axis=1)
    logging.info("differences computed")
    
    # free up some memory
    del df_diffs
else: 
    # select relevant columns, ignore neighbours
    df = df[['id', col]]

## FEATURE EXTRACTION ----------------------------------------------------------------------------------------
logging.info("beginning feature extraction")
X = extract_features(df, column_id='id', default_fc_parameters=EfficientFCParameters(), impute_function=impute, n_jobs=16)
logging.info("feature extraction complete, ")

prefix = args.filename[:-3]
X.to_hdf('data/features/'+prefix+'_'+electrode+'_eff.h5', key='data', complevel=9)
logging.info("features saved to 'data/features/"+prefix+"_"+str(args.electrode)+"_eff.h5'")

logging.info("time taken = "+str(time.process_time() - start))
