import glob
import pandas as pd

X = pd.DataFrame()

for file in glob.glob("data/features/filtered/*_eff.h5"):
    df_features = pd.read_hdf(file)
    df_features.reset_index(inplace=True, drop=True)
    X = pd.concat([X, df_features], axis=1)

print(X.shape)
print(X.head())
X.reset_index(inplace=True)
X.to_hdf("data/achat_filtered.h5", key="features", complevel=9)