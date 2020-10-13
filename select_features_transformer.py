import argparse
import pandas as pd

from src.features.modified_feature_selector import FeatureSelector

## PARSE COMMAND LINE ARGS ---------------------------------------------------------------------------------
parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawTextHelpFormatter)
parser.add_argument('window_size', help='Number of time steps in each observation. Choose 4000, 6000 or 10000.')
parser.add_argument('n_significant', help='Number of classes for which a feature needs to be a statistically significant predictor.')
parser.add_argument('n_classes', help='Number of classes in the target variable')
args = parser.parse_args()

assert int(args.window_size) in [4000, 6000, 10000], 'window_size must be one of 4000, 6000 or 10000'
assert int(args.n_significant) <= int(args.n_classes), 'n_significant cannot exceed n_classes'

X = pd.read_hdf('data/features/ach-at_'+args.window_size+'_eff_combined.h5')
y = pd.read_hdf('data/processed/y_'+args.n_classes+'_class_'+args.window_size+'_AT.h5')

sub = pd.read_hdf('data/processed/subject_'+args.window_size+'_AT.h5')
sub = sub.reset_index(drop=True)
y = y.reset_index(drop=True)

# DO FEATURE SELECTION ON ALL TRAINING DATA FOR NOW
fs = FeatureSelector(multiclass=True, n_significant=int(args.n_classes))
fs.fit(X,y)
X_filt = fs.transform(X)

X_filt.to_hdf('data/features/filtered/ach-at_6000_eff'+'_'+args.n_significant+'_'+str(args.n_classes)+'_filtered.h5')