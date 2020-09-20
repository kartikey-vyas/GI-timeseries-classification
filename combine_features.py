import pandas as pd
import glob
import argparse

parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawTextHelpFormatter)
parser.add_argument('window_size', help='Number of time steps in each observation. Choose 4000, 6000 or 10000.')
args = parser.parse_args()
assert int(args.window_size) in [4000, 6000, 10000], 'window_size must be one of 4000, 6000 or 10000'

X = pd.DataFrame()

for file in glob.glob('data/features/'+args.window_size+'/*'):
    X_n = pd.read_hdf(file)
    X_n.reset_index(0, inplace=True, drop=True)
    X = pd.concat([X, X_n], axis=1)
    
X.to_hdf('data/features/ach-at-hex_'+args.window_size+'_eff_combined.h5', key='data', complevel=9)