## Usage: sudo -u redislabs python3 file.py  --config-file cluster.csv --dbname <dbname>

import requests
from requests.auth import HTTPBasicAuth
import urllib3
import csv
import base64
import argparse
import os
import json
from datetime import datetime

# Disable warnings for unverified HTTPS requests (not recommended for production)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Global config placeholders (to be filled from CSV)
clname = ''
port = 9443
host = ''
cluser = ''
clpass = ''
cldesc = ''
backup_location = ''
dbname = ''

# Function to export Redis backup to a mount point with timestamped folder
def export_redis_backup(bdb_uid: int):
    # Create timestamp for unique backup folder
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    backup_path_db_ts = os.path.join(backup_location, dbname, timestamp)

    # Create local backup directory
    os.makedirs(backup_path_db_ts, exist_ok=True)

    # Prepare the export request
    url = f"https://{host}:{port}/v1/bdbs/{bdb_uid}/actions/export"
    headers = {"Content-Type": "application/json"}
    data = {
        "export_location": {
            "type": "mount_point",
            "path": backup_path_db_ts  # Must exist and be writable on Redis Enterprise node
        }
    }

    print("Sending request to:", url)
    print("Request payload:", json.dumps(data, indent=2))

    # Make POST request to export backup
    response = requests.post(
        url,
        headers=headers,
        json=data,
        auth=HTTPBasicAuth(cluser, clpass),
        verify=False  # Skip SSL verification for now
    )

    # Print API response
    print("Response code:", response.status_code)
    print("Response body:", response.text)

    return response

# Function to get all Redis databases via REST API
def get_bdbs():
    url = f"https://{host}:{port}/v1/bdbs"
    print(url)

    try:
        response = requests.get(url, auth=HTTPBasicAuth(cluser, clpass), verify=False)
        response.raise_for_status()  # Raise error on 4xx/5xx responses
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        return None

# Function to find UID of a database by its name
def find_uid_by_name(data, name):
    for item in data:
        if item.get("name") == name:
            return item.get("uid")
    return None

# Function to parse a single-line CSV with key:value pairs
def parse_kv_csv(filename):
    with open(filename, newline='') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            kv_pairs = row if row else next(reader)
            config = dict(pair.split(":", 1) for pair in kv_pairs)

            # Decode base64-encoded password if present
            if 'clpass' in config:
                try:
                    config['clpass'] = base64.b64decode(config['clpass']).decode('utf-8').strip()
                except Exception as e:
                    print(f"Error decoding clpass: {e}")
                    config['clpass'] = ''

            return config

# Function to set environment variables (optional)
def set_env_vars(config):
    for key, value in config.items():
        os.environ[key.upper()] = value  # Uppercase by convention

# Main script
if __name__ == "__main__":
    # CLI argument parsing
    parser = argparse.ArgumentParser(description="Load config from CSV and export Redis backup.")
    parser.add_argument("--config-file", required=True, help="Path to the config CSV file")
    parser.add_argument("--dbname", required=True, help="Database name to export")

    args = parser.parse_args()
    config = parse_kv_csv(args.config_file)

    # Assign global values from parsed config
    clname = config['clname']
    port = int(config['port'])
    host = config['host']
    cluser = config['cluser']
    clpass = config['clpass']
    backup_location = config['backup_location']
    dbname = args.dbname

    # Get UID and export backup
    try:
        data = get_bdbs()
        if data:
            uid = find_uid_by_name(data, dbname)
            if uid is not None:
                print(f"Exporting database '{dbname}' with UID {uid}")
                export_redis_backup(uid)
            else:
                print(f" No UID found for dbname '{dbname}'")
        else:
            print("No data returned from get_bdbs()")
    except Exception as e:
        print(f"Error occurred: {e}")
