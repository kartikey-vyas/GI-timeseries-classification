import pandas as pd
import numpy as np

df_ach_at = pd.read_hdf("data/processed/ach_at_full.h5")

cols = ['t', 'window_id', 15, 14, 13, 4, 57, 48, 47, 46, 'y']
df = df_ach_at[cols]

df_diffs = (df[[15, 14, 13, 4, 57, 48, 47, 46]]
    .diff(axis=1)
    .add_suffix("_diff")
    .drop(columns = ['15_diff']))

df = pd.concat([df,df_diffs], axis=1)

df.to_hdf("ach_at_middle_diffs", key = "data", complevel=9)
