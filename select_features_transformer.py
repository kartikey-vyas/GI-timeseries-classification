import argparse
import pandas as pd
from src.features.feature_selection import MulticlassFeatureSelector

## INITIALISE ARGPARSER ---------------------------------------------------------------------------------
parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawTextHelpFormatter)
parser.add_argument('n_classes')
args = parser.parse_args()


X = pd.DataFrame()

for file in glob.glob("../data/features/6000/*"):
    X_n = pd.read_hdf(file)
    X_n.reset_index(0, inplace=True, drop=True)
    X = pd.concat([X, X_n], axis=1)

del X_n

y = pd.read_hdf('data/processed/y_'+str(args.n_classes)+'_class_6000.h5')

fs = MulticlassFeatureSelector()
fs.fit(X,y)
X_filt = fs.transform(X)

X_filt.to_hdf('data/features/filtered/ach-at-hex_6000_eff'+str(args.n_classes)+'_filtered.h5')