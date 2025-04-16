## Usage: sudo -u redislabs python3 file.py  --config-file cluster.csv --dbname <bdname>

import requests
from requests.auth import HTTPBasicAuth
import urllib3
import csv
import base64
import argparse
import os
import json
from datetime import datetime

clname = ''
port = 9443
host = ''
cluser = ''
clpass = ''
cldesc = ''
backup_location = ''
dbname = ''

def export_redis_backup(bdb_uid: int):
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    backup_path_db_ts = os.path.join(backup_location, dbname,timestamp)

    # This makes the dir locally – but the server must have this mount point too
    os.makedirs(backup_path_db_ts, exist_ok=True)

    url = f"https://{host}:{port}/v1/bdbs/{bdb_uid}/actions/export"
    headers = {"Content-Type": "application/json"}
    data = {
        "export_location": {
            "type": "mount_point",
            "path": backup_path_db_ts  # Must match what's registered in Redis Enterprise
        }
    }

    print("Sending request to:", url)
    print("Request payload:", json.dumps(data, indent=2))

    response = requests.post(
        url,
        headers=headers,
        json=data,
        auth=HTTPBasicAuth(cluser,clpass),
        verify=False  # Note: disables SSL verification; fine for dev/testing
    )

    print("Response code:", response.status_code)
    print("Response body:", response.text)

    return response

def get_bdbs():
    url = f"https://{host}:{port}/v1/bdbs"
    print(url)

    try:
        response = requests.get(url, auth=HTTPBasicAuth(cluser,clpass), verify=False)
        response.raise_for_status()  # Raises an error for bad responses (4xx or 5xx)
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        return None

def find_uid_by_name(data, name):
    for item in data:
        if item.get("name") == name:
            return item.get("uid")
    return None


def parse_kv_csv(filename):
    with open(filename, newline='') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            kv_pairs = row if row else next(reader)
            config = dict(pair.split(":", 1) for pair in kv_pairs)

            # Decode base64 password if present
            if 'clpass' in config:
                try:
                    config['clpass'] = base64.b64decode(config['clpass']).decode('utf-8').strip()
                except Exception as e:
                    print(f"Error decoding clpass: {e}")
                    config['clpass'] = ''

            return config

def set_env_vars(config):
    for key, value in config.items():
        os.environ[key.upper()] = value  # Use uppercase env vars by convention

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Load config from CSV and export as environment variables.")
    parser.add_argument("--config-file", required=True, help="Path to the config CSV file")
    parser.add_argument("--dbname", required=True, help="Database name")

    args = parser.parse_args()
    config = parse_kv_csv(args.config_file)

    clname = config['clname']
    port = int(config['port'])
    host = config['host'] 
    cluser = config['cluser']
    clpass = config['clpass']
    backup_location = config['backup_location']
    dbname = args.dbname

    try:
      data = get_bdbs()
      if data:
        uid = find_uid_by_name(data, dbname)
        if uid is not None:
            print(f"Exporitng database '{dbname}' with UID {uid}")
            export_redis_backup(uid)
        else:
            print(f" No UID found for dbname '{dbname}'")
      else:
        print(" No data returned from get_bdbs()")
    except Exception as e:
        print(f" Error occurred: {e}")

