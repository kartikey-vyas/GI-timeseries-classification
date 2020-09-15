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
    # combine the MEA data into one data frame
    data = pd.DataFrame(matfile['filt_data'])
    df_ts = data.T
    
    # create id for each discrete window
    win = 1
    ids = pd.DataFrame(index=df_ts.index)
    for i in range(0,len(df_ts),window_size):
        ids.loc[i:i+window_size,'id'] = win
        win += 1
    
    df_ts.insert(0, 'id', ids)

    return df_ts

def load_MEA_data(folder = "data/raw/Ach-AT-Hex"):
    """ This function retrieves a list of file paths of MEA data

        Arguments
        ---------
        folder: specifies the root folder from where to load the data
                default = "data/raw/Ach-AT"
        
        Returns
        -------
        list of files in specified folder

    """
    d = folder
    filenames = []
    
    # get all the paths of the files to be loaded in
    for root, _unused, files in os.walk(d):
        for file in files:
            if file.endswith(".mat"):
                filenames.append(os.path.join(root, file))

    return sorted(filenames)
    

def label_MEA_data(filenames, window_size = 6000):
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
                    
        Returns
        -------
        dataset: DataFrame containing 'time', 'window_id', electrode readings
            numbered 0-59 and target variable 'y'
    """
    last_win = 0
    dataset = pd.DataFrame()
    
    print('Creating data set with discrete time windows of size: '+str(window_size))
    
    for file in filenames:
        matfile = loadmat(file)
        f_name = os.path.split(file)[1]
        f_name = f_name[:-4]
        
        df_subject = make_windows(matfile, window_size)
        df_subject['id'] += last_win
        df_subject['subject'] = f_name
        
        last_win = df_subject['id'].tail(1).values[0]
        print('Total Distinct Samples: '+str(last_win))
        
        # determine which label needs to be applied
        if f_name.endswith("0"):
            # baseline
            df_subject['y'] = 0
        elif f_name.endswith("1"):
            # Ach applied
            df_subject['y'] = 1
        elif f_name.endswith("at_2"):
            # AT applied after Ach
            df_subject['y'] = 2
        elif f_name.endswith("hex_2"):
            # Hex applied after Ach
            df_subject['y'] = 3
        
        dataset = dataset.append(df_subject)
        print('Subject Added: '+f_name)
            
    return dataset.reset_index(drop=True)

def generate_dataset(name, folder, window_size):
    files = load_MEA_data(folder=folder)
    dataset = label_MEA_data(files, window_size=window_size)
    dataset.to_hdf('data/processed/'+str(name)+'_'+str(window_size)+'.h5', key='data', complevel=9)