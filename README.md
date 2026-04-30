# SpaceOps-ISS-Tracker
DS2002 Final Project - Automatic ISS Tracker

A ETL pipeline that automatically fetches the current ISS position from a public API, transforms the data, and stores it in a database on AWS, building a time series dataset that grows without manual intervention. 

## Repository Structure
```
SpaceOps-ISS-Tracker Repo Folder Outline
│
├── data folder (tba)
│   └── tba
│
├── iss-tracker
│   ├── __pycache__
│   ├── .chalice
│   ├── .gitignore
│   ├── app.py
│   └── requirements.txt
│
├── query
│   ├── instructions.md
│   └── spaceops_query.py
│   
├── DS2002_Milestone.pdf
│   
├── LICENSE
│   
└── README.md
```

## Installation/Building
```
# clone the repository
git clone https://github.com/stephaniediau/SpaceOps-ISS-Tracker.git
cd SpaceOps-ISS-Tracker

# create & activate virtual environment
python3 -m venv venv
source venv/bin/activate        # Mac/Linux
venv\Scripts\activate           # Windows

# install dependencies
pip install -r iss-tracker/requirements.txt

# deploy pipeline to AWS Lambda
cd iss-tracker
chalice deploy
```

## Usage
### Running pipeline locally
```
cd iss-tracker
chalice local
```

### Querying database
```
# run query script
python3 -i query/spaceops_query.py
```


## Notes
- This project follows standard ETL (Extract, Transform, Load) pipeline structure
- This project uses AWS Chalice and has a scheduled rate limit of one minute, but note that there are other options besides Chalice that can support potentially faster rates. For example, AWS EC2 with cron jobs or containerized services such as AWS Docker.
- Potential future improvements include deploying an API that can run queries against the database.