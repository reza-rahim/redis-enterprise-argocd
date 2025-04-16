
### add some fake data
```
export KB=4096 #4KB

for i in {1..1000}; do
  VALUE=$(head -c $KB </dev/urandom | base64 | tr -d '\n' | head -c $KB)
  echo "SET key:$i $VALUE"
done > redis_commands.txt

cat redis_commands.txt | redis-cli -h db1 -p 13000 --tls --insecure --user user --pass password

```

### S3 backup and recovery 
```
read -r -d '' payload <<EOF
{
   "type": "s3",
   "bucket_name": "redis-argocd-bank",
   "subdir": "backup/11",
   "access_key_id": $AWS_ACCESS_KEY_ID,
   "secret_access_key": $AWS_SECRET_ACCESS_KEY
}
EOF

curl -k -u "$REC_USERNAME:$REC_PASSWORD" -X POST \
     -H "Content-Type: application/json" \
     -d "$payload" \
     https://south-dev-rec:9443/v1/bdbs/1/actions/export"

```

```
{
    "type": "s3",
    "bucket_name": bucketname,
    "subdir": f"/{hostname}/{db_name}/",
    "filename": file,
    "access_key_id": aws_access_key_id,
    "secret_access_key": aws_secret_access_key
}
```
