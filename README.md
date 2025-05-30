# Redis Enterprise (RE) GitOps-Style Automated Deployment with ArgoCD on K8/Openshift

This guide outlines a GitOps-style, fully automated deployment of **two Redis Enterprise (RE) clusters** — one in the **north** and one in the **south** — using **ArgoCD** on **Kubernetes or OpenShift** environments. The primary objective is to shift all manual operations to the *initial setup phase*, so that once the automation begins, there are no intermediate manual steps required.

---
## [What is GitOps?](docs/gitops/README.md)

---

##  Initial Setup (Manual Prerequisites)

Before enabling GitOps automation, you need to perform the following **manual setup steps**. These are **one-time operations** that prepare your environment for a fully automated RE deployment.



### 1. Create a Shared S3-Compatible Bucket

A **shared object store** (e.g., AWS S3, MinIO, Ceph) is required to:

- Share the cluster topology configuration.
- Exchange sealed secrets between clusters.

You’ll need to create a bucket (e.g., `re-shared-config`) accessible to both RE clusters.



### 2. Define Cluster Topology

Inside the shared bucket, create a file named `cluster_config.json`. This file outlines the participating RE clusters, their roles, and where to store their state/configuration within the bucket. <br>
The values in the JSON file may vary across environments like dev, test, and prod. To handle this, we can create environment-specific directories and place the corresponding cluster_config.json file in each one.

- [S3_bucket]/dev
- [S3_bucket]/test
- [S3_bucket]/prod



```json
[
  {
    "clusername": "south",
    "s3_dir": "south",
    "apiFqdnUrl": "api.south.ps-redis.com",
    "dbFqdnSuffix": "-cluster.south.ps-redis.com",
    "apiPort": 443
  },
  {
    "clusername": "north",
    "s3_dir": "north",
    "apiFqdnUrl": "api.north.ps-redis.com",
    "dbFqdnSuffix": "-cluster.north.ps-redis.com",
    "apiPort": 443
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

**This is inspired by ["Sealed Secrets" for Kubernetes project](https://github.com/bitnami-labs/sealed-secrets)**

Problem: "I can manage all my K8s config in git, except Secrets."<br>

Solution: Encrypt your Secret into a SealedSecret, which is safe to store - even inside a public repository. The SealedSecret can be decrypted only by the controller running in the target cluster and nobody else (not even the original author) is able to obtain the original Secret from the SealedSecret.

### 5. Create username and password for health check upser


```
kubectl create secret generic health-check-user -n  $NSP \
  --from-literal=username=health-check-user \
  --from-literal=password=<password>
```

---

## Setup ArgoCD on K8 
```
kubectl create namespace argocd
kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml

# https://localhost:8080/ for ArgoCD webUI 
# use admin/initial-password to login
kubectl port-forward svc/argocd-server -n argocd 8080:443

# How to get the initial-password
argocd admin initial-password -n argocd
kubectl get secret -n argocd argocd-initial-admin-secret -o jsonpath="{.data.password}" | base64 -d
```

### Argo CD Resource Hooks
Argo CD resource hooks offer flexibility by allowing users to execute custom scripts at various stages of the application’s lifecycle. This can be particularly useful in scenarios that require going beyond the default behavior provided by Kubernetes. [More on Argo CD Resource Hooks](https://codefresh.io/learn/argo-cd/argo-cd-hooks-the-basics-and-a-quick-tutorial/)<br>

Let's build a custom Docker container to handle various pre- and post-processing tasks using ArgoCD hooks.

The [Dockerfile](docker/Dockerfile)
```
docker build -t rezarahim/alpine-tools:1.1 .
docker push  rezarahim/alpine-tools:1.1
```
---

## Redis Enterprise for Kubernetes Documentaion

**We assume you are familiar with the manual process of deploying Redis Enterprise (RE) using the operator in a Kubernetes environment.** <br>
[Redis Enterprise for Kubernetes](https://redis.io/docs/latest/operate/kubernetes/)

[Redis Enterprise for Kubernetes Github location for Example and CRD ](https://github.com/RedisLabs/redis-enterprise-k8s-docs)

---
## Setup the South Cluster



### Let's look into [ArgoCD Application](https://argo-cd.readthedocs.io/en/stable/core_concepts/) [south-dev-operator-argo.yaml](https://github.com/reza-rahim/redis-enterprise-argocd/blob/main/south/south-dev-operator-argo.yaml) for dev env.

```
apiVersion: argoproj.io/v1alpha1
kind: Application
```
- This defines the resource type — an Application from ArgoCD.

- This is how you tell ArgoCD what to deploy and where.


```
metadata:
  name: south-dev-operator-argo
  namespace: argocd
