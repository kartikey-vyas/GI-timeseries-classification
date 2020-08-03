# Kartikey's Log

This is document will serve as a progress log for my part 4 project. It is written in markdown.

- [Kartikey's Log](#kartikeys-log)
  - [Setting up a development environment](#setting-up-a-development-environment)
    - [Technologies Used](#technologies-used)
    - [Workflow](#workflow)
  - [Progress Log](#progress-log)
    - [Semester 1](#semester-1)
      - [Week 2](#week-2)
      - [Week 3](#week-3)
      - [Week 4 (Teaching-free week)](#week-4-teaching-free-week)
      - [Week 5](#week-5)
      - [Week 6](#week-6)
      - [Midsemseter Break Week 1](#midsemseter-break-week-1)
      - [Midsemester Break Week 2](#midsemester-break-week-2)
    - [COVID-19 LEVEL 2](#covid-19-level-2)
      - [Literature Review Feedback](#literature-review-feedback)
      - [Vivek's initial advice](#viveks-initial-advice)
      - [ML Meeting with Andreas](#ml-meeting-with-andreas)
      - [Friday 12 June Meeting](#friday-12-june-meeting)
      - [Thursday 25 June](#thursday-25-june)
    - [Intersem Break](#intersem-break)
      - [Thursday 9 July](#thursday-9-july)
    - [Semester 2](#semester-2)
      - [Week 1 Meeting](#week-1-meeting)
  - [*script descriptions*](#script-descriptions)

## Setting up a development environment

Since I am working from a Windows 10 PC, I decided to use a Linux distribution that I run natively on windows through the Windows Subsystem for Linux (WSL 2). This contains a linux kernel that runs alongside windows - it is like a lightweight VM.

### Technologies Used

- WSL 2 - Windows Subsystem for Linux
  - Ubuntu 18.04 LTS
- Installed miniconda on ubuntu
  - conda 4.8.2
  - python 3.7.4
  - jupyter core 4.6.1
  - jupyter-notebook 6.0.3
- Git for version control
  - github repo: <https://github.com/kartikey-vyas/engsci700-project37>
- Windows Terminal >_
- VS Code
  - VS Code Remote (connects to WSL Ubuntu)
  - GitLens
- Cookie Cutter Data Science template

### Workflow

1. Open windows terminal. This will automatically start Ubuntu 18.04 running on WSL 2.
2. `cd code/p4p && code .` to open project folder in VS Code.
3. open jupyter notebooks/scripts in VS Code.

This set up will be used going forward from 13/03.

## Progress Log

### Semester 1
#### Week 2

##### Friday 13<sup>th</sup> March <!-- omit in toc -->

- Meeting with Peng (see meeting minutes)
- Organise time to see Andreas after reading time-series docs and getting started with `tsfresh`
- Continue literature review, start with the MEA documents sent by Peng.

#### Week 3

##### Monday 16<sup>th</sup> March <!-- omit in toc -->

- adapted [progress.md](progress.md) to contain summaries of all of the readings that we complete.
- read Geron (2017) chapters 1 and 2, completed summary.

##### Tuesday 17<sup>th</sup> March <!-- omit in toc -->

- Downloaded and installed Python KOANS
- going to commit some time everyday to work through KOANS and improve python skills

##### Thursday 18<sup>th</sup> March <!-- omit in toc -->

- fixed some of the markdown linting issues by creating [.markdownlint.json](.markdownlint.json) in the project-logs directory.
  - if theres an annoying rule that keeps causing unnecessary warnings in your markdown file, add the rule name followed by false to the json file. e.g. `MD032 = false`

##### Friday 19<sup>th</sup> March <!-- omit in toc -->

- Meeting with Peng and Andreas
- continued python koans

#### Week 4 (Teaching-free week)

##### Wednesday 25<sup>th</sup> <!-- omit in toc -->

- Watched literature review workshop video
- starting time-series readings
  - read Nielsen chapter 1 and chapter 8

##### Thursday 26<sup>th</sup> March <!-- omit in toc -->

- completed ch8 nielsen
- starting tsfresh readings

**Ideas for progressing in the next two weeks**
- Building my ML environment
  - Where is data stored? s3/cloud somewhere? *google drive, consider transferring to s3*
  - Where are am I running my code?
    - VM? - *Ubuntu 18.04 on WSL 2 on windows 10*
    - What code version? *Python 3.7*
- How do I track my performance?
  - What features being experimented?
  - What accuracy measure?
  - What algorithm?
    - What algorihtm parameters?
- How do i analyse my results?
  - What do I need to interpret my results?
  - What am I looking for?
- Artifacts?
  - What plots?

Looking at the data, my understanding so far is this:
- 0: baseline, 1: first drug, 2: second drug
- 60 electrodes, 180s @ 1000Hz
- Edges of the MEA are likely to have less reliable data

**Write python scripts that can:**
1. connect to google drive and download the raw data (run once)
2. extract the `filt_data` 2d array from each file and label it.
   1. find package to interact with .mat files
   2. convert 2d array into appropriate object
3. compute the *mean* of the 2d array to get an average time series signal for each subject, reducing filesize 60x.

##### Friday 27<sup>th</sup> March <!-- omit in toc -->

- downloaded the data to my computer today, stored in `data/raw`
- testing how to interact with .mat files using `scipy.io`
- working on a script that recursively loads all the files, extracts the time-series data and stores them in pandas data frames.
  - question for andreas/peng: should I be taking the values from every electrode or using a mean?
  - starting with mean for simplicity (reduces data size by 60x) - this can be used in my prototype

- experimented with this in a notebook [`1.0-kv-loading-data.ipynb`](../1.0-kv-loading-data.ipynb)
- put relevant applicable code into [`make_dataset.py`](../src/data/make_dataset.py)
  - next steps: include an export to csv files, put in `data/interim`
- recommended that we change our project structure in terms of github repos
  1. **Data Science Repo**: The original repo, based on the cookie cutter data science strucutre. This will house all the python scripts, notebooks etc. used to develop the ML classifier. Managed by Kartikey.
  2. **Mathematical Modelling Repo**: This will house the simulations and MATLAB files, as well as any python scripts to build the MM. Managed by Louis
  3. **Documentation Repo**: This will contain project logs, meeting updates, references, resources and p4p admin stuff. Managed by both of us.

##### Monday 30<sup>th</sup> March <!-- omit in toc -->

- rename ML repo, create documentation repo
  - ML repo: [GI-timeseries-classification](https://github.com/kartikey-vyas/GI-timeseries-classification)
  - MM repo: [GI-mathematical-modelling](https://github.com/louis-cf-lin/GI-mathematical-modelling)
  - Doc repo: [p4p-documentation](https://github.com/kartikey-vyas/p4p-documentation)


#### Week 5

no progress

#### Week 6

no progress

#### Midsemseter Break Week 1

no progress

#### Midsemester Break Week 2

##### Monday 20<sup>th</sup> April <!-- omit in toc -->

Starting literature review this week.  
Notes from Friday's meeting:
- do not downsample the data
- can chop up the 3 minute samples into 1-second windows or similar
- need a full lit review draft by next meeting (Friday 24 Apr)

##### Wednesday 22<sup>nd</sup> April <!-- omit in toc -->

Starting to write the literature review in markdown. Familiar enough with the workflow and dataset that starting the project won't be too much of an issue as soon as the lit review is done.

Using **Zotero** to manage my references. Unsure if this is the best product but it has a useful chrome plugin and can export bibiliographies in a variety of formats including BibTeX.

I intend to do the final copy of my lit review in LaTeX. Might just use overleaf at this point.

### COVID-19 LEVEL 2

Covid really messed things up, trying to get back to normal now. CONSISTENT WORKFLOW.

#### Literature Review Feedback 
Andreas's Feedback:
  - fig. 1 needs axes descriptions for final report. Do this in photoshop/paint/word
  - quote on pg 3 (ECG wave characteristics) should have an accompanying diagram. Peng said the diagram wasn't really necessary so maybe remove the description of the waveform entirely.
  - *concerning ML*:  "For your final report, you could weave a brief discussion of feature engineering from time series into the introduction in order to pave the way for your project scope. Please use the papers from Ben Fulcher as well as the descriptions of tsfresh (see attached)."

#### Vivek's initial advice

*ASK PENG*:  
- How frequently do we need to make a prediction?  
- For the subjects we have, what is the typical value of cycles per minute for slow waves?

*Initially Assume:*
 - start with every 6s (10 per minute)
 - 30 prediction windows over 3 mins
 - discretised windows initially ; first 6k are window 1, next 6k are window 2...
 - have them overlap a bit after you see the size of the data

Target variable: 
$$ y \in \{0,1,2\} $$ 
- 0: Baseline Recording
- 1: Ach Applied
- 2: AT Applied (after Ach)

Combine them into one big dataframe at the end

1. create windows for means data (Ach-AT only)
2. build training set with means data (Ach-AT only)
3. create windows/build training set with full data


#### ML Meeting with Andreas

get any classification result
- use what data we have in raw format (60 cols, 180k rows)

cross validation
- leave one group (subject) out sci-kit learn CV

hpc access:
>- uoa00488 ("Data Science for Engineering Applications")

#### Friday 12 June Meeting

**Experiments to run**:
1. Extract minimal features on full Ach-AT data set
    - fit decision tree
    - fit random forest
    - cross validate with subjects 0-5
    - test on subject 6
2. Repeat 1 with efficient features


try this with a small selection of electrodes
feature importance plots from tree
- use seaborn to create histograms of feature distribution
- distinct dists for each y = important
- overlapping dists = insignificant
try a random forest on X_min and X_eff

read the link for NeSI access (Mahuika cluster)
formulate python scripts that can do small parts of the feature extraction (ie can run it for a specific window ID)

#### Thursday 25 June
produced some histograms of feature distributions for the 4 electrode dataset (subject 0, ach-at)
- shows me that most of the features (after minimal feature extraction, imputation and selection) have a hard time distinguishing the three outcomes
- dont know how to interpret them further or what to do after this

tried using subject 2 with a couple of different configurations (minimal features, test size=0.4)
- middle strip of electrodes: accuracy ~87%
- all electrodes: accuracy ~87%

next:
- cross validation?
- random forest
- train on multiple subjects and test on a different one

### Intersem Break
#### Thursday 9 July
**pending: full dataset features**
- split into train/test
  - take one subject out to test on
    - cross-val on training set to optimise params
  - random split
    - cross-val on training set
- cross-val with whole dataset

model(s) to fit -> random forest, max depth = 3, 200 trees [those were the best from experimenting on subject 2]


**Questions to ask Andreas:**

- how to interpret feature importance
- what other model algorithms to test (SVM, xgboost, NN (MLP, CNN), LR)
- tsfresh configuration options
- how to set up parameter sweeps on HPC
  - suggest ez-experimentr infrastructure (singularity containers)? Ask about auckland uni cloud services. Otherwise use my AWS credits.
- what result metric should I use?
  - my thoughts: precision, recall, accuracy, area under ROC
- how should I document my progress so far
- what am i doing well, what can i improve on
- moving to the next part of the project - slow wave propagation directionality

gridsearchCV
sys library
job array ${} - this argument can be passed to python script - use it to specify sensor subset
set up python script to accept different arguments
library argparse
sns function: violinplot
time()

one hot encode the target col

look into:
  feature selection code
  p-values
  take ones that appear 3 times

accuracy measures:
  matthews correlation coefficient
  AUC sklearn metrics

feature importance - link this back to the physiology

be aware of any inconsistencies in processed data when splitting up feature extraction tasks

### Semester 2
#### Week 1 Meeting
**Monday 3/8**

Make sure to include logging messages as scripts progress 
Split dataframe into 60 features so that each script doesnt have to hold full set in memory? -> maybe just split into rows or cols of the MEA



*script descriptions*  
---
**extract_features.py**  
purpose: run *efficient* feature extraction on entire dataset  
method:
1. do each feature + differences with neighbours separately
2. specify with job array {1:60} parameter
3. script args
    - signal_num: integer, 1-60, specifies which electrode to do feature extraction for
4. file to read from: ach_at_full.h5 (6 second intervals)
5. file to write to: `fname = "electrode_{}_efficient_features.h5".format(signal_num)`
6. put them in folder data/features/unfiltered

---
**select_features.py**  
purpose: conduct hypothesis testing on each feature with respect to target variable y.  
method:
1. do each extracted h5 file separately as it is produced
2. script args
    - signal_num: integer, 1-60, specifies which electrode to filter features for
3. run the `target_binary_feature_real_test()` function on each feature for each target var. Target vars should be binary (0/1 baseline, 0/1 Ach, 0/1 AT). Use mann test.
4. save features with p-value <0.05 for **all 3** target vars.
5. file to write to: `fname = "electrode_{}_efficient_features_filtered.h5".format(signal_num)`