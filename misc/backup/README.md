
### add some fake data
```
export KB=4096 #4KB

for i in {1..1000}; do
  VALUE=$(head -c $KB </dev/urandom | base64 | tr -d '\n' | head -c $KB)
  echo "SET key:$i $VALUE"
done > redis_commands.txt

cat redis_commands.txt | redis-cli -h db1 -p 13000 --tls --insecure --user user --pass password

```

### S3 backup 
```
read -r -d '' payload <<EOF
{
   "export_location": {
     "type": "s3",
     "bucket_name": "redis-argocd-bank",
     "subdir": "backup/11",
     "access_key_id": "$AWS_ACCESS_KEY_ID",
     "secret_access_key": "$AWS_SECRET_ACCESS_KEY"
  }
}
EOF

curl -k -u "$REC_USERNAME:$REC_PASSWORD" -X POST \
     -H "Content-Type: application/json" \
     -d "$payload" \
     "https://south-dev-rec:9443/v1/bdbs/1/actions/export"

```

## recovery 
```
{
    "type": "s3",
    "bucket_name": bucketname,
    "subdir": f"/{hostname}/{db_name}/",
    "filename": file,
    "access_key_id": aws_access_key_id,
    "secret_access_key": aws_secret_access_key
}

https://{hostname}:{port}/v1/bdbs/{uid}/actions/import",
                    auth=auth,
                    headers={"Content-Type": "application/json"},
                    json=data,
                    verify=False
```

```
Example Directory Structure After Export
/tmp/backup/
└── mydb/
    └── 20250416T160230/
        └── (backup files here)
```

```
from pathlib import Path
try:
    base_path = Path('/your/base/directory')  # Change this to your actual path
    directories = [d.name for d in base_path.iterdir() if d.is_dir()]
except Exception as e:
    print(f"An unexpected error occurred: {e}")
    directories = []
```
