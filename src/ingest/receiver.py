import socket
import json
from src.ingest.db import insert_reading
import time


def parse_packet(data):
    try:
        return json.loads(data.decode())
    except (json.JSONDecodeError, UnicodeDecodeError):
        return None
if __name__ == "__main__":          
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(("localhost", 9999))
    last_seqs = {}
    count = 0
    start_time = time.time()
    while True:
        data, addr = sock.recvfrom(1024)
        reading = parse_packet(data)
        if reading is None:
            print(f"Bad packet dropped: {data}")
        else:
            print(reading)
            insert_reading(reading)
            latency = time.time() - reading['timestamp']

            count += 1
            if count % 100 == 0:
                rate = count / (time.time() - start_time)
                print(f"latency: {latency*1000:.1f}ms   throughput: {rate:.0f} rows/sec")


            channel = reading['channel']
            seq = reading['seq']
            if channel not in last_seqs:
                last_seqs[channel] = seq

            else:

                if seq - last_seqs[channel] > 1:
                    missing = seq - last_seqs[channel] - 1                         
                    print(f"WARNING: gap on {channel} - missed {missing} packets")   
                last_seqs[channel] = seq     

                                  
                                  
    
        