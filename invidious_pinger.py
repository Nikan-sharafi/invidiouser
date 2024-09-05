import requests
import platform
import subprocess
import re
import json


def fetch_data(url):
    res = requests.get(url)
    if res.status_code == 200:
        return res.json()
    return None


def ping_host(host):
    # choose command based on os
    param = "-n" if platform.system().lower() == "windows" else "-c"
    
    command = ["ping", param, "1", host]
    
    try:
        # ping the url
        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        
        if result.returncode == 0:
            if platform.system().lower() == "windows":
                match = re.search(r"Average = (\d+)ms", result.stdout) # extract ping data
            else:
                match = re.search(r"rtt min/avg/max/mdev = \d+.\d+/(\d+.\d+)/\d+.\d+/\d+.\d+ ms", result.stdout)

            ping_time = match.group(1)
            return ping_time
            
        else:
            return None
    
    except Exception as e:
        print(f"An error occurred: {e}")


configs = 'https://api.invidious.io/instances.json?pretty=1&sort_by=type,users'

instances = fetch_data(configs)

healthy_instances = {}
for instant in instances:
    url, _ = instant

    ping = ping_host(url)
    if ping:
        healthy_instances[url] = ping

# sort instances based on ping
healthy_instances = [{'url' : k, 'ping': v} for k, v in
                      sorted(healthy_instances.items(), key=lambda x:x[1])]

# save as jsom
with open('instances.json', 'w') as json_file:
    json.dump(healthy_instances, json_file, indent=4)