import socket
import json

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)   
sock.bind(("localhost", 9999))   
def parse_packet(data):
    try:
        return json.loads(data.decode())
    except (json.JSONDecodeError, UnicodeDecodeError):
        return None

while True:
    data, addr = sock.recvfrom(1024)
    reading = parse_packet(data)
    try:
        if reading is None:
            print(f"Bad packet dropped: {data}")
        else:
            print(reading)
    except (json.JSONDecodeError, UnicodeDecodeError):
        print('Stopped')