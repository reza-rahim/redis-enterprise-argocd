We are in the process of implementing a Redis database with remote backup functionality. As part of audit and compliance requirements, it is necessary to report which databases have the backup option enabled and the corresponding backup timestamps.

To support this, we are introducing two additional fields in the inventory JSON file:

persistence – Indicates whether backup is enabled.

backup_times – Captures the timestamps when backups were performed.

The Inventory team is requested to update the inventory database ingestion process to accommodate these two new fields.
