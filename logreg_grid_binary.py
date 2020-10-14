"""This script executes a machine learning pipeline composed of the following elements:
    1. Feature Selection
    2. Quantile Transform
    3. Grid Search: Group k-fold Cross Validation with Logistic Regression
Feature selection is done through tsfresh. The filtering process uses the Mann-Whitney U test to determine statistical significance
for predicting the target. The Benjamini-Yekutieli procedure is used to account for family-wise error rate and
select only the relevant features.

Command line arguments 
----------

problem: Which binary problem to fit a model on. Choose from "base_v_drug", "base_v_at", "base_v_hex", "first_v_second", "ach_v_hex" and "at_v_hex"

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

from tsfresh.transformers import FeatureSelector

from sklearn.pipeline import Pipeline
from sklearn.model_selection import GridSearchCV, GroupKFold
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import QuantileTransformer

## PARSE COMMAND LINE ARGS ---------------------------------------------------------------------------------
parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawTextHelpFormatter)
parser.add_argument('problem', help='Which binary problem to fit a model on. Choose from "base_v_drug", "base_v_at", "base_v_hex", "first_v_second", "ach_v_hex" and "at_v_hex"')
args = parser.parse_args()

problems = ["base_v_drug", "base_v_at", "base_v_hex", "first_v_second", "ach_v_hex", "at_v_hex"]
problem = problems[int(args.problem)]

## INITIALISE LOGGING --------------------------------------------------------------------------------------
# use current time as a unique identifier
now = datetime.now()
job_id = now.strftime("%d%m%y_%H%M%S")

# create log file
logging.basicConfig(filename='logs/logreg_'+problem+'_'+job_id+'.txt',\
     level=logging.DEBUG)

## LOAD DATA --------------------------------------------------------------------------------------------
X = pd.read_hdf('data/FINAL/X_'+problem+'.h5')
y = pd.read_hdf('data/FINAL/y_'+problem+'.h5')
subject = pd.read_hdf('data/FINAL/subject_'+problem+'.h5')

# cross-validation iterator
gkf = GroupKFold(n_splits = len(subject.unique()))
gkf = list(gkf.split(X, y, subject))

# scoring
scoring = {'Accuracy': 'accuracy',
           'F1-score': 'f1_weighted'
           }
 
# define the pipeline

# DO FEATURE SELECTION ON ALL TRAINING DATA FOR NOW
fs = FeatureSelector(n_jobs=20)
fs.fit(X,y)
X_filtered = fs.transform(X)

dump(fs, 'models/FINAL/feature_selector_'+problem+'.joblib')

qt = QuantileTransformer()
clf = LogisticRegression(solver='saga', penalty='l1', max_iter=1000)
cachedir = mkdtemp()
pipeline = Pipeline(steps=[('qt', qt), ('clf', clf)], memory=cachedir)

# hyperparameters
n_quantiles = [10]
output_distribution = ['normal']
C = np.logspace(-4,4,20)

# parameter grid
param_grid = {'qt__n_quantiles': n_quantiles, 
              'qt__output_distribution': output_distribution,
              'clf__C': C}

clf_grid = GridSearchCV(pipeline,
                        param_grid=param_grid,
                        cv=gkf,
                        scoring=scoring,
                        refit='F1-score',
                        verbose=2,
                        n_jobs=20)

search = clf_grid.fit(X_filtered, y)

# Remove the cache directory
rmtree(cachedir)

dump(search, 'models/logreg_gridsearch_CV_'+problem+'.joblib')