```
- name: This is the name of your ArgoCD Application.

- namespace: This is the namespace where ArgoCD itself is installed, not where your app is deployed. ArgoCD watches its own namespace (argocd).

#### Source — Where to get the manifests
```
  source:
    repoURL: https://github.com/reza-rahim/redis-enterprise-argocd/
    targetRevision: main
    path: south/operator-chart
    helm:
      valueFiles:
      - dev-values.yaml
```
This tells ArgoCD where to pull your deployment config from:

- repoURL: GitHub repo that contains your app’s Helm chart or Kubernetes YAML.

- targetRevision: Git branch to track — here it’s main.

- path: Folder in the repo that contains the Helm chart.

- helm.valueFiles: You’re using Helm, and passing dev-values.yaml — likely contains environment-specific settings (like image versions, replicas, resource limits, etc.).

#### Destination — Where to deploy
```
  destination:
    server: https://kubernetes.default.svc
    namespace: dev
```
- server: Tells ArgoCD to deploy to the Kubernetes cluster it's running in.

- namespace: The app will be deployed into the prod namespace in the cluster.

#### Sync Policy — How it stays in sync
```
  syncPolicy: 
    automated:
      prune: true
      selfHeal: true
    syncOptions:
      - CreateNamespace=true
```
This controls how ArgoCD keeps the app in sync with Git:

- automated: Enables automatic syncing (no need to click “Sync” manually).

- prune: true: Deletes resources from the cluster if they're no longer in Git.

- selfHeal: true: Automatically fixes any drift if something changes in the cluster.

syncOptions:

- CreateNamespace=true: If the prod namespace doesn’t exist, ArgoCD will create it for you.

**Let's look into ArgoCD Application [south-prod-operator-argo.yaml](https://github.com/reza-rahim/redis-enterprise-argocd/blob/main/south/south-prod-operator-argo.yaml) for prod env.**<br>

Main Differencein the helm.valueFiles section:
```
helm:
  valueFiles:
  - dev-values.yaml
  - prod-values.yaml
```
Helm allows multiple values files to be layered. When two or more files are used, So prod-values.yaml will override any overlapping settings from dev-values.yaml.

---
### Deploy the Redis Operator for South cluster.
```
  kubectl apply -n argocd -f south-dev-operator-argo.yaml
  kubectl get -n south-dev  po
```
<br>
ArgoCD UI:
<img src="images/operator-south-dev.png" width="800">
<br>

---
### Deploy the Redis cluser for South cluster.
```
kubectl apply -n argocd -f south-dev-rec-argo.yaml
  kubectl get -n south-dev  po
```
  
<br>
ArgoCD UI:
<img src="images/rec-south-dev.png" width="800">
<br>

---

### Deploy the Redis Operator for North cluster.
```
  kubectl apply -n argocd -f north-dev-operator-argo.yaml
  kubectl get -n south-dev  po
