import json
import logging
import requests
from datetime import datetime
from chalice import Chalice

app = Chalice(app_name='iss-tracker')
app.debug = True

logger = logging.getLogger()
logger.setLevel(logging.INFO)

URL = "http://api.open-notify.org/iss-now.json"

def extract():
    response = requests.get(URL)
    response.raise_for_status()
    return response.json()

def transform(data):
    timestamp = datetime.utcfromtimestamp(data['timestamp'])
    pos = data['iss_position']
    return {
        "timestamp": str(timestamp),
        "latitude": float(pos['latitude']),
        "longitude": float(pos['longitude']),
        "message": data['message']
    }

@app.schedule('rate(1 minute)')
def fetch_iss(event):
    data = extract()
    record = transform(data)

    logger.info(record)

    return {
        "status": "success",
        "data": record
    }
