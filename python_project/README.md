Programming fundamentals project
==============================

Remeber to follow PEP8 guys ;) 
Hotel review sentiment analysisisisisisissisisisisisisisisisisisis :)
feel free to update this markdown fileeeeeeeee

# Getting started 
### Whats a virtual environment and why do we need to use it??
Virtual environments are "workspaces" isolated from ur local machine to avoid conflicts in package versions

### Before u start, you have to activate your virtual environment 
if you dont, you'll be using library versions from your local machine
1. Open terminal
2. FOR CMD: ``Run myenv\Scripts\activate`` to activate virtual env 
    FOR BASH ``source myenv/Scripts/activate`` to activate virtual env
3. pip install -r requirements.txt to install libraries 

### How to add a library
Should you need additional libraries, you need to update the requirements.txt file after installing our library
1. ``pip install libary_name`` to install library
2. ``pip freeze > requirements.txt`` to update requirements.txt file

# Commands to know!
``pip freeze`` to check libriries installed ok??????????
``deactivate`` to exit virtual env


Project structure
------------

    ├── myenv                    <- Virtual environment folder
    │
    ├── notebooks                <- Jupyter notebooks
    |
    ├── data
    │   └── raw                  <- The original, immutable data dump.                        
    │
    ├── requirements.txt         <- dependencies
    │
    ├── src                      <- Source code for use in this project.
    │   ├── main.py              <- execution point
    │   │
    │   ├── data cleaning        <- Scripts to download or generate data
    │   │   └── make_dataset.py
    │   │
    │   ├── data fetching        <- Scripts to turn raw data into features for modeling
    │   │   └── extraction.py
    │   │
    │   ├── sentiment analysis   <- Scripts to create sentiment analysis
    │   │   │                 
    │   │   └── sa.py
    │   │   
    │   │
    │   └── visualization        <- EDA
            └── visualize.py

##we can do this guyssssss