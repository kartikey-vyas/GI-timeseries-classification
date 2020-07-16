# Generate full data set for Ach-AT (all subjects)
from src.data.load_data import load_MEA_data, label_MEA_data

# load from the Ach-AT folder
ach_at = load_MEA_data(folder = "data/raw/Ach-AT")
label_MEA_data(ach_at, 'ach_at_full')

# TODO include a 'subject' column either here or in the feature matrix. This will be used to build the grouped CV iterator.

# NEXT SCRIPT -> full_feature_extraction.py