
```
rladmin tune db db:<ID> max_connections N
```
```
kubectl get secret -n south-dev  south-dev-rec  -o jsonpath="{.data.username}" | base64 --decode
echo
kubectl get secret -n south-dev  south-dev-rec  -o jsonpath="{.data.password}" | base64 --decode
echo
```

```
kubectl delete   -n argocd -f north-dev-rec-argo.yaml
kubectl delete  -n north-dev  rec north-dev-rec --grace-period=0 --force
kubectl delete  -n north-dev pvc redis-enterprise-storage-north-dev-rec-0  redis-enterprise-storage-north-dev-rec-1 redis-enterprise-storage-north-dev-rec-2
kubectl delete  -n north-dev job redis-job    
kubectl delete  -n north-dev deploy health-check
```

```
kubectl delete   -n argocd -f south-dev-rec-argo.yaml
kubectl delete  -n south-dev  rec south-dev-rec --grace-period=0 --force
#kubectl patch -n south-dev  rec/south-dev-rec --type=merge -p '{"metadata": {"finalizers":null}}'
kubectl delete  -n south-dev pvc redis-enterprise-storage-south-dev-rec-0  redis-enterprise-storage-south-dev-rec-1 redis-enterprise-storage-south-dev-rec-2
kubectl delete  -n south-dev job redis-job    
kubectl delete  -n south-dev deploy health-check
kubectl delete -f south-dev-db1-argo.yaml

```

### Change password
```
read -r -d '' payload <<EOF
{
    "username": "user",
    "old_password": "password",
    "new_password": "password1"
}
EOF

curl -k -u "$REC_USERNAME:$REC_PASSWORD" -X POST \
-H "Content-Type: application/json" \
-d "$payload" \
"https://south-dev-rec:9443/v1/users/password"
```

```
read -r -d '' payload <<EOF
{
  "email": "health-check-user@example.com",
  "password": "$HEATHCHECK_PASSWORD",
  "name": "$HEATHCHECK_USERNAME",
  "role_uids": [2],
  "auth_method": "regular"
}
EOF

curl -k -u "$REC_USERNAME:$REC_PASSWORD" -X POST \
  -H 'Content-Type: application/json' \
  -d "$payload" \
  "https://${REC_HOSTNAME}:9443/v1/users"

 curl -k -u "$REC_USERNAME:$REC_PASSWORD" -X POST \
      -H 'Content-Type: application/json' \
      -d '{"management":"none","name":"full-access-role"}' \
      https://south-dev-rec:9443/v1/roles
```
```      

###
curl -k -u "$REC_USERNAME:$REC_PASSWORD" -X POST \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "password",
    "name": "user",
    "role_uids": [3],
    "auth_method": "regular"
  }' \
  "https://south-dev-rec:9443/v1/users"
```
