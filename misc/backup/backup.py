import requests
from requests.auth import HTTPBasicAuth
import urllib3
from datetime import datetime
import os
import json

# Disable SSL warnings since we're using -k (insecure)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def export_redis_backup(bdb_uid: int, base_path: str = "/tmp/backup/", user: str = "demo@redis.com", password: str = "test", host: str = "localhost", port: int = 9443):
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    backup_path = os.path.join(base_path, timestamp)

    # This makes the dir locally – but the server must have this mount point too
    os.makedirs(backup_path, exist_ok=True)
    os.chmod(backup_path, 0o777)

    url = f"https://{host}:{port}/v1/bdbs/{bdb_uid}/actions/export"
    headers = {"Content-Type": "application/json"}
    data = {
        "export_location": {
            "type": "mount_point",
            "path": backup_path  # Must match what's registered in Redis Enterprise
        }
    }

    print("Sending request to:", url)
    print("Request payload:", json.dumps(data, indent=2))

    response = requests.post(
        url,
        headers=headers,
        json=data,
        auth=HTTPBasicAuth(user, password),
        verify=False  # Note: disables SSL verification; fine for dev/testing
    )

    print("Response code:", response.status_code)
    print("Response body:", response.text)

    return response

def find_uid_by_name(data, name):
    for item in data:
        if item.get("name") == name:
            return item.get("uid")
    return None

def get_bdbs():
    url = "https://localhost:9443/v1/bdbs"
    username = "demo@redis.com"
    password = "test"

    try:
        response = requests.get(url, auth=HTTPBasicAuth(username, password), verify=False)
        response.raise_for_status()  # Raises an error for bad responses (4xx or 5xx)
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        return None

# Example usage
if __name__ == "__main__":
    name_to_find = "test1"
    data = get_bdbs()
    if data:
       uid = find_uid_by_name(data,name_to_find)
       print(uid)
       print(export_redis_backup(uid))
