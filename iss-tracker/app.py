import logging
import requests
from datetime import datetime, timezone
from chalice import Chalice

app = Chalice(app_name='iss-tracker')
app.debug = True

logger = logging.getLogger()
logger.setLevel(logging.INFO)

URL = "http://api.open-notify.org/iss-now.json"
TIMEOUT = 5

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

@app.schedule('rate(1 minute)')
def fetch_iss(event):
    try:
        data = extract()
        record = transform(data)

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
