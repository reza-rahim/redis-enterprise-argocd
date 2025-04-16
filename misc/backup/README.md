
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
{
   "type": "s3",
   "bucket_name": bucketname,
   "subdir": f"{hostname}/{db_name}",
   "access_key_id": aws_access_key_id,
   "secret_access_key": aws_secret_access_key
}

https://{hostname}:{port}/v1/bdbs/{uid}/actions/export",
                auth=auth,
                headers={'Content-Type': 'application/json'},
                json=data,
                verify=False
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
