import pandas as pd
from tsfresh import extract_features, select_features
from tsfresh.feature_extraction import MinimalFCParameters
from tsfresh.utilities.dataframe_functions import impute

df_ach_at = pd.read_hdf("data/processed/ach_at_full.h5")
y = (df_ach_at[['window_id','y']]
     .drop_duplicates()
     .set_index('window_id')
     .T
     .squeeze())

df_ach_at.drop(columns = ['y'])
X = extract_features(df_ach_at, column_id='window_id', column_sort='t', default_fc_parameters=MinimalFCParameters(),
impute_function=impute)
X.to_hdf('data/features/achat_full_min.h5', key = 'data', complevel = 9)

X_filtered = select_features(X, y)
X_filtered.to_hdf('data/features/achat_filtered_min.h5', key = 'data', complevel = 9)