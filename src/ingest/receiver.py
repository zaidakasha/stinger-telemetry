import socket
import json

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)   
sock.bind(("localhost", 9999))   

while True:
    try:
        try:
            data, addr = sock.recvfrom(1024)
            text = data.decode()       
            reading = json.loads(text) 
            print(reading)  
        except json.decoder.JSONDecodeError:
            print(f'A packet dropped {data}')
    except KeyboardInterrupt:
        print('Stopped')