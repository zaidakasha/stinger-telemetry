import socket
import json
from src.ingest.db import insert_reading


def parse_packet(data):
    try:
        return json.loads(data.decode())
    except (json.JSONDecodeError, UnicodeDecodeError):
        return None
if __name__ == "__main__":          
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(("localhost", 9999))
    while True:
        data, addr = sock.recvfrom(1024)
        reading = parse_packet(data)
        if reading is None:
            print(f"Bad packet dropped: {data}")
        else:
            print(reading)
            insert_reading(reading) 
    
        