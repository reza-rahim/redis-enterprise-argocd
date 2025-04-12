# Redis Enterprise (RE) GitOps-Style Automated Deployment with ArgoCD

This guide outlines a GitOps-style, fully automated deployment of **two Redis Enterprise (RE) clusters** — one in the **north** and one in the **south** — using **ArgoCD** on **Kubernetes or OpenShift** environments. The primary objective is to shift all manual operations to the *initial setup phase*, so that once the automation begins, there are no intermediate manual steps required.

---

## 🌱 Initial Setup (Manual Prerequisites)

Before enabling GitOps automation, you need to perform the following **manual setup steps**. These are **one-time operations** that prepare your environment for a fully automated RE deployment.

---

### 1. 📦 Create a Shared S3-Compatible Bucket

A **shared object store** (e.g., AWS S3, MinIO, Ceph) is required to:

- Share the cluster topology configuration.
- Exchange sealed secrets between clusters.

You’ll need to create a bucket (e.g., `re-shared-config`) accessible to both RE clusters.

---

### 2. 🗺️ Define Cluster Topology

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

   

   
   
