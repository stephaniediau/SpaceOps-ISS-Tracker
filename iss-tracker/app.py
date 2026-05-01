import logging
import os
import requests
import mysql.connector 
from datetime import datetime, timezone
from chalice import Chalice

app = Chalice(app_name='iss-tracker')
app.debug = True

logger = logging.getLogger()
logger.setLevel(logging.INFO)

URL = "http://api.open-notify.org/iss-now.json"
TIMEOUT = 5

def connect_db():
    DBHOST = os.environ.get('DBHOST', 'ds2002.cgls84scuy1e.us-east-1.rds.amazonaws.com')
    DBUSER = os.environ.get('DBUSER')
    DBPASS = os.environ.get('DBPASS')
    DB     = 'spaceops_tracking'

    return mysql.connector.connect(host=DBHOST, user=DBUSER, password=DBPASS, database=DB)

def extract():
    response = requests.get(URL, timeout=TIMEOUT)
    response.raise_for_status()
    return response.json()

def transform(data):
    timestamp = datetime.fromtimestamp(data['timestamp'], tz=timezone.utc)
    pos = data['iss_position']
    return {
        "timestamp": timestamp.isoformat(),
        "latitude": float(pos['latitude']),
        "longitude": float(pos['longitude']),
        "message": data.get('message', 'unknown')
    }

def register_reporter(table, reporter_name):
    db = connect_db()
    cursor = db.cursor()

    cursor.execute(f"SELECT reporter_id FROM {table} WHERE team_name = %s", (reporter_name,))
    result = cursor.fetchone()

    if result:
        reporter_id = result[0]
        logger.info("Reporter already exists")
    else:
        cursor.execute(f"INSERT INTO {table} (team_name) VALUES (%s)", (reporter_name,))
        db.commit()
        reporter_id = cursor.lastrowid
        logger.info("Reporter registered")

    cursor.close()
    db.close()
    return reporter_id

def load(record, reporter_id):
    db = connect_db()
    cursor = db.cursor()

    query = """
        INSERT INTO locations (timestamp, latitude, longitude, message, reporter_id)
        VALUES (%s, %s, %s, %s, %s)
    """

    cursor.execute(query, (
        record['timestamp'],
        record['latitude'],
        record['longitude'],
        record['message'],
        reporter_id
    ))

    db.commit()
    cursor.close()
    db.close()

@app.schedule('rate(1 minute)')
def fetch_iss(event):
    try:
        reporter_name = "SpaceOps"
        reporter_id = register_reporter("reporters", reporter_name)

        data = extract()
        record = transform(data)
        load(record, reporter_id)
        
        logger.info(record)

        return{
            "status": "success",
            "data": record
        }

    except requests.exceptions.Timeout as e:
        logger.warning(f"ISS API timeout: {str(e)}")
        
        return{
            "status": "error",
            "error": "timeout"
        }
    
    except requests.exceptions.RequestException as e:
        logger.error(f"ISS API request failed: {str(e)}")

        return{
            "status": "error",
            "error": str(e)
        }
    
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")

        return{
            "status": "error",
            "error": str(e)
        }
