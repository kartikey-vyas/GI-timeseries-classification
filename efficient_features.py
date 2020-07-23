import pandas as pd
from tsfresh import extract_features, select_features
from tsfresh.feature_extraction import EfficientFCParameters
from tsfresh.utilities.dataframe_functions import impute
import argparse

# COMMAND LINE ARGUMENT PARSING -------------------------------------------
parser = argparse.ArgumentParser(description='This script runs automated feature extraction on processed MEA data')
parser.add_argument('filename')
parser.add_argument('data')
args = parser.parse_args()
# -------------------------------------------------------------------------

# Load processed dataframe
fpath = "data/processed/" + args.filename
df_ach_at = pd.read_hdf(fpath)

# Retrieve target variable
y = (df_ach_at[['window_id','y']]
     .drop_duplicates()
     .drop_duplicates(subset = ["window_id"])
     .set_index('window_id')
     .T
     .squeeze()
     .sort_index(0))

# Extract features
df_ach_at = df_ach_at.drop(columns = ['y'])
X = extract_features(df_ach_at, column_id='window_id', column_sort='t', default_fc_parameters=EfficientFCParameters(),
impute_function=impute)


# look for rows in X where len == 1
# this is needed due to a quirk in the data processing functions - some of the time windows end up only including 1 step (1ms)
idx_to_remove = list(X[X['0__length'] == 1].index)
X = X.drop(idx_to_remove)
y = y.drop(idx_to_remove)

# Save target variable
y.to_hdf('data/features/achat_y.h5', key = 'data', complevel = 9)

# Save design matrix
X.to_hdf('data/features/achat_'+args.data+'_eff.h5', key = 'data', complevel = 9)