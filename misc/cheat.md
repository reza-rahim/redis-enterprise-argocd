
```
kubectl delete   -n argocd -f south-dev-rec-argo.yaml
kubectl delete  -n south-dev  rec south-dev-rec
kubectl delete  -n south-dev pvc redis-enterprise-storage-south-dev-rec-0  redis-enterprise-storage-south-dev-rec-1 redis-enterprise-storage-south-dev-rec-2

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
