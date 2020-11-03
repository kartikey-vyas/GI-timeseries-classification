import pandas as pd
import glob

X = pd.DataFrame()

for file in glob.glob('data/features/6000/*'):
    X_n = pd.read_hdf(file)
    X_n.reset_index(0, inplace=True, drop=True)
    X = pd.concat([X, X_n], axis=1)
    
X.to_hdf('data/features/ach-at-hex_6000_eff_combined.h5', key='data', complevel=9)