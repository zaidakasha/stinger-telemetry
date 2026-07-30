import time
import random
def make_reading():
    dict_readings = {}
    dict_readings['channel'] = 'coolant temp'
    dict_readings['timestamp'] = time.time()
    dict_readings['value'] = random.gauss(85, 1 )
    dict_readings['seq'] = 0
    return dict_readings

print(make_reading())