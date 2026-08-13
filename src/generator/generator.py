import time
import random
import socket
import json

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

counters = {'coolant_temp': 0, 'rpm': 0, 'throttle_pos': 0}
rpm = 2000
throttle_pos = 50
time_n = {'coolant_temp':0,'rpm': 0, 'throttle_pos': 0}


def make_reading(sensor):
    dict_readings = {}
    dict_readings['channel'] = sensor
    dict_readings['timestamp'] = time.time()
    if sensor == 'coolant_temp':
        dict_readings['value'] = random.gauss(95, 1 )
    elif sensor == 'rpm':
        dict_readings['value'] = rpm 
    elif sensor == 'throttle_pos':
        dict_readings['value'] = throttle_pos
    counters[sensor] +=1
    dict_readings['seq'] = counters[sensor]
    return dict_readings


def send(reading):
    text = json.dumps(reading)
    data = text.encode()
    sock.sendto(data, ("localhost", 9999))

try:

    while True: 
        throttle_pos = throttle_pos + random.uniform(-5, 5)
        if throttle_pos < 0: throttle_pos = 0
        if throttle_pos > 100: throttle_pos = 100

        target = 2000 + (throttle_pos / 100) * (9000 - 2000)
        rpm = rpm + (target - rpm) * 0.1
        if rpm < 2000: rpm = 2000
        if rpm > 9000: rpm = 9000
        
        time_n['coolant_temp'] += 1
        time_n['rpm'] += 1
        time_n['throttle_pos'] += 1
        if time_n['coolant_temp'] >= 10:
            send(make_reading('coolant_temp'))
            time_n['coolant_temp'] = 0

        if time_n['rpm'] >= 1:
            send(make_reading('rpm'))
            time_n['rpm'] = 0
        
        if time_n['throttle_pos'] >= 5:
            send(make_reading('throttle_pos'))
            time_n['throttle_pos'] = 0    
        time.sleep(0.01) 

except KeyboardInterrupt:
    print('Stopped')


