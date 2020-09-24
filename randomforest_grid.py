"""This script executes a machine learning pipeline composed of the following elements:
    1. Feature Selection
    2. Grid Search: Group k-fold Cross Validation with Random Forest
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
from sklearn.ensemble import RandomForestClassifier
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
X = pd.read_hdf('data/features/ach-at-hex_'+args.window_size+'_eff_combined.h5')
y = pd.read_hdf('data/processed/y_'+args.n_classes+'_class_'+args.window_size+'.h5')
sub = pd.read_hdf('data/processed/subject_'+args.window_size+'.h5')
sub = sub.reset_index(drop=True)
y = y.reset_index(drop=True)

train = sub[(sub != '02_0315_ach-at') & (sub != '06_0201_ach-hex')].index
test = sub[(sub == '02_0315_ach-at') | (sub == '06_0201_ach-hex')].index

X_train, X_test, y_train, y_test = X.iloc[train,:], X.iloc[test,:], y[train], y[test]

# cross-validation iterator
gkf = GroupKFold(n_splits = len(sub[train].unique()))
gkf = list(gkf.split(X_train, y_train, sub[train]))

# scoring
scoring = {'Accuracy': 'accuracy',
           'F1-score': 'f1_weighted',
           'Precision': 'precision_weighted',
           'Recall': 'recall_weighted',
           }

# DO FEATURE SELECTION ON ALL TRAINING DATA FOR NOW
fs = FeatureSelector(multiclass=True, n_significant=int(args.n_classes))
fs.fit(X_train,y_train)
X_train_filtered = fs.transform(X_train)

# hyperparameters
n_estimators = [200, 600, 1000, 1500, 2000]
max_depth = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100, None]
min_samples_split = [2, 5, 10]
min_samples_leaf = [1, 2, 4]
max_features = ['auto', 'sqrt']
bootstrap = [True, False]

# parameter grid
param_grid = {'n_estimators': n_estimators,
               'max_features': max_features,
               'max_depth': max_depth,
               'min_samples_split': min_samples_split,
               'min_samples_leaf': min_samples_leaf,
               'bootstrap': bootstrap}

rf = RandomForestClassifier()
rf_grid = GridSearchCV(estimator=rf,
                       param_grid=param_grid,
                       cv=gkf,
                       refit='F1-score',
                       scoring=scoring,
                       verbose=2,
                       n_jobs=-1)

search = rf_grid.fit(X_train_filtered, y_train)
dump(search, 'models/rf_gridsearch_ach-at-hex_'+args.window_size+'_'+args.n_significant+'_'+args.n_classes+'_.joblib')

# TEST
X_test_filtered = fs.transform(X_test)

dump(search.best_estimator_.predict(X_test_filtered), 'models/rf_predicted_ach-at-hex_'+args.window_size+'_'+args.n_significant+'_'+args.n_classes+'_.joblib')
