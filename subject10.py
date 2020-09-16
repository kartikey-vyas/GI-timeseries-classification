import pandas as pd
import numpy as np

df = pd.read_hdf('data/processed/ach_at_hex_10000.h5')
subject = (df[['id','subject']]
           .drop_duplicates('id')
           .set_index('id')
           .T
           .squeeze()
           .sort_index(0))
subject = subject.str.slice(stop=-2)
subject.to_hdf('data/processed/subject_10000.h5', key='data', complevel=9)