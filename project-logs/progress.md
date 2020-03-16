# Part IV Project 2020 Readings

This document will serve as a progress log, including lists of tasks, comments on readings and meeting updates.

- [Part IV Project 2020 Readings](#part-iv-project-2020-readings)
  - [To Read](#to-read)
  - [Reading Summaries](#reading-summaries)
    - [Hands-On Machine Learning... Geron (2017)](#hands-on-machine-learning-geron-2017)

## To Read

| Kart  | Louis | Title                                                                |
| :---: | :---: | :------------------------------------------------------------------- |
|  ---  |  ---  | **Andreas - Dive into Part IV**                                      |
|   ✔   |   ✔   | Best/Good Enough Practices in Scientific Computing                   |
|   ✔   |       | On Communicating Scientific Data                                     |
|       |   ✔   | Improving the traditional information management in natural sciences |
|   ✔   |       | Git Book                                                             |
|   ✔   |       | Data Science Process, Ch 1 and 2 of Geron (2017)                     |
|       |       | Time-series features, Ch 1 and 8 of Nielsen (2019)                   |
|       |       | Time-series features, overview from Fulcher (2018)                   |
|       |       | Learn about tsfresh, Christ et al. (2016, 2018)                      |
|  ---  |  ---  | **Peng's Material**                                                  |
|       |       | MEA 2019                                                             |
|       |       | Gastric Model 2D                                                     |
|       |       | Sodium Cell Model                                                    |
|       |       | Simplified Cell Model                                                |

## Reading Summaries

### Hands-On Machine Learning... Geron (2017)

#### Chapter 1 - The Machine Learning Landscape <!-- omit in toc -->

This chapter discussed the fundamentals of ML. It discussed different ways of categorising ML algorithms/approaches. It also brought up notable challenges in ML problems. Mostly recap of basic STATS 369 material.

- *Supervised vs. Unsupervised Learning*
  - Supervised: Training data is labeled, model predicts what the label will be on an unlabelled data point. e.g. Regression, Trees, SVM, KNN...
  - Unsupervised: Unlabeled training data. Includes clustering algorithms, dimensionality reduction and visualisation. e.g. k-means, PCA...
  - Semisupervised: Mostly unlabeled, some labeled e.g. Google photos labels clusters of photos rather than each photo.
- *Online vs. Batch Learning*
  - Batch: when new data is available, must retrain entire model with new + old data
  - Online: can train system incrementally by feeding it new data sequentially
- *Instance-based vs. Model-based Learning*
  - Instance: model remembers training data points, uses similarity measure to compare to new points. e.g. k-nearest neighbours
  - Model: build a model that generalises the training data, use it to make predictions. e.g. linear regression

**Machine Learning Challenges**

- Insufficient quantity of data
- Nonrepresentative training data
- Poor-quality data (very noisy, missing data)
- Irrelevant features (feature selection, feature extraction)
- Overfitting
- Underfitting
- Testing and Validating (train-test split, cross-validation)

#### Chapter 2 - End to End ML Project <!-- omit in toc -->

**Outline of Steps**

- Big Picture
  - Frame the problem
    - Objective of the solution; how will the predictions be used downstream?
    - Current solution; improvements, requirements
    - ML solution type; Supervised, Classification, Batch
  - Select performance measure
  - Check the assumptions
