```
import boto3

s3 = boto3.client('s3')

bucket_name = 'your-bucket-name'
object_key = 'path/to/file.txt'

response = s3.get_object(Bucket=bucket_name, Key=object_key)

# The file content is in the 'Body' stream
content = response['Body'].read().decode('utf-8')

# Print or list the lines
lines = content.splitlines()
for line in lines:
    print(line)

```
