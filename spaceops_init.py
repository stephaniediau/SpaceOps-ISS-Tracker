#!/usr/bin/env python3

import os
import mysql.connector

DBHOST = os.environ.get('DBHOST', 'ds2002.cgls84scuy1e.us-east-1.rds.amazonaws.com')
DBUSER = os.environ.get('DBUSER')
DBPASS = os.environ.get('DBPASS')
DB     = 'spaceops_tracking'

db = mysql.connector.connect(host=DBHOST, user=DBUSER, password=DBPASS, database=DB)
cursor = db.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS reporters (
        reporter_id INT AUTO_INCREMENT PRIMARY KEY,
        team_name VARCHAR(100)
    )
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS locations (
        timestamp DATETIME,
        latitude FLOAT,
        longitude FLOAT,
        message VARCHAR(50),
        reporter_id INT
    )
""")

db.commit()
print("Tables created successfully")

cursor.close()
db.close()