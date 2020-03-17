# Part IV Project 2020 Readings

This document will serve as a progress log, including lists of tasks, comments on readings and meeting updates.

- [Part IV Project 2020 Readings](#part-iv-project-2020-readings)
  - [To Read](#to-read)
  - [Reading Summaries](#reading-summaries)
    - [Hands-On Machine Learning ... (Geron, 2017)](#hands-on-machine-learning--geron-2017)
    - [Good enough practices ... (Wilson et al., 2017)](#good-enough-practices--wilson-et-al-2017)
      - [Data management](#data-management)
      - [Software](#software)
      - [Collaboration](#collaboration)
      - [Project Organisation](#project-organisation)
      - [Tracking changes](#tracking-changes)
      - [Manuscripts](#manuscripts)
    - [Best Practices ... (Wilson et al., 2014)](#best-practices--wilson-et-al-2014)

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

### Hands-On Machine Learning ... (Geron, 2017)

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

#

### Good enough practices ... (Wilson et al., 2017)

This article presents a set of computing tools and techniques that researchers are recommended to adopt. In particular, it is aimed at people who are new to research computing so some fundamental basics have been omitted from this summary.  

#### Data management

- Save raw data as originally generated, and consider changing file permissions to read-only, or similar. If not practical (e.g. large databases), record the exact procedure used to obtain the raw data.
- Ensure raw data is backed up in more than one location.
- Store useful metadata as part of file names, and use meaningful variable names.
- Write scripts for every stage of data processing.
- Give each record/observation a unique identifier for merging.
- Submit data to a reputable DOI-issuing repository (optional).

#### Software

- Include a brief explanation, an example, and reasonable parameter values at the start of every programme.
- Decompose programmes into functions no more than about 60 lines, and take no more than 6 arguments.
- Write and reuse functions, don't repeat yourself (D.R.Y.), and search for software libraries that do what you need. Test these before relying on them.
- Make dependencies explicit e.g. `REQUIREMENTS.md` or  `README` in the root directory.
- Use if/else statements instead of commenting/uncommenting code.
- Provide a simple example with known ouputs for testing.
- Submit code to a reputable DOI-issuing repository (optional).

#### Collaboration

- Create a `README.md` in the home directory that contains the project title, description/purpose, contact-info, and an example of the task.
- Decide on a communication strategy between project members, and with external collaborators.
- Optional:
  - `CONTRIBUTING.md` containing dependencies, installation tests, guidelines, and checklists for people looking to contribute to the project.
  - `TODO.md` list of items that newcomers can work on.
  - `LICENSE.md` file that clearly states what license(s) apply to the project. 
  - `CITATION.md` describes how to cite the parts of the project or as a whole.

#### Project Organisation

- Put raw data in a `data` directory and cleaned/processed files in `results`.
- Put source code in `src`.
- 
      .
      |--CITATION
      |--README
      |--LICENSE
      |--requirements.txt
      |--data
      |   |--birds_count_table.csv
      |--doc
      |   |--notebook.md
      |   |--manuscript.md
      |   |--changelog.txt
      |--results
      |   |--summarised_results.csv
      |--src
      |   |--sightings_analysis.py
      |   |--runall.py

#### Tracking changes

- Keep using Git version control.

#### Manuscripts

- Write manuscripts in plain text format that permits version control.
- Use a bibliography manager.

#

### Best Practices ... (Wilson et al., 2014)

This article is a condensed version of *Good enough practices ... (Wilson et al., 2017)*. The core info has been stripped away and only notes of interest are mentioned.

- A programme should not require its readers to hold more than a handful of facts in memory at once.
- The best language/coding style/version control system/software to use is almost always whatever your colleagues are already using.
- It is typically better to find an established library or package that solves a problem than to attempt to write one's own routines for well established problems.
- Defensive programming&mdash;add assertations to programmes to check their operation.
- Automated testing&mdash;use off-the-shelf unit testing libraries and turn bugs into test cases.
- Faster, lower level languages require more lines of code to accomplish the same task, so write code in highest-level language possible. Shift to low-level languages when the performance boost is absolutely necessary. Even when it is known that a low-level language will ultimately be necessary, rapid prototyping in a high-level language helps programmers make and evaluate design decisions quickly.
- Document interfaces and reasons, not implementations. Inline documentation that recapitulates code is not useful.
- Rather than write a paragraph to explain a complex piece of code, reorganise the code itself so that it doesn't need such an explanation (sometimes not possible).
