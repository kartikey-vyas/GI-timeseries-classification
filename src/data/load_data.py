# This file contains functions that assist with converting the MEA signals to the correct format for feature extraction
# 
#
# Author: Kartikey Vyas

# imports
import os
from scipy.io import loadmat
import numpy as np
import pandas as pd

def make_windows(matfile, window_size = 6000):
    """ This function creates a dataframe with discrete time windows from the raw MEA signals.
        Signals begin as .mat files

        Parameters
        ----------
        matfile: dict that is the output of loadmat() from scipy.io
                
        window_size: number of rows per window
                default = 6000
                    6 second windows. Chosen based on average cpm of GI slow waves
        
        Returns
        -------
        df: DataFrame with columns 'time', 'window_id' and electrode numbers
         
    """
    # retrieve the relevant data from the dictionaries
    df = pd.DataFrame(matfile['filt_data'].copy())
    df = df.T
    time = pd.DataFrame(matfile['filt_t'].copy())
    time = time.T

    # set up the time column
    time.columns = ['t']
    time['t'] = time['t'] - 60000 # make time start at 0
    time['window_id'] = time['t'] / window_size # n second windows
    time['window_id'] = time['window_id'].astype(int)

    # join the electrode signals with time
    df = pd.concat([time, df], axis=1)

    return df

def load_MEA_data(folder = "data/raw/Ach-AT"):
    """ This function retrieves a list of file paths of MEA data

        Arguments
        ---------
        folder: specifies the root folder from where to load the data
                default = "data/raw/Ach-AT"

    """
    d = folder
    filenames = []

    # get all the paths of the files to be loaded in
    for root, dirs, files in os.walk(d):
        for file in files:
            if file.endswith(".mat"):
                filenames.append(os.path.join(root, file))
    
    return sorted(filenames)
    

def label_MEA_data(filenames, output, window_size = 6000):
    """ This function creates a labelled dataset of MEA signals.
        The MEA data must be in .mat files. The dataset is discretised into time windows.

        Arguments
        ---------
        filenames: list of strings, file paths of the MEA .mat files
        
        window_size: int number of rows per window
            default = 6000
                6 second windows. Chosen based on average cpm of GI slow waves
                    
        cols: list of column names to include in the processed dataset
            for the MEA problem, this refers to the electrode numbers to include 
            time and window_id are always included
            default = 'all'
                includes every column
                    
        output: string name of .h5 file to save dataset as. Do not include file extension
            or root folder
                    
        Returns
        -------
        dataset: DataFrame containing 'time', 'window_id', electrode readings
            numbered 0-59 and target variable 'y'
    """
    # initialise name of previous file accessed
    prev_name = filenames[0]
    prev_name = os.path.split(prev_name)[1]
    prev_name = prev_name[:-4]
    
    subject = 0
    
    dataset = pd.DataFrame()
    
    for file in filenames:
        matfile = loadmat(file)
        f_name = os.path.split(file)[1]
        f_name = f_name[:-4]
        
        # check if subject number has changed
        if f_name[:-6] != prev_name[:-6]:
            subject += 1
        
        # df['subject'] = subject
        # df['subject'] = df['subject'].astype('category')
        
        # increment time by a fixed amount per subject, that exceeds
        # the max time value for a single subject
        matfile['filt_t'] += 900000*subject
        
        df = make_windows(matfile, window_size)
        df['subject'] = f_name
        
        # determine which label needs to be applied
        if f_name.endswith("0"):
            # baseline
            df['y'] = 0
        elif f_name.endswith("at_1"):
            # Ach applied
            df['y'] = 1
        elif f_name.endswith("at_2"):
            # AT applied after Ach
            df['y'] = 2
        elif f_name.endswith("hex_2"):
            # Hex applied after Ach
            df['y'] = 3
        
        dataset = dataset.append(df)
        
        # update previous name
        prev_name = f_name

#     if cols == "all":
#         pass
#     else:
#         columns = ['t','window_id']
#         columns = columns+cols
#         dataset = dataset[columns]
    
    dataset.to_hdf('data/processed/'+output+'.h5', key = 'data', complevel = 9)

def OLD_load_MEA_data(folder = "data/raw",method = "means"):
    """ This function loads the raw data from .mat files.
        All raw data must be placed in data/raw

        Arguments
        ---------
        folder: specifies the root folder where the data to be loaded will be put
                default = "data/raw"
                
        method: specifies how to process the data before exporting it. 
                default = "means" 
                    only keeps the mean signal for each MEA
    """
    d = folder
    filenames = []

    # get all the paths of the files to be loaded in
    for root, dirs, files in os.walk(d):
        for file in files:
            if file.endswith(".mat"):
                filenames.append(os.path.join(root, file))

    # initialise time vectors
    t0 = {'time': np.arange(60001, 240001, 1)}
    t1 = {'time': np.arange(420001, 600001, 1)}
    t2 = {'time': np.arange(780001, 960001, 1)}

    # set up dataframes to add the values into
    # baseline (0), first drug administered (1), second drug administered (2)

    df_baseline = pd.DataFrame(t0)
    df_first = pd.DataFrame(t1)
    df_second = pd.DataFrame(t2)

    for file in filenames:
        matfile = loadmat(file)
        MEA_data = pd.DataFrame(matfile['filt_data'])
        if method == "means":
            MEA_data = pd.DataFrame(MEA_data.mean(axis=0))
            # the name of the file will be the column header
            colname = os.path.split(file)[1]
            colname = colname[:-4]
            MEA_data.columns = [colname]
        elif method == "all":
            pass
        
        # concatenate appropriate dataframe
        if colname.endswith("0"):
            df_baseline = pd.concat([df_baseline, MEA_data], axis=1)
        elif colname.endswith("1"):
            df_first = pd.concat([df_first, MEA_data], axis=1)
        else:
            df_second = pd.concat([df_second, MEA_data], axis=1)

    # export to csv
    export_path = "data/interim/"
    if method == "means":
        ext = "_means.csv"
    
    df_baseline.to_csv(export_path+"baseline"+ext)
    df_first.to_csv(export_path+"first"+ext)
    df_second.to_csv(export_path+"second"+ext)