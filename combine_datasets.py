import pandas as pd

achat = pd.read_hdf('data/processed/ach_at_6000_full.h5')
achhex = pd.read_hdf('data/processed/ach_hex_6000_full.h5')

achhex = achhex[achhex['y'] < 3]

df = pd.concat([achat,achhex])

df.to_hdf('data/processed/ach_at_combined_6000.h5')