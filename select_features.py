"""This script runs feature selection on extracted features from the MEA data, after p-values generated.
The Benjamini-Yekutieli procedure is used to adjust p-values, accounting for accumulated statistical 
error.

Command Line Arguments
----------------------

alpha: False Discovery Rate (FDR) level.
        This should be a float between 0 and 1

Output
-------
Generates a design matrix with the selected features for each set of extracted features in data/features/.
Saves as an hdf (.h5) file in data/features/filtered/

Author: Kartikey Vyas"""

## IMPORTS ----------------------------------------------------------------------------------------------
import argparse
import datetime
import subprocess
import os
import logging
import time
from datetime import datetime
import glob
import pandas as pd
from statsmodels.stats.multitest import multipletests


## INITIALISE ARGPARSER ---------------------------------------------------------------------------------
parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawTextHelpFormatter)
parser.add_argument('alpha', type=float)
args = parser.parse_args()

## INITIALISE LOGGING -----------------------------------------------------------------------------------
# use current time as a unique identifier
now = datetime.now()
job_id = now.strftime("%d%m%y_%H%M%S")

# create directories if not already there
if not os.path.isdir('logs/feature_selection/'):
    subprocess.run(['mkdir', 'logs/feature_selection'],
    check=True, text=True)

if not os.path.isdir('data/features/filtered/'):
    subprocess.run(['mkdir', 'data/features/filtered'],
    check=True, text=True)

# create log file
logging.basicConfig(filename='logs/feature_selection/feature_selection_'\
    +'_'+job_id+'.txt', level=logging.DEBUG)


## LOAD DATA --------------------------------------------------------------------------------------------
start = time.process_time()

logging.info("loading vector of p-values")
df = pd.read_hdf('data/p_values.h5')

# clean up any rows which don't have numeric values
df = df.drop(df[df['ach'].apply(lambda x: isinstance(x, str))].index)
alpha = args.alpha

## BENJAMINI-YEKUTIELI PROCEDURE ------------------------------------------------------------------------
logging.info("running b-y tests with FWER = "+str(alpha))

# run the benjamini-yekutieli procedure on each column
accept_0 = multipletests(df.iloc[:,0], method='fdr_by', alpha=alpha)
accept_1 = multipletests(df.iloc[:,1], method='fdr_by', alpha=alpha)
accept_2 = multipletests(df.iloc[:,2], method='fdr_by', alpha=alpha)

logging.info("saving adjusted p-values")
# save each vector in case we want to use them individually
baseline = pd.DataFrame([accept_0[0],accept_0[1]])
ach = pd.DataFrame([accept_1[0],accept_1[1]])
at = pd.DataFrame([accept_2[0],accept_2[1]])

baseline.T.to_hdf('data/baseline_adj_p_values.h5', key='data', complevel=9)
ach.T.to_hdf('data/ach_adj_p_values.h5', key='data', complevel=9)
at.T.to_hdf('data/at_adj_p_values.h5', key='data', complevel=9)

## SELECT FEATURES --------------------------------------------------------------------------------------
logging.info("selecting relevant features")

# accept features that are accepted for all 3 target vars
accept_all = accept_0[0]*accept_1[0]*accept_2[0]
relevant = df[accept_all]

# save relevant features
relevant.to_hdf('data/relevant_features.h5', key='data', complevel=9)

print(str(time.process_time() - start))