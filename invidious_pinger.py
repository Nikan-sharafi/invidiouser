import requests
import time
import json

def fetch_data(url):
    res = requests.get(url)
    if res.status_code == 200:
        return res.json()
    return None

def check_latency(host):
    try:
        start_time = time.time()
        res = requests.get(f"https://{host}", timeout=5)    
        latency = time.time() - start_time
        if res.status_code == 200:
            return latency
        else:
            return None
    except Exception as e:
        print(f"Error reaching {host}: {e}")
        return None

configs = 'https://api.invidious.io/instances.json?pretty=1&sort_by=type,users'

instances = fetch_data(configs)

healthy_instances = {}
for instant in instances:
    url, _ = instant
    latency = check_latency(url)
    if latency:
        healthy_instances[url] = latency

# Sort instances based on latency
healthy_instances = [{'url': k, 'latency': v} for k, v in
                    sorted(healthy_instances.items(), key=lambda x: x[1])]

# save as json
with open('instances.json', 'w') as json_file:
    json.dump(healthy_instances, json_file, indent=4)
    print('sucsses')
