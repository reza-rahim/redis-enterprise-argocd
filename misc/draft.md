We are in the process of implementing a Redis database with remote backup functionality. As part of audit and compliance requirements, it is necessary to report which databases have the backup option enabled and the corresponding backup timestamps.

To support this, we are introducing two additional fields in the inventory JSON file:

persistence – Indicates whether backup is enabled.

backup_times – Captures the timestamps when backups were performed.

The Inventory team is requested to update the inventory database ingestion process to accommodate these two new fields.


https://www.linkedin.com/pulse/big-shift-from-kubernetes-power-tool-invisible-plumbing-reza-rahim-nc8vc

https://www.linkedin.com/pulse/fine-tuning-embedding-model-synthetic-data-improving-rag-reza-rahim-ayvsc/


```
curl \
  --header "Authorization: Bearer $TFE_TOKEN" \
  https://app.terraform.io/api/v2/workspaces/<workspace-id>/state-versions

curl \
  --request DELETE \
  --header "Authorization: Bearer $TFE_TOKEN" \
  https://app.terraform.io/api/v2/state-versions/<state-version-id>

```

```
terraform apply -parallelism=1

find /path/to/directory -type f -mtime +7
```

```
crdb-cli crdb create \
  --name db \
  --memory-size 1GB \
  --encryption yes \
  --port 12000 \
  --password test \
  --instance fqdn=rec02.ns2.svc.cluster.local,url=https://api.apps.demo-2.ps-redis.com,username=demo@redislabs.com,password=DwTox56v,replication_endpoint=db-cluster.demo-2.ps-redis.com:443,replication_tls_sni=db-cluster.demo-2.ps-redis.com \
  --instance fqdn=rec03.ns3.svc.cluster.local,url=https://api.apps.demo-3.ps-redis.com,username=demo@redislabs.com,password=5bpxJEVo,replication_endpoint=db-cluster.demo-3.ps-redis.com:443,replication_tls_sni=db-cluster.demo-3.ps-redis.com
```

```
import csv

with open('your_file.csv', newline='') as csvfile:
    reader = csv.DictReader(filter(lambda row: not row.startswith('#'), csvfile))
    for row in reader:
        kv = dict(row)
        print(kv)

```

```
https://redis.io/docs/latest/operate/rs/networking/cluster-lba-setup/#network-architecture-with-load-balancer
```


