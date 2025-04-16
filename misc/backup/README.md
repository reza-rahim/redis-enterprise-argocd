
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
