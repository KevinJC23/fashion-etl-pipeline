# Fashion Studio ETL Pipeline 

## Case Study
You are a data engineer working for a retail company in fashion and design. Every month, your company release a new items that are widely loved and purchased by public. 

One time, the growth of fashion and design retailers increased rapidly! The result was a rapid influx of rivals. Your competitors are very adept at manipulating the prices, promotions, and even new clothing styles.

With this in mind, your company asked a data team to conduct research on their prices and products. The chosen competitor was Fashion Studio, which frequently releases a variety fashion products, such as t-shirts, pants, jackets, and outerwear.

![alt text](https://assets.cdn.dicoding.com/original/academy/dos-e8e13cd55ce219b9020f358daafadb5120250212132559.jpeg)
<p align="center">
  Website page: <a href="https://fashion-studio.dicoding.dev">https://fashion-studio.dicoding.dev</a>
</p>

As a data engineer, your job is to capturing and preparing competitor data so it's ready for use by the data science team. Therefore, your primary focus will be creating a simple ETL pipeline to capture, prepare, and store competitor data. 

## Folder Structure
```
etl-pipeline/
│
├── tests/
│   ├── test_extract.py                  
│   ├── test_load.py
│   └── test_transform.py
│
├── utils/
│   ├── extract.py
│   ├── transform.py
│   └── load.py
│
├── docker-compose.yaml
├── google-sheet-api.json
├── main.py  
├── products.csv
├── README.md
└── requirements.txt                        
```

## Setup Instruction

### Prerequisites
- Python 3.9+
- Docker Desktop (to run a PostgreSQL)
- Google Cloud Platform (to save the data to Google Sheets) 

### Environment Installation
```
# Create a Python Virtual Environment
python -m venv venv

# Activate the Virtual Environment
source venv/bin/activate    # For Mac/Linux
venv/Scripts/activate       # For Windows

# Install dependencies
pip install -r requirements.txt
```

### PostgreSQL Database with Docker
```
# Open Docker Desktop

# Run the container in the terminal
docker-compose up -d

# Enter to PostgreSQL terminal
docker exec -it fashion_postgres_container psql -U developer -d fashion_db

# Write SQL command to see contents of the table
SELECT * FROM products;
``` 

### Save Data using Google Sheets API
```
# Open Google Cloud Console

# Click Navigation Menu, then choose 'APIs & Library'

# Through the search bar, search 'Google Sheets API' then click 'Enabled'

# Click Navigation Menu, then choose 'APIs & Library' -> 'Credentials'

# In 'Credentials' page, click 'Create Credentials' -> 'Service Account', then:
  - Fill your 'Service Account Name'
  - Click 'Create and Continue' and in 'Select a Role' choose 'Basic -> Editor' 
  - After finish, click 'Continue' and 'Done'

# Create Service Account Key through several steps:
  - Click on the service account that you created before
  - Then, click 'Keys' -> 'Add Keys' -> 'Create New Key'
  - Select .JSON as a format file key and click 'Create'

# Copy the 'Client Email' then on Spreadsheet, click 'Share' button and give the access for 'Client Email' as 'Editor'

# Then click 'Send'

# Open 'main.py' file and fill 'SPREADSHEET_ID' with the spreadsheetID in the web url
  - URL Google Sheets: https://docs.google.com/spreadsheets/d/1QQJRRQBveHhZbHXBmI-7rrbntI96tihOYoR5GYrTcIE/edit?gid=0#gid=0
  - SpreadsheetID: 1QQJRRQBveHhZbHXBmI-7rrbntI96tihOYoR5GYrTcIE
```

### Run the Application
```
# Run the Script
python main.py
```

### Run unittest in tests folder
```
# Run the unittest
python -m pytest tests
```

### Run test coverage in tests folder
```
# simple report:
python -m pytest --cov=utils tests

# see missing lines report:
python -m pytest --cov=utils --cov-report=term-missing tests

# see the report in HTML form:
python -m pytest --cov=utils --cov-report=html tests
```