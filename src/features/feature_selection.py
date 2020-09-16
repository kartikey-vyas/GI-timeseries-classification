"""
This file contains methods to implement feature selection for multiclass classification problems.
It builds upon the feature selection methods in tsfresh.

Feature selection is performed through testing the influence of the feature on the target by univariate tests.
The calculated p-values are then used in multiple testing procedures (Benjamini-Yekutieli), where it is decided which
features to keep and which to discard.

Author: Kartikey Vyas
References: tsfresh - Maximilian Christ (maximilianchrist.com), Blue Yonder Gmbh, 2016
"""
import numpy as np
import pandas as pd
from statsmodels.stats.multitest import multipletests
from functools import partial, reduce

from multiprocessing import Pool

from tsfresh.feature_selection.significance_tests import target_binary_feature_real_test, \
    target_real_feature_binary_test, target_real_feature_real_test, target_binary_feature_binary_test
from tsfresh.feature_selection.relevance import calculate_relevance_table, get_feature_type, _calculate_relevance_table_for_implicit_target
from tsfresh.utilities.distribution import initialize_warnings_in_workers
from tsfresh.feature_selection import select_features

from sklearn.base import BaseEstimator, TransformerMixin

def multiclass_relevance_table(X, y, test_for_binary_target_binary_feature='fisher', 
                               test_for_binary_target_real_feature='mann', 
                               test_for_real_target_binary_feature='mann',
                               test_for_real_target_real_feature='kendall', fdr_level=0.05, 
                               hypotheses_independent=False, n_jobs=1, show_warnings=False, 
                               chunksize=None,
                               ml_task='classification'):
    """
    Extends the FRESH Algorithm to a multiclass classification problem. Keeps the features which 
    are relevant
    for predicting all target classes.
    """
    
    # can only be done for a classification problem
    if ml_task != 'classification':
        raise ValueError('ml_task must be \'classification\'')
    
    # Parallelisation
    if n_jobs == 0:
        map_function = map
    else:
        pool = Pool(processes=n_jobs, initializer=initialize_warnings_in_workers, initargs=(show_warnings,))
        map_function = partial(pool.map, chunksize=chunksize)
        
    y = y.reset_index(drop=True)
    X = X.reset_index(drop=True)
    
    # initialise relevance table
    relevance_table = pd.DataFrame(index=pd.Series(X.columns, name='feature'))
    relevance_table['feature'] = relevance_table.index
    relevance_table['type'] = pd.Series(
        map_function(get_feature_type, [X[feature] for feature in relevance_table.index]),
        index=relevance_table.index
    )
    
    # individual tables for real, binary and constant features
    table_real = relevance_table[relevance_table.type == 'real'].copy()
    table_binary = relevance_table[relevance_table.type == 'binary'].copy()
    table_const = relevance_table[relevance_table.type == 'constant'].copy()
    table_const['p_value'] = np.NaN
    table_const['relevant'] = False
    
    tables = []
    for label in y.unique():
        _test_real_feature = partial(target_binary_feature_real_test, y=(y == label),
                                     test=test_for_binary_target_real_feature)
        _test_binary_feature = partial(target_binary_feature_binary_test, y=(y == label))
        tmp = _calculate_relevance_table_for_implicit_target(
            table_real, table_binary, X, _test_real_feature, _test_binary_feature, hypotheses_independent,
            fdr_level, map_function
        )
        tmp = tmp.reset_index(drop=True)
        tmp.columns = tmp.columns.map(lambda x : x+'_'+str(label) if x !='feature' and x!='type' else x)

        tables.append(tmp)

    relevance_table = reduce(lambda  left,right: pd.merge(left,right,on=['feature','type'],
                                                how='outer'), tables)
    relevance_table['n_significant'] = relevance_table.filter(regex='^relevant_', axis=1).sum(axis=1)
    relevance_table['relevant'] = np.where(relevance_table['n_significant'] >= len(y.unique()), True, False)
    relevance_table.index = relevance_table['feature']
    
    return relevance_table

class MulticlassFeatureSelector(BaseEstimator, TransformerMixin):
    """
    Sklearn-compatible estimator, for reducing the number of features in a dataset to only those,
    that are relevant and significant to a given target. This code has been adapted from tsfresh and extended
    for multiclass classification problems.
    """

    def __init__(self, test_for_binary_target_binary_feature='fisher',
                 test_for_binary_target_real_feature='mann', test_for_real_target_binary_feature='mann', 
                 test_for_real_target_real_feature='kendall', fdr_level=0.05, hypotheses_independent=False, 
                 n_jobs=1, show_warnings=False, chunksize=None, ml_task='classification'):
        """
        Create a new FeatureSelector instance.
        """
        self.relevant_features = None
        self.p_values = None
        self.features = None

        self.test_for_binary_target_binary_feature = test_for_binary_target_binary_feature
        self.test_for_binary_target_real_feature = test_for_binary_target_real_feature
        self.test_for_real_target_binary_feature = test_for_real_target_binary_feature
        self.test_for_real_target_real_feature = test_for_real_target_real_feature

        self.fdr_level = fdr_level
        self.hypotheses_independent = hypotheses_independent

        self.n_jobs = n_jobs
        self.chunksize = chunksize
        self.ml_task = ml_task
        
    def fit(self, X, y):
        """
        Extract the information, which of the features are relevant for all classes using the given target.
        """
        if not isinstance(X, pd.DataFrame):
            X = pd.DataFrame(X.copy())

        if not isinstance(y, pd.Series):
            y = pd.Series(y.copy())

        relevance_table = multiclass_relevance_table(
            X, y, ml_task=self.ml_task, n_jobs=self.n_jobs,
            chunksize=self.chunksize, fdr_level=self.fdr_level,
            hypotheses_independent=self.hypotheses_independent,
            test_for_binary_target_real_feature=self.test_for_binary_target_real_feature)
        
        self.relevant_features = relevance_table.loc[relevance_table.relevant].feature.tolist()
        self.p_values = relevance_table.filter(regex='^p_value_*', axis=1)
        self.features = relevance_table.index.tolist()

        return self
    
    def transform(self, X):
        """
        Delete all features, which were not relevant in the fit phase.
        """
        if self.relevant_features is None:
            raise RuntimeError("You have to call fit before.")

        if isinstance(X, pd.DataFrame):
            return X.copy().loc[:, self.relevant_features]
        else:
            return X[:, self.relevant_features]