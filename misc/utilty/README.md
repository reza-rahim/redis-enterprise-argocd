```


kubectl delete -n north-dev po redis-pod
export RECNAME=north-dev-rec;envsubst < redis-pod.yaml |  kubectl apply -n north-dev  -f -
kubectl exec -it -n north-dev redis-pod -- sh


--

export RECNAME=south-dev-rec;envsubst < redis-pod.yaml | kubectl apply -n south-dev  -f -
kubectl exec -it -n south-dev redis-pod -- sh
kubectl delete -n south-dev po redis-pod

#--grace-period=0 --force

```

```

read -r -d '' payload <<EOF
{
   "username": "user",
   "old_password": "password",
   "new_password": "password1"
}
EOF

curl -k -u "$REC_USERNAME:$REC_PASSWORD" -X PUT \
     -H "Content-Type: application/json" \
     -d "$payload" \
     "https://south-dev-rec:9443/v1/users/password"

read -r -d '' payload <<EOF
{
   "username": "user",
   "old_password": "password1",
   "new_password": "password"
}
EOF
```

