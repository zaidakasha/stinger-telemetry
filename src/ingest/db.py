import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "telemetry.db")
con = sqlite3.connect(DB_PATH)
cur = con.cursor()
cur.execute("CREATE TABLE IF NOT EXISTS readings(channel TEXT, timestamp REAL , value REAL, seq INTEGER)")
con.commit()

def insert_reading(reading):
    cur.execute("INSERT INTO readings (channel, timestamp, value, seq) VALUES (?, ?, ?, ?)", (reading['channel'], reading['timestamp'], reading['value'], reading['seq']))
    con.commit()

