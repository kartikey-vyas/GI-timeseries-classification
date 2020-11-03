Kartikey Vyas Part IV Project 2020 - Research Compendium
========================================================

>*Understanding the spatiotemporal organisation of GI bioelectrical activity at the microscale*

This project aims to build a machine learning framework to classify bioelectrical signals, using automated time series feature extraction.

Supervisors:
- Dr. Peng Du
- Dr. Andreas Kempa-Liehr

### Project Organization
------------
    ├── README.md          <- The top-level README for developers using this project.
    ├── data
    │   ├── FINAL          <- The final, canonical data sets for modeling.
    │   ├── processed      <- Intermediate data that has been transformed.
    │   ├── features       <- Extracted features.
    │   |   └── 6000       <- Features extracted from processed data set with windows of size 6000.
    │   └── raw            <- The original, immutable data dump.
    │
    ├── models             <- Trained and serialized models, model predictions, or model summaries
    ├── slurm              <- Slurm scripts to run python jobs on the NeSI HPC Cluster
    ├── notebooks          <- Jupyter notebooks. Naming convention is a number (for ordering),
    │                         the creator's initials, and a short `-` delimited description, e.g.
    │                         `1.0-jqp-initial-data-exploration`.
    ├── project-logs       <- Logs of project progress and explanations of choice of methods.
    ├── reports            <- Generated analysis as HTML, PDF, LaTeX, etc.
    │   └── figures        <- Generated graphics and figures to be used in reporting
    ├── environment.yml    <- The environment file for reproducing the analysis environment, e.g.
    │                         generated with `conda env export > environment.yml`
    ├── setup.py           <- makes project pip installable (pip install -e .) so src can be imported
    ├── src                <- Source code for use in this project.
       ├── __init__.py    <- Makes src a Python module
       ├── data           <- Scripts to generate data
       ├── features       <- Scripts to turn raw data into features for modeling  
       ├── models         <- Scripts to train and evaluate models


--------
## Abstract
The treatment and diagnosis of gastrointestinal (GI) motility disorders remains a significant and costly problem for current clinical practice. GI motility is driven by the rhythmic
contraction and relaxation of smooth muscles. This phenomenon is governed by bioelectrical
activity known as slow waves. Dysrhythmia and abnormalities in slow waves are
often the cause behind GI motility disorders and are treated with certain drugs. The effect
of these drugs on the spatiotemporal propagation of slow waves is not well characterised.
The main aim of this project was to explore the applications of machine learing (ML)
on this problem. The available data consisted of GI slow wave potentials recorded from
a 60 electrode Micro-electrode Array (MEA). Automated times series feature extraction
and selection, implemented through the FRESH (FeaturRe Extraction based on Scalable
Hypothesis tests) algorithm, was conducted. It was found that classifiers could reliably
predict whether a subject was administered Atropine (AT) or Hexamethonium (Hex) subsequent
to the administering of ACh (Acetylcholine). The most important features were
explored. GI slow waves from subjects under the effect of AT consistently had higher
values for each of the most important features indicating that AT has an excitatory effect
on pacemaker potentials when administered after ACh, while Hex does not. For example,
AT influenced slow waves had higher frequency and noise levels, on average containing
4 to 10 peaks for every 6 second recording, while Hex infl
uenced slow waves had only
up to 3 peaks for the same length of recording. Overall, a systematic framework has
been established for characterising GI slow waves through machine learning that avoids
laborious feature engineering.


## Setup
Make sure some form of Anaconda and Python (3.8+) are installed.

Create the virtual environment for this project with:  
`conda env create -f environment.yml`


### Raw Data
The raw data consists of 33 `.mat` files containing MATLAB cell arrays. Within these, there are two arrays, namely `filt_data` and `filt_t`, which contain the electrode readings from the MEA. The naming convention of these files are as follows:

`00_0315_ach-at_0.mat`
- `00_0315` = subject number
- `ach-at` = first drug applied was ACh, second drug was AT
- `_0.mat` = baseline recording, `_1.mat` = first drug, `_2.mat` = second drug

Data has not been stored on GitHub due to size. Please enquire with Dr. Peng Du for access to the raw data.

## Execution

### Sripts
Scripts have been organised into folders in `src` according to their function. **When running scripts, make sure they are moved to the root directory first.**

Here is the order in which scripts should be run to generate features:
1. `make_dataset.py`
2. `extract_features.py`
3. `combine_features.py`

Next, one of the scripts from `models` can be run, e.g. `randomforest_grid_multiclass.py`

### HPC
Due to the high computational cost and memory requirements of some of the scripts, much of the computation was done on the NeSI HPC Cluster (Mahuika). As such, the folder `slurm` contains Slurm scripts that create jobs that can be executed on the cluster. To submit jobs on the cluster, first commit any new code to this repo. Next, use `submit_jobs.sh` to choose a slurm script to execute.

### Notebooks
Several insights and visualisations were produced from iPython/Jupyter notebooks. The following notebooks are very important for producing the final results:
- `9.0-kv-randomforest.ipynb`
- `9.5-kv-exploration.ipynb`

### Multiclass + tsfresh
This repo contains an implementation of multiclass feature selection incorporated into the `tsfresh` library. The python scripts `modified_feature_selection.py` and `modified_feature_selector.py` contain local implementations of this code and are called in other functions as submodules of `src.features`. As of the 28th of October, the proposed multiclass feature selection method from this project has been accepted and merged into `tsfresh`.

### Manual Multiclass
The first multiclass feature selection implementation used the Mann-Whitney U test and Benjamini-Yekutieli procedure separately to first extract p-values and then correct for false discovery rate. This can be done through the scripts `hypothesis_tests.py` and `select_features_b-y.py`.
