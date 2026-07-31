import time
import random
def make_reading(sensor):
    dict_readings = {}
    dict_readings['channel'] = str(sensor)
    dict_readings['timestamp'] = time.time()
    if sensor == 'coolant_temp':
        dict_readings['value'] = random.gauss(85, 1 )
    elif sensor == 'rpm':
        rpm = 2000
        dict_readings['value'] = rpm + random.uniform(-200,200)
    dict_readings['seq'] = 0
    return dict_readings

try:
    while True:
        print(make_reading('rpm'))
        time.sleep(0.1)

except KeyboardInterrupt:
    print('Stopped')
