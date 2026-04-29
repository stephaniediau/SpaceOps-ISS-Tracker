#!/usr/bin/env python3

import os
import json
import decimal
import datetime
import mysql.connector
from mysql.connector import Error


DBHOST = os.environ.get('DBHOST', 'ds2002.cgls84scuy1e.us-east-1.rds.amazonaws.com')
DBUSER = os.environ.get('DBUSER')
DBPASS = os.environ.get('DBPASS')
REPORTER_ID = int(os.environ.get('REPORTER_ID', 1))
DB = 'spaceops_tracking'

def get_connection():
    return mysql.connector.connect(host=DBHOST, user=DBUSER, password=DBPASS, database=DB)

def decoder(o):
    if isinstance(o, datetime.datetime):
        return str(o)
    if isinstance(o, decimal.Decimal):
        return str(o)

def print_results(results):
    print(json.dumps(results, default=decoder, indent=2))

# Query 1: Most recent ISS location
def get_latest_location():
    db = get_connection()
    cursor = db.cursor(dictionary=True)
    try:
        cursor.execute("""
            SELECT timestamp, latitude, longitude, message
            FROM locations
            WHERE reporter_id = %s
            ORDER BY timestamp DESC
            LIMIT 1
        """, (REPORTER_ID,))
        print_results(cursor.fetchall())
    except Error as e:
        print("Error:", e)
    finally:
        cursor.close()
        db.close()

# Query 2: Last N locations
def get_last_n_locations(n=10):
    db = get_connection()
    cursor = db.cursor(dictionary=True)
    try:
        cursor.execute("""
            SELECT timestamp, latitude, longitude, message
            FROM locations
            WHERE reporter_id = %s
            ORDER BY timestamp DESC
            LIMIT %s
        """, (REPORTER_ID, n))
        print_results(cursor.fetchall())
    except Error as e:
        print("Error:", e)
    finally:
        cursor.close()
        db.close()

# Query 3: Closest location to a given timestamp
def get_location_at_time(target_timestamp):
    db = get_connection()
    cursor = db.cursor(dictionary=True)
    try:
        cursor.execute("""
            SELECT timestamp, latitude, longitude, message
            FROM locations
            WHERE reporter_id = %s
            ORDER BY ABS(TIMESTAMPDIFF(SECOND, timestamp, %s))
            LIMIT 1
        """, (REPORTER_ID, target_timestamp))
        print_results(cursor.fetchall())
    except Error as e:
        print("Error:", e)
    finally:
        cursor.close()
        db.close()

# Query 4: Closest location to a given latitude and longitude
def get_location_near(target_lat, target_lon, n=5):
    db = get_connection()
    cursor = db.cursor(dictionary=True)
    try:
        cursor.execute("""
            SELECT timestamp, latitude, longitude, message,
                   SQRT(POW(latitude - %s, 2) + POW(longitude - %s, 2)) AS distance
            FROM locations
            WHERE reporter_id = %s
            ORDER BY distance ASC
            LIMIT %s
        """, (target_lat, target_lon, REPORTER_ID, n))
        print_results(cursor.fetchall())
    except Error as e:
        print("Error:", e)
    finally:
        cursor.close()
        db.close()

if __name__ == '__main__':
    print("=== Latest ISS Location ===")
    get_latest_location()

    print("\n=== Last 10 Locations ===")
    get_last_n_locations(10)

    print("\n=== Closest to 2026-04-01 12:00:00 ===")
    get_location_at_time("2026-04-01 12:00:00")

    print("\n=== Closest to lat=0, lon=0 (top 5) ===")
    get_location_near(0.0, 0.0, 5)