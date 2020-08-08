import argparse
import logging
from datetime import datetime
import pandas as pd
from tsfresh import extract_features
from tsfresh.feature_extraction import EfficientFCParameters
from tsfresh.utilities.dataframe_functions import impute

## PARSE COMMAND LINE ARGS ---------------------------------------------------------------------------------
parser = argparse.ArgumentParser(description='This script runs automated feature extraction on processed MEA data')
parser.add_argument('filename')
parser.add_argument('electrode')
args = parser.parse_args()

## INITIALISE LOGGING --------------------------------------------------------------------------------------
# use current time as a unique identifier
now = datetime.now()
job_id = now.strftime("%d%m%y_%H%M%S")
# create logfile
logging.basicConfig(filename='logs/feature_extraction/feature_extraction_'+args.electrode+'_'+job_id,level=logging.DEBUG)

if int(args.electrode) not in range(1,60):
    logging.error("Invalid electrode selected - terminating script")
    exit()

## for now, load the full data frame, retrieve the relevant columns and then delete the full df from memory
## it would probably be faster to generate 60 dataframes and access the desired one...
# access complete dataset hdf file
fpath = "data/processed/" + args.filename
df_ach_at = pd.read_hdf(fpath)

logging.info("loaded dataframe")

# select relevant columns
col = int(args.electrode)
df = df_ach_at[['t', 'window_id', col]]

# remove full dataset from memory
df_ach_at = None
del df_ach_at

logging.info("beginning feature extraction")
# begin feature extraction
X = extract_features(df, column_id='window_id', column_sort='t', default_fc_parameters=EfficientFCParameters(),
impute_function=impute)
logging.info("feature extraction complete, ")

# save design matrix
X.to_hdf('data/features/achat_'+args.electrode+'_eff.h5', key = 'data', complevel = 9)
logging.info("features saved to 'data/features/achat_"+args.electrode+"_eff.h5'")