import sqlite3
import os
import time

DB_PATH = os.path.join(os.path.dirname(__file__), "telemetry.db")
con = sqlite3.connect(DB_PATH, check_same_thread=False)
cur = con.cursor()
cur.execute("CREATE TABLE IF NOT EXISTS readings(channel TEXT, timestamp REAL , value REAL, seq INTEGER)")
cur.execute('CREATE INDEX IF NOT EXISTS idx_channel_ts ON readings(channel, timestamp)')
con.commit()

def insert_reading(reading):
    cur.execute("INSERT INTO readings (channel, timestamp, value, seq) VALUES (?, ?, ?, ?)", (reading['channel'], reading['timestamp'], reading['value'], reading['seq']))
    con.commit()

def get_recent(channel, seconds):
    con = sqlite3.connect(DB_PATH, check_same_thread=False)
    result = con.execute('SELECT * FROM readings WHERE channel = ? AND timestamp > ?', (channel, time.time() - seconds)).fetchall()
    con.close()
    return result



