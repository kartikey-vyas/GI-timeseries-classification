"""This script runs hypothesis tests to filter features extracted from the MEA data.
The Mann-Whitney U test is used to determine whethere a feature provides good separation between
all 3 categories of target variable.

Output
-------
Generates a dataframe of p-values, with each row corresponding to a feature.
Saves as an hdf (.h5) file in data/.

Author: Kartikey Vyas"""

## IMPORTS ----------------------------------------------------------------------------------------------
import argparse
import logging
import time
import re
from datetime import datetime
import os
import glob
import subprocess
import pandas as pd
import numpy as np
from tsfresh.feature_selection.significance_tests import target_binary_feature_real_test

## INITIALISE ARGPARSER FOR COMMAND LINE HELP -----------------------------------------------------------
parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawTextHelpFormatter)
args = parser.parse_args()

## INITIALISE LOGGING -----------------------------------------------------------------------------------
# use current time as a unique identifier
now = datetime.now()
job_id = now.strftime("%d%m%y_%H%M%S")

# create directories if not already there
if not os.path.isdir('logs/feature_selection/'):
    subprocess.run(['mkdir', 'logs/feature_selection'],
    check=True, text=True)

# create log file
logging.basicConfig(filename='logs/feature_selection/hyp_test_'\
    +'_'+job_id+'.txt', level=logging.DEBUG)

## LOADING DATA -----------------------------------------------------------------------------------------
start = time.process_time()

y = pd.read_hdf('data/ach_at_combined_y.h5')
y_bin = y.astype('category')
y_bin = pd.get_dummies(y_bin)

logging.info("Loaded target variable")

## FEATURE SELECTION -------------------------------------------------------------------------------------
loop = 0

p_vector = []
X_filt = pd.DataFrame()

# get all the paths of the files to be loaded in
for file in glob.glob("data/features/*_eff.h5"):
    # load feature dataframe
    X = pd.read_hdf(file)
    # X_filt = pd.DataFrame()
    logging.info("Loaded Features from: "+file)

    # look for rows in X where len == 1
    # this is needed due to a quirk in the data processing functions - 
    # some of the time windows end up only including 1 step (1ms)
    if loop == 0:
        idx_to_remove = np.setdiff1d(y.index,X.index)
        y = y.drop(idx_to_remove)
    loop = 1
    # test each feature with Mann-Whitney U Test
    logging.info("Testing Hypothesis...")
    for feature in X:
        p = []
        try:
            p.append(target_binary_feature_real_test(X[feature],y_bin[0],'mann'))
            p.append(target_binary_feature_real_test(X[feature],y_bin[1],'mann'))
            p.append(target_binary_feature_real_test(X[feature],y_bin[2],'mann'))
        except ValueError:
            p.append(1000)
            p.append(1000)
            p.append(1000)

        p.append(feature)
        p_vector.append(p)

# Save target variable
y = y.reset_index(0, drop=True)
y.to_hdf('data/ach_at_combined_y.h5', key='y', complevel=9)
logging.info('target variable saved to data/achat_y.h5')

# Save vector of p-values
df_p = pd.DataFrame(p_vector, columns = ['baseline', 'ach', 'at', 'feature'])
df_p.to_hdf('data/p_values.h5', key='p_vals', complevel=9)
logging.info('vector of p-values saved to data/p_values.h5')

logging.info('time taken = '+str(time.process_time() - start))
