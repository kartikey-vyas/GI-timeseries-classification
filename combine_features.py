"""This script combines, filters and saves the relevant extracted features. Requires completion of 
the hypothesis testing and feature selection scripts. 

The features are sorted by their p-values for distinguishing AT.

Output
-------
Generates a design matrix with the relevant features.
Saves as an hdf (.h5) file in data/features/filtered/

Author: Kartikey Vyas"""

import argparse
import glob
import pandas as pd

## INITIALISE ARGPARSER ----------------------------------------------------------------------------------
parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawTextHelpFormatter)
parser.add_argument('alpha', type=float)
args = parser.parse_args()

## LOAD DATA ---------------------------------------------------------------------------------------------
X_filt = pd.DataFrame()

for file in glob.glob("data/features/*_eff.h5"):
    X = pd.read_hdf(file)
    X.reset_index(inplace=True, drop=True)
    length = X.columns[X.columns.str.endswith('_length')][0]
    idx_to_remove = list(X[X[length] == 1].index)
    X = X.drop(idx_to_remove)
    X_filt = pd.concat([X_filt, X], axis=1)

# retrieve the relevant features
relevant = pd.read_hdf('data/relevant_features_alpha_'+str(args.alpha)+'_.h5')
relevant = relevant.sort_values(by=['at'])

# SELECT FEATURES ----------------------------------------------------------------------------------------
X_filt = X_filt[relevant['feature'].values]

# add subject column to use in grouped CV iterator
subject = 0
for i in range(1,6):
    X_filt.loc[(i-1)*90:i*90, 'subject'] = subject
    subject += 1
X_filt.reset_index(inplace=True, drop=True)

X_filt.to_hdf("data/features/filtered/achat_filtered_"+str(args.alpha)+"_.h5", key="features", complevel=9)
