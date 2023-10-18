Programming fundamentals project
==============================

- Remeber to follow PEP8 guys ;)
- feel free to update this markdown fileeeeeeeee

# Getting started 
### Whats a virtual environment and why do we need to use it??
Virtual environments are "workspaces" isolated from ur local machine to avoid conflicts in package versions

### what to do if ModuleNotFoundError: No module named 'pip'
``python -m ensurepip --default-pip``

### Before u start, you have to activate your virtual environment 
if you dont, you'll be using library versions from your local machine
1. Open terminal
2. FOR CMD: ``Run myenv\Scripts\activate`` to activate virtual env 
-  FOR BASH ``source myenv/Scripts/activate`` to activate virtual env
3. ``pip install -r requirements.txt`` to install libraries 
4. ``ipython kernel install --user --name=venv`` to create a kernel inside jupyter notebook

### How to add a library
Should you need additional libraries, you need to update the requirements.txt file after installing our library
1. ``pip install libary_name`` to install library
2. ``pip freeze > requirements.txt`` to update requirements.txt file

# Commands to know!
``pip freeze`` to check libriries installed ok??????????
``deactivate`` to exit virtual env


Project structure
------------

    ├── data
    │   └── raw                  <- The original, immutable data dump. 
    ├── myenv                    <- Virtual environment folder
    │
    ├── notebooks                <- Jupyter notebooks
    |
    ├── src                      <- Source code for use in this project.
    │   │
    │   ├── data_cleaning        <- Scripts to turn raw data into features for modeling
    │   │   └── cleaning.py
    │   │
    │   ├── data_scrapping       <- Scripts to download or generate data
    │   │   |── 01_scrape_hotel.py
    |   |   |── 02_scrape_review.py
    |   |   └── 03_clean_file.py
    │   │
    │   ├── sentiment_analysis   <- Scripts to create sentiment analysis
    │   │   │                 
    │   │   └── sa_vader.py
    │   │   
    │   ├── visualisation        <- EDA
    |   |     └── visualise.py    
    |   |              
    |   └── main.py              <= Execution point  
    |
    ├── README.md                <- Markdown file
    |
    └── requirements.txt         <- Dependencies

# How to run this project FOR PROFESSORS
1. run main.py script in src directory
2. drag & drop Finalised_Total_Reviews.csv from data/raw/ into GUI
3. access rabs on the left and select hotels to be analysed from drop down bar

# How to run this project
1. Run 01_scrape_hotel.py, 02_scrape_review.py and 02_scrape_review.py in order from the data_scrapping directory
2. Files Hotel_list.csv & Finalised_Total_Reviews.csv will be generated in data/raw directory
3. run main.py script in src directory
4. drag & drop Finalised_Total_Reviews.csv into GUI
5. access rabs on the left and select hotels to be analysed from drop down bar
