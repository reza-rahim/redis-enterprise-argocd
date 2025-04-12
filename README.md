# Redis Enterprise (RE) GitOps-Style Automated Deployment with ArgoCD

This guide outlines a GitOps-style, fully automated deployment of **two Redis Enterprise (RE) clusters** — one in the **north** and one in the **south** — using **ArgoCD** on **Kubernetes or OpenShift** environments. The primary objective is to shift all manual operations to the *initial setup phase*, so that once the automation begins, there are no intermediate manual steps required.

---

##  Initial Setup (Manual Prerequisites)

Before enabling GitOps automation, you need to perform the following **manual setup steps**. These are **one-time operations** that prepare your environment for a fully automated RE deployment.

---

### 1. Create a Shared S3-Compatible Bucket

A **shared object store** (e.g., AWS S3, MinIO, Ceph) is required to:

- Share the cluster topology configuration.
- Exchange sealed secrets between clusters.

You’ll need to create a bucket (e.g., `re-shared-config`) accessible to both RE clusters.

---

### 2. Define Cluster Topology

Inside the shared bucket, create a file named `clusters_topology_config.json`. This file outlines the participating RE clusters, their roles, and where to store their state/configuration within the bucket.

```json
[
  {
    "clusername": "south",
    "s3_dir": "south",
    "primary": true
  },
  {
    "clusername": "north",
    "s3_dir": "north",
    "primary": false
  }
]
```

### 3. Create AWS Credentials Secret
On each Kubernetes or OpenShift cluster (in the target namespace where RE will be deployed), create a Kubernetes secret with your object store credentials:

```
kubectl create secret generic aws-credentials -n <namespace> \
  --from-literal=AWS_ACCESS_KEY_ID=<your-access-key-id> \
  --from-literal=AWS_SECRET_ACCESS_KEY=<your-secret-access-key>

```

### 4. Generate and Share PKI Key Pair for Sealed Secrets
To securely share sealed secrets across clusters, we use a shared RSA key pair (private/public). All clusters must use the same key pair for encryption and decryption of sensitive data (e.g., passwords, tokens).<br>

a. Generate the RSA Key Pair:
```
openssl genpkey -algorithm RSA -out private_key.pem
openssl rsa -pubout -in private_key.pem -out public_key.pem
```
b. Create Kubernetes Secret in Each Cluster:<br>
Distribute the key pair to all participating clusters by creating a secret in the target namespace:

```
kubectl create secret generic rsa-keys -n <namespace> \
  --from-file=private_key.pem \
  --from-file=public_key.pem
```


