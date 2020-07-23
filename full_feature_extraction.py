# TODO MODIFY THIS TO TAKE COMMAND LINE ARG (sys library)
# arg: specify what kinds of features to extract, ie minimal, efficient, full etc.

import argparse
import pandas as pd
from tsfresh import extract_features, select_features
from tsfresh.feature_extraction import MinimalFCParameters
from tsfresh.utilities.dataframe_functions import impute

# TODO fix this to apply to our function
# # COMMAND LINE ARGUMENT PARSING -------------------------------------------
# parser = argparse.ArgumentParser(description='This script runs automated feature extraction on processed MEA data')
# parser.add_argument('integers', metavar='N', type=int, nargs='+',
#                    help='an integer for the accumulator')
# parser.add_argument('--sum', dest='accumulate', action='store_const',
#                    const=sum, default=max,
#                    help='sum the integers (default: find the max)')
# # -------------------------------------------------------------------------

# Load processed dataframe
df_ach_at = pd.read_hdf("data/processed/ach_at_full.h5")

# Retrieve target variable
y = (df_ach_at[['window_id','y']]
     .drop_duplicates()
     .drop_duplicates(subset = ["window_id"])
     .set_index('window_id')
     .T
     .squeeze()
     .sort_index(0))

# Save target variable
y.to_hdf('data/features/achat_y.h5', key = 'data', complevel = 9)

# Extract features
df_ach_at = df_ach_at.drop(columns = ['y'])
X = extract_features(df_ach_at, column_id='window_id', column_sort='t', default_fc_parameters=MinimalFCParameters(),
impute_function=impute)
X.to_hdf('data/features/achat_full_min.h5', key = 'data', complevel = 9)

# look for rows in X where len == 1
# this is needed due to a quirk in the data processing functions - some of the time windows end up only including 1 step (1ms)
idx_to_remove = list(X[X['0__length'] == 1].index)
X = X.drop(idx_to_remove)
y = y.drop(idx_to_remove)

# INCLUDE IF STATEMENT (e.g. if relevant == true...)
# X_filtered = select_features(X,y)
# X_filtered.to_hdf('data/features/achat_filtered_min.h5', key = 'data', complevel = 9)