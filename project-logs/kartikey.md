# Kartikey's Log

This is document will serve as a progress log for my part 4 project. It is written in markdown.

- [Kartikey's Log](#kartikeys-log)
  - [Setting up a development environment](#setting-up-a-development-environment)
    - [Technologies Used](#technologies-used)
    - [Workflow](#workflow)
  - [Progress Log](#progress-log)
    - [Week 2](#week-2)
    - [Week 3](#week-3)
    - [Week 4 (Teaching-free week)](#week-4-teaching-free-week)

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

1. Open windows terminal. This will automatically start Ubuntu 18.04 running on WSL 2. `win + 1`
2. `cd engsci700-project37 && code .` to open project folder in VS Code.
3. *insert jupyter notebook workflow here once figured out*

This set up will be used going forward from 13/03.

## Progress Log

### Week 2

#### Friday 13<sup>th</sup> March <!-- omit in toc -->

- Meeting with Peng (see meeting minutes)
- Organise time to see Andreas after reading time-series docs and getting started with `tsfresh`
- Continue literature review, start with the MEA documents sent by Peng.

### Week 3

#### Monday 16<sup>th</sup> March <!-- omit in toc -->

- adapted [progress.md](progress.md) to contain summaries of all of the readings that we complete.
- read Geron (2017) chapters 1 and 2, completed summary.

#### Tuesday 17<sup>th</sup> March <!-- omit in toc -->

- Downloaded and installed Python KOANS
- going to commit some time everyday to work through KOANS and improve python skills

#### Thursday 18<sup>th</sup> March <!-- omit in toc -->

- fixed some of the markdown linting issues by creating [.markdownlint.json](.markdownlint.json) in the project-logs directory.
  - if theres an annoying rule that keeps causing unnecessary warnings in your markdown file, add the rule name followed by false to the json file. e.g. `MD032 = false`

#### Friday 19<sup>th</sup> March <!-- omit in toc -->

- Meeting with Peng and Andreas
- continued python koans

### Week 4 (Teaching-free week)

#### Wednesday 25<sup>th</sup> <!-- omit in toc -->

- Watched literature review workshop video
- starting time-series readings
  - read Nielsen chapter 1 and chapter 8

#### Thursday 26<sup>th</sup> March<!-- omit in toc -->

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