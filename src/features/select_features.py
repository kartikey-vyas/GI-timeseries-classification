"""
This file contains methods to implement feature selection for multiclass classification problems.
It builds upon the feature selection methods in tsfresh.

Feature selection is performed through testing the influence of the feature on the target by univariate tests.
The calculated p-values are then used in multiple testing procedures (Benjamini-Yekutieli), where it is decided which
features to keep and which to discard.

Author: Kartikey Vyas
"""

import numpy as np
import pandas as pd
from statsmodels.stats.multitest import multipletests
from tsfresh.feature_selection.significance_tests import target_binary_feature_real_test, \
    target_real_feature_binary_test, target_real_feature_real_test, target_binary_feature_binary_test
from tsfresh.feature_selection.relevance import calculate_relevance_table

def select_features_multiclass():
    pass