```

---
### Deploy the Redis cluser for South cluster.
```
kubectl apply -n argocd -f north-dev-rec-argo.yaml
kubectl get -n south-dev  po
```
---
### Description of Rec deployment and the associated CI jobs,
**This Helm chart installs a Kubernetes Job that configures Redis Enterprise Remote Clusters securely by handling secrets, ACLs, roles, and cross-cluster connection setup.**

**Kubernetes Job ([redis-job](north/rec-north-chart/templates/redis-posthook-job.yaml))**<br>
- Triggered post-install using Helm hooks.

- Waits for the target Redis Enterprise Cluster API to become available via repeated curl checks.
  - Sources two config scripts:
  - [config-map-acl.sh](north/rec-north-chart/templates/config_map_acl.yaml) (ACL/user setup)
  - [config-map-rec.sh](north/rec-north-chart/templates/config_map_rec.yaml) (cluster sync and secret handling)

**ConfigMaps**<br>

A. **config-map-acl.sh**
- Uses the Redis Enterprise API to:
  - Create an ACL
  - Create a role (health-check-role)
  - Create a user with specific credentials and assign the role

B. **config-map-rec.sh**
- Sets environment-specific variables using Helm values.
- Downloads a cluster_config.json file from S3 containing configuration for all clusters.
- For the primary cluster:
  - Encrypts and uploads its credentials to S3 using RSA keys.

Then:

- Waits until all clusters’ credentials are uploaded to S3.
- For each cluster:
  - Decrypts credentials from S3
  - Creates Kubernetes secrets
  - Applies a RedisEnterpriseRemoteCluster resource to establish connectivity

**Secrets and Encryption**<br>
- RSA keys are pulled from Kubernetes secrets.
- Credentials are encrypted before upload and decrypted when pulled.
- Secrets are dynamically created per cluster.

**Environment Support**<br>
- Uses Helm values to support multiple environments (dev, test, prod).
- Each environment can have its own cluster_config.json.

---

### Database Health check

Health Check a Flask-based Redis health check web app in a Kubernetes cluster. It exposes a /probe endpoint that checks Redis connectivity and key availability with optional TLS.<br>
The goal is to provide a flexible, parameterized HTTP endpoint (/probe) that can be used to probe Redis clusters securely or insecurely, supporting custom host/port settings and returning health status.
**Key Components**

1. ConfigMap ([flask-redis-app](north/rec-north-chart/templates/config_map_healthcheck_app.yaml))
   - Stores a Flask app (app.py) that:
     - Reads Redis connection parameters (host, port, tls) from URL query params.
     - Fetches Redis username/password from environment variables.
     - Connects to Redis, skipping TLS verification if needed (ssl_cert_reqs="none").
     - Queries 10 keys (xxxxxxx0 to xxxxxxx9) and returns 200 OK or 500 Error.
2. Service ([health-check](north/rec-north-chart/templates/healthcheck.yaml))
   - Exposes the Flask app internally on port 5000 using ClusterIP.

3. Deployment ([health-check](north/rec-north-chart/templates/healthcheck.yaml))
   - Deploys 1 pod using the image rezarahim/alpine-tool:1.2.
     - Runs the Flask app from the mounted ConfigMap at /etc/config/health/app.py.
     - Uses environment variables for Redis credentials from the Kubernetes Secret named health-check-user.
     - Mounts the Flask app via a volume referencing the flask-redis-app ConfigMap.

```
#host is service or db name
#database port
#Database is tls enable or not 
http://health-check:5000/probe?host=db1&port=13000&tls=true
```


**This Bash script checks the health of a Redis instance via an HTTP probe up to 5 times:**

- It uses parameterized variables for timeout, sleep, host, port, and TLS.
- Sends a request to a health-check endpoint and captures the HTTP status code.
- If the response is 200 (OK), it prints "database healthy" and exits with code 0.
- Otherwise, it waits and retries up to 5 times, then exits with code 1 if all fail.

```
#!/bin/bash

TIMEOUT_DURATION=2      # Timeout for curl in seconds
RETRY_INTERVAL=5        # Wait time between retries in seconds
HOST="db1"              # Redis db service name
PORT="13000"            # Redis port
TLS="true"              # TLS enabled or not (true/false)

for i in 1 2 3 4 5
do
  URL="http://health-check:5000/probe?host=$HOST&port=$PORT&tls=$TLS"
  status_code=$(timeout "$TIMEOUT_DURATION" curl -s -o /dev/null -w "%{http_code}" "$URL")

  if [[ "$status_code" == "200" ]]; then
    echo "database healthy"
    exit 0
  fi

  echo "database unhealthy (HTTP $status_code), retrying in $RETRY_INTERVAL sec"
  sleep "$RETRY_INTERVAL"
done

exit 1

```

**The shell variable $? holds the exit status of the last executed command:**

- 0 means success (the command ran without errors).
- Any non-zero value means failure (the command encountered an error).


```
# command

if [[ $? == 0 ]]; then
  echo "Success"
else
  echo "Failure"
fi
```


**Ingress example [link](misc/ingress/healtcheck.yaml)**


---

### Deploy a single region Database  


```
kubectl apply -f south-dev-db1-argo.yaml
```

The example database **db1** will be created with two Users created previously by [config_map_acl.yaml](south/rec-south-chart/templates/config_map_acl.yaml) 
-  DB User `health-check-user`, Role: `health-check-role`
-  DB User `user`, Rol e:`full-access-role` 

<br>[south-dev-db1-argo.yaml](south/db1-chart/templates/db1.yaml)

```
apiVersion: app.redislabs.com/v1alpha1
kind: RedisEnterpriseDatabase
metadata:
  name: db1
spec:
  memorySize: {{ .Values.memorySize }}
  databasePort: {{ .Values.databasePort }}
  shardCount: {{ .Values.shardCount }}
  replication: true
  tlsMode: enabled
  rolesPermissions:
    - role: "health-check-role"
      acl: "health-check-acl"
      type: "redis-enterprise"
    - role: "full-access-role"
      acl: "Full Access"
      type: "redis-enterprise"
```

<img src="images/db1.png" width="800">

<br>

**Accessing the database db1**([ingres file](misc/ingress/healtcheck.yaml)
```
redis-cli -h db1.south-dev -p 13000 --tls --insecure 
auth user password
```

