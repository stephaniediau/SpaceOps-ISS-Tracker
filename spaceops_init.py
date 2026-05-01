import mysql.connector
db = mysql.connector.connect(host='ds2002.cgls84scuy1e.us-east-1.rds.amazonaws.com', user='eby2ch', password='eby2ch', database='spaceops_tracking')
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