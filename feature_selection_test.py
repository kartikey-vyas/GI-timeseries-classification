"""Feature selection is done through a local branch of tsfresh, which has been modified to handle multiclass
classification problems. The filtering process uses the Mann-Whitney U test to determine statistical significance
for predicting the target. The Benjamini-Yekutieli procedure is used to account for family-wise error rate and
select only the relevant features.

Command line arguments 
----------
window_size: Number of time steps in each observation. Choose 4000, 6000 or 10000.
             Determines which set of features will be used in the pipeline.
             one of:
                ach-at-hex_4000_eff_combined.h5
                ach-at-hex_6000_eff_combined.h5
                ach-at-hex_10000_eff_combined.h5
        
n_significant: Number of classes for which a feature needs to be a statistically significant predictor to be
               accepted as relevant. This is passed into tsfresh.transformers.FeatureSelector().
               
n_classes: Number of classes in the target variable.
           one of:
           4 - baseline, ach, at, hex
           3 - baseline, ach, (at or hex)
           2 - baseline, (ach, at or hex) OR at, hex

Output
-------
grid: GridSearchCV object, stored as HDF file

Author: Kartikey Vyas"""

import argparse
from joblib import dump

import pandas as pd
import numpy as np

from src.features.modified_feature_selector import FeatureSelector

## PARSE COMMAND LINE ARGS ---------------------------------------------------------------------------------
parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawTextHelpFormatter)
parser.add_argument('window_size', help='Number of time steps in each observation. Choose 4000, 6000 or 10000.')
parser.add_argument('n_classes', help='Number of classes in the target variable')
args = parser.parse_args()

assert int(args.window_size) in [4000, 6000, 10000], 'window_size must be one of 4000, 6000 or 10000'

## LOAD DATA --------------------------------------------------------------------------------------------
X = pd.read_hdf('data/features/ach-at-hex_'+args.window_size+'_eff_combined.h5')
print('Extracted Features, Window Size '+args.window_size+': ' + str(X.shape))
y = pd.read_hdf('data/processed/y_'+args.n_classes+'_class_'+args.window_size+'.h5')
sub = pd.read_hdf('data/processed/subject_'+args.window_size+'.h5')
sub = sub.reset_index(drop=True)
y = y.reset_index(drop=True)

train = sub[(sub != '02_0315_ach-at') & (sub != '06_0201_ach-hex')].index
test = sub[(sub == '02_0315_ach-at') | (sub == '06_0201_ach-hex')].index

X_train, X_test, y_train, y_test = X.iloc[train,:], X.iloc[test,:], y[train], y[test]

# DO FEATURE SELECTION ON ALL TRAINING DATA FOR NOW
for i in range(int(args.n_classes), 0, -1):
    fs = FeatureSelector(multiclass=True, n_significant=i, n_jobs=18)
    fs.fit(X_train,y_train)
    X_train_filtered = fs.transform(X_train)
    print('Filtered, Features Significant for '+str(i)+' Classes: ' + str(X_train_filtered.shape))