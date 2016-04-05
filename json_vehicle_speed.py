import json
import time

with open('Border_Roads.json', 'r') as file:
    decoded = json.loads(file.readline())
    now = time.gmtime(decoded['timestamp'])

    while True:
        if decoded['name'] == 'vehicle_speed':
            print decoded
        time.sleep(0.01)
        try:
            decoded = json.loads(file.readline())
        except Exception:
            break