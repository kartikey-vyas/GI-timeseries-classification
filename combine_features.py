import glob
import pandas as pd

X = pd.DataFrame()

for file in glob.glob("data/features/filtered/*_eff.h5"):
    df_features = pd.read_hdf(file)
    df_features.reset_index(inplace=True, drop=True)
    X = pd.concat([X, df_features], axis=1)


# add subject column to use in grouped CV iterator
subject = 0
for i in range(1,6):
    X.loc[(i-1)*90:i*90, 'subject'] = subject
    subject += 1
X.reset_index(inplace=True, drop=True)

print(X.shape)
print(X.head())
X.to_hdf("data/achat_filtered.h5", key="features", complevel=9)
