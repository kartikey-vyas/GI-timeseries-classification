"""This script executes a machine learning pipeline composed of the following elements:
    1. Feature Selection
    2. Grid Search: Group k-fold Cross Validation with Random Forest
Feature selection is done through a local branch of tsfresh, which has been modified to handle multiclass
classification problems. The filtering process uses the Mann-Whitney U test to determine statistical significance
for predicting the target. The Benjamini-Yekutieli procedure is used to account for family-wise error rate and
select only the relevant features.

Command line arguments 
----------

problem: Which multiclass problem to fit a model on. Choose from "all", "base_v_ach_v_at", "base_v_ach_v_hex", "base_v_ach_v_drug2"

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

import pandas as pd
import numpy as np

from src.features.modified_feature_selector import FeatureSelector

from sklearn.pipeline import Pipeline
from sklearn.model_selection import GridSearchCV, GroupKFold
from sklearn.ensemble import RandomForestClassifier

## PARSE COMMAND LINE ARGS ---------------------------------------------------------------------------------
parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawTextHelpFormatter)
parser.add_argument('problem', help='Which multiclass problem to fit a model on. Choose from "all", "base_v_ach_v_at", "base_v_ach_v_hex", "base_v_ach_v_drug2"')
args = parser.parse_args()

problems = ["all", "base_v_ach_v_at", "base_v_ach_v_hex", "base_v_ach_v_drug2"]
problem = problems[int(args.problem)]

## INITIALISE LOGGING --------------------------------------------------------------------------------------
# use current time as a unique identifier
now = datetime.now()
job_id = now.strftime("%d%m%y_%H%M%S")

# create log file
logging.basicConfig(filename='logs/logreg_pipeline_'+args.window_size+'_'+args.n_significant+'_'+args.n_classes+'_'+job_id+'.txt',\
     level=logging.DEBUG)

## LOAD DATA --------------------------------------------------------------------------------------------
if problem in ["all", "base_v_ach_v_drug2"]:
    X = pd.read_hdf('data/FINAL/X_all.h5')
else:
    X = pd.read_hdf('data/FINAL/X_'+problem+'.h5')

y = pd.read_hdf('data/FINAL/y_'+problem+'.h5')
sub = pd.read_hdf('data/FINAL/subject_'+problem+'.h5')
X = X.reset_index(drop=True)
sub = sub.reset_index(drop=True)
y = y.reset_index(drop=True)


# cross-validation iterator
gkf = GroupKFold(n_splits = len(sub.unique()))
gkf = list(gkf.split(X, y, sub))

# scoring
scoring = {'Accuracy': 'accuracy',
           'F1-score': 'f1_weighted'
           }
 
# define the pipeline

# DO FEATURE SELECTION ON ALL TRAINING DATA FOR NOW
fs = FeatureSelector(multiclass=True, n_significant=int(args.n_significant), n_jobs=32)
fs.fit(X,y)
X_filtered = fs.transform(X)

dump(fs, 'models/FINAL/feature_selector_'+problem+'_.joblib')

# hyperparameters
n_estimators = [100, 500, 1000]
max_depth = [1, 2, 5, 10, 15, None]
# min_samples_split = [2, 5, 10]
# min_samples_leaf = [1, 2, 4]
# max_features = ['log2', 'sqrt']
# bootstrap = [True, False]

# parameter grid
param_grid = {'n_estimators': n_estimators,
               'max_depth': max_depth}

rf = RandomForestClassifier()
rf_grid = GridSearchCV(estimator=rf,
                       param_grid=param_grid,
                       cv=gkf,
                       refit='Accuracy',
                       scoring=scoring,
                       verbose=2,
                       n_jobs=32)

search = rf_grid.fit(X_filtered, y)
dump(search, 'models/FINAL/rf_gridsearch_CV_'+problem+'_.joblib')
