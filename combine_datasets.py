import pandas as pd

achat = pd.read_hdf('data/processed/ach_at_full_6000.h5')
achhex = pd.read_hdf('data/processed/ach_hex_full_6000.h5')

achhex = achhex[achhex['y'] < 3]
achhex['window_id'] += 1000

df = pd.concat([achat,achhex])

df.to_hdf('data/processed/ach_at_combined_6000.h5', key='data', complevel=9)