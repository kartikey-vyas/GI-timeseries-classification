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
    
    return filenames
    

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
        if f_name[:-6] == prev_name[:-6]:
            subject += 1
        
        # increment time by a fixed amount per subject, that exceeds
        # the max time value for a single subject
        matfile['filt_t'] += 900000*subject
        
        df = make_windows(matfile, window_size)
        
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