"""This script executes a machine learning pipeline composed of the following elements:
    1. Feature Selection
    2. Quantile Transform
    3. Grid Search: Group k-fold Cross Validation with Logistic Regression
Feature selection is done through a local branch of tsfresh, which has been modified to handle multiclass
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
import logging
import os
import time
from datetime import datetime
from joblib import dump
from tempfile import mkdtemp
from shutil import rmtree

import pandas as pd
import numpy as np

from src.features.modified_feature_selector import FeatureSelector

from sklearn.pipeline import Pipeline
from sklearn.model_selection import GridSearchCV, GroupKFold
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import QuantileTransformer

## PARSE COMMAND LINE ARGS ---------------------------------------------------------------------------------
parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawTextHelpFormatter)
parser.add_argument('window_size', help='Number of time steps in each observation. Choose 4000, 6000 or 10000.')
parser.add_argument('n_significant', help='Number of classes for which a feature needs to be a statistically significant predictor.')
parser.add_argument('n_classes', help='Number of classes in the target variable')
args = parser.parse_args()

assert int(args.window_size) in [4000, 6000, 10000], 'window_size must be one of 4000, 6000 or 10000'
assert int(args.n_significant) <= int(args.n_classes), 'n_significant cannot exceed n_classes'

## INITIALISE LOGGING --------------------------------------------------------------------------------------
# use current time as a unique identifier
now = datetime.now()
job_id = now.strftime("%d%m%y_%H%M%S")

# create log file
logging.basicConfig(filename='logs/logreg_pipeline_'+args.window_size+'_'+args.n_significant+'_'+args.n_classes+'_'+job_id+'.txt',\
     level=logging.DEBUG)

## LOAD DATA --------------------------------------------------------------------------------------------
X = pd.read_hdf('data/features/ach-at_'+args.window_size+'_eff_combined.h5')
y = pd.read_hdf('data/processed/y_'+args.n_classes+'_class_'+args.window_size+'_AT.h5')
sub = pd.read_hdf('data/processed/subject_'+args.window_size+'_AT.h5')
X = X.reset_index(drop=True)
sub = sub.reset_index(drop=True)
y = y.reset_index(drop=True)

# train = sub[(sub != '02_0315_ach-at') & (sub != '06_0201_ach-hex')].index
# test = sub[(sub == '02_0315_ach-at') | (sub == '06_0201_ach-hex')].index

# X_train, X_test, y_train, y_test = X.iloc[train,:], X.iloc[test,:], y[train], y[test]

# cross-validation iterator
gkf = GroupKFold(n_splits = len(sub.unique()))
gkf = list(gkf.split(X, y, sub))

# scoring
scoring = {'Accuracy': 'accuracy',
           'F1-score': 'f1_weighted'
           }
 
# define the pipeline

# DO FEATURE SELECTION ON ALL TRAINING DATA FOR NOW
fs = FeatureSelector(multiclass=True, n_significant=int(args.n_classes), n_jobs=18)
fs.fit(X,y)
X_filtered = fs.transform(X)

qt = QuantileTransformer()
clf = LogisticRegression(multi_class='multinomial')
cachedir = mkdtemp()
pipeline = Pipeline(steps=[('qt', qt), ('clf', clf)], memory=cachedir)

# hyperparameters
n_quantiles = [10]
output_distribution = ['normal']
penalty = ['l1']
C = np.logspace(-4,4,20)

# parameter grid
param_grid = {'qt__n_quantiles': n_quantiles, 
              'qt__output_distribution': output_distribution,
              'clf__penalty' : penalty,
              'clf__solver' : ['saga'],
              'clf__C': C,
              'clf__max_iter': [1000]}

clf_grid = GridSearchCV(pipeline,
                        param_grid=param_grid,
                        cv=gkf,
                        scoring=scoring,
                        refit='F1-score',
                        verbose=2,
                        n_jobs=18)

search = clf_grid.fit(X_filtered, y)

# Remove the cache directory
rmtree(cachedir)

dump(search, 'models/logreg_gridsearch_CV_ach-at_'+args.window_size+'_'+args.n_significant+'_'+args.n_classes+'.joblib')

# # TEST
# X_test_filtered = fs.transform(X_test)

# dump(search.best_estimator_.predict(X_test_filtered), 'models/logreg_predicted_ach-at_'+args.window_size+'_'+args.n_significant+'_'+args.n_classes+'.joblib')
