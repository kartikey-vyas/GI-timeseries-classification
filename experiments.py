# TODO 
# purpose:
#   set up grouped CV iterator
#   try numerous model parameters (gridsearchCV)
#       random forest
#   try numerous electrode subsets (take this as a command line arg using sys library)
#   save results

import pandas as pd
import numpy as np
from joblib import dump
from sklearn.model_selection import GridSearchCV, GroupKFold, RandomizedSearchCV
from sklearn.ensemble import RandomForestClassifier

X = pd.read_hdf('/data/features/filtered/filtered_0.05_.h5')
y = pd.read_hdf('/data/ach_at_combined_y.h5', key='y')
# y_bin = y.astype('category')
# y_bin = pd.get_dummies(y_bin)

# ADD SUBJECT COLUMN
s = 1
for i in range(1,6):
    X.loc[90*(i-1):90*i,'subject'] = s
    s += 1
for i in range(1,7):
    X.loc[450+(60*(i-1)):450+(60*i),'subject'] = s
    s+=1
assert not any(pd.isna(X['subject']))

train = X[X['subject'] != 4].index
test = X[X['subject'] == 4].index

X_train, X_test, y_train, y_test = X.iloc[train,:], X.iloc[test,:], y.iloc[train], y.iloc[test]

# cross-validation iterator
gkf = GroupKFold(n_splits=10)
gkf = list(gkf.split(X_train, y_train, X_train['subject']))

# hyperparameters
n_estimators = np.arange(100, 2000, 50)
max_depth = np.arange(5, 105, 10)
min_samples_split = [2, 5, 10]
min_samples_leaf = [1, 2, 4]
max_features = ['sqrt', 'log2', None]
bootstrap = [True, False]

# parameter grid
param_grid = {'n_estimators': n_estimators,
               'max_features': max_features,
               'max_depth': max_depth,
               'min_samples_split': min_samples_split,
               'min_samples_leaf': min_samples_leaf,
               'bootstrap': bootstrap}

# one vs. rest scoring
scoring = 'roc_auc_ovr_weighted'

rf = RandomForestClassifier()
rf_random = RandomizedSearchCV(estimator=rf,
param_distributions=param_grid,
n_iter=50,
cv=gkf,
verbose=2,
n_jobs=-1)

search = rf_random.fit(X_train, y_train)

dump(rf_random, 'models/rf_random_search_50_model.joblib')

results = pd.DataFrame(search)

results.to_hdf('models/rf_random_search_50_results.h5', key='data', complevel=9)
